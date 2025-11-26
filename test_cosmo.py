from azure.cosmos import CosmosClient
import os

uri = os.getenv("COSMOS_URI")
key = os.getenv("COSMOS_KEY")

client = CosmosClient(uri, credential=key)
db = client.get_database_client("productdb")
container = db.get_container_client("productcontainer")

items = container.query_items(
    query="SELECT * FROM c",
    enable_cross_partition_query=True
)

print(list(items))
