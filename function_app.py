import os
import json
import azure.functions as func

from azure.cosmos import CosmosClient
try:
    from azure.cosmos.exceptions import CosmosHttpResponseError
except Exception:
    CosmosHttpResponseError = Exception

app = func.FunctionApp()

def get_cosmos_client():
    uri = os.getenv("COSMOS_URI")
    key = os.getenv("COSMOS_KEY")
    if not uri or not key:
        raise RuntimeError("COSMOS_URI or COSMOS_KEY not set in environment.")
    return CosmosClient(uri, credential=key)

def get_db_and_container(client):
    # Defaults set to your values
    db_name = os.getenv("COSMOS_DATABASE", "productdb")
    container_name = os.getenv("COSMOS_CONTAINER", "productcontainer")
    db = client.get_database_client(db_name)
    container = db.get_container_client(container_name)
    return db, container

@app.function_name(name="get_product")
@app.route(route="product/{prod_id}", methods=["GET"])
def get_product(req: func.HttpRequest) -> func.HttpResponse:
    prod_id = req.route_params.get("prod_id")
    try:
        client = get_cosmos_client()
        _, container = get_db_and_container(client)
        # Ensure container partition key is /id — change partition_key if different
        item = container.read_item(item=prod_id, partition_key=prod_id)
        return func.HttpResponse(json.dumps(item), status_code=200, mimetype="application/json")
    except RuntimeError as e:
        return func.HttpResponse(str(e), status_code=500)
    except CosmosHttpResponseError as e:
        return func.HttpResponse(f"Cosmos error: {e}", status_code=500)
    except Exception as e:
        return func.HttpResponse(f"Error reading item: {e}", status_code=500)

@app.function_name(name="list_products")
@app.route(route="products", methods=["GET"])
def list_products(req: func.HttpRequest) -> func.HttpResponse:
    try:
        client = get_cosmos_client()
        _, container = get_db_and_container(client)
        query = "SELECT * FROM c"
        items_iter = container.query_items(query=query, enable_cross_partition_query=True)
        items = list(items_iter)
        return func.HttpResponse(json.dumps(items), status_code=200, mimetype="application/json")
    except RuntimeError as e:
        return func.HttpResponse(str(e), status_code=500)
    except CosmosHttpResponseError as e:
        return func.HttpResponse(f"Cosmos error: {e}", status_code=500)
    except Exception as e:
        return func.HttpResponse(f"Error listing items: {e}", status_code=500)

@app.function_name(name="create_product")
@app.route(route="product", methods=["POST"])
def create_product(req: func.HttpRequest) -> func.HttpResponse:
    try:
        client = get_cosmos_client()
        _, container = get_db_and_container(client)

        body = req.get_json()
        if not isinstance(body, dict):
            return func.HttpResponse("Invalid JSON body", status_code=400)
        if "id" not in body:
            return func.HttpResponse("Request JSON must include 'id' field", status_code=400)

        container.create_item(body)
        return func.HttpResponse("Created", status_code=201)
    except RuntimeError as e:
        return func.HttpResponse(str(e), status_code=500)
    except CosmosHttpResponseError as e:
        return func.HttpResponse(f"Cosmos error: {e}", status_code=500)
    except Exception as e:
        return func.HttpResponse(f"Error creating item: {e}", status_code=500)

@app.function_name(name="update_product")
@app.route(route="product/{prod_id}", methods=["PUT"])
def update_product(req: func.HttpRequest) -> func.HttpResponse:
    prod_id = req.route_params.get("prod_id")
    try:
        client = get_cosmos_client()
        _, container = get_db_and_container(client)

        body = req.get_json()
        if not isinstance(body, dict):
            return func.HttpResponse("Invalid JSON body", status_code=400)

        body["id"] = prod_id
        container.upsert_item(body)
        return func.HttpResponse("Updated", status_code=200)
    except RuntimeError as e:
        return func.HttpResponse(str(e), status_code=500)
    except CosmosHttpResponseError as e:
        return func.HttpResponse(f"Cosmos error: {e}", status_code=500)
    except Exception as e:
        return func.HttpResponse(f"Error updating item: {e}", status_code=500)

@app.function_name(name="delete_product")
@app.route(route="product/{prod_id}", methods=["DELETE"])
def delete_product(req: func.HttpRequest) -> func.HttpResponse:
    prod_id = req.route_params.get("prod_id")
    try:
        client = get_cosmos_client()
        _, container = get_db_and_container(client)

        container.delete_item(item=prod_id, partition_key=prod_id)
        return func.HttpResponse(status_code=204)
    except RuntimeError as e:
        return func.HttpResponse(str(e), status_code=500)
    except CosmosHttpResponseError as e:
        return func.HttpResponse(f"Cosmos error: {e}", status_code=500)
    except Exception as e:
        return func.HttpResponse(f"Error deleting item: {e}", status_code=500)
