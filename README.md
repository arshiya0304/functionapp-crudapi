Products CRUD API (Azure Functions + Cosmos DB) Project Overview

Create a simple HTTP CRUD API for Products using Python Azure Functions and Cosmos DB (SQL API). Operations:
POST /api/products → Create product
GET /api/products → List all products
GET /api/products/{id} → Retrieve product by ID
PUT /api/products/{id} → Update product
DELETE /api/products/{id} → Delete product

Database: Cosmos DB Container Products with partition key /id.

Prerequisites:
Python 3.10+,VS Code,Azure Functions Core Tools,Azure Cosmos DB account

Setup Steps:
Clone the repository
git clone cd
Create virtual environment and activate
Windows
python -m venv venv venv\Scripts\activate
Linux/Mac
python3 -m venv venv source venv/bin/activate
Install dependencies
pip install azure-functions azure-cosmos
Configure local.settings.json
{ "IsEncrypted": false, "Values": { "AzureWebJobsStorage": "", "FUNCTIONS_WORKER_RUNTIME": "python", "COSMOS_DB_CONN_STR": "", "COSMOS_DB_DATABASE": "ProductsDB", "COSMOS_DB_CONTAINER": "Products" } }
Create Functions
POST /api/products → Create product
GET /api/products → List all products
GET /api/products/{id} → Retrieve product by ID
PUT /api/products/{id} → Update product by ID
DELETE /api/products/{id} → Delete product by ID
Run Locally func start
Endpoints will be available at: http://localhost:7071/api/...
Test API Endpoints
POST
curl -X POST http://localhost:7071/api/products
-H "Content-Type: application/json"
-d '{"id":"p100","name":"Wireless Mouse","price":249.5,"tags":["peripherals","wireless"]}'
GET All
curl http://localhost:7071/api/products
GET by ID
curl http://localhost:7071/api/products/p100
PUT
curl -X PUT http://localhost:7071/api/products/p100
-H "Content-Type: application/json"
-d '{"name":"Wireless Mouse Pro","price":299.5}'
DELETE
curl -X DELETE http://localhost:7071/api/products/p100
Deploy to Azure
Login to Azure:
az login
Create Function App in Azure
Deploy:
func azure functionapp publish
Sample Product Document { "id": "p100", "name": "Wireless Mouse", "price": 249.5, "tags": ["peripherals","wireless"] }
Notes
Partition key must be /id in Cosmos DB.
Validate id and numeric price.
Proper HTTP status codes: 201, 200, 204, 404, 400.
Logs can be viewed in VS Code terminal or Azure Portal.
pip install azure-functions azure-cosmos
Configure local.settings.json
{ "IsEncrypted": false, "Values": { "AzureWebJobsStorage": "", "FUNCTIONS_WORKER_RUNTIME": "python", "COSMOS_DB_CONN_STR": "", "COSMOS_DB_DATABASE": "ProductsDB", "COSMOS_DB_CONTAINER": "Products" } }
Create Functions
POST /api/products → Create product
GET /api/products → List all products
GET /api/products/{id} → Retrieve product by ID
PUT /api/products/{id} → Update product by ID
DELETE /api/products/{id} → Delete product by ID
Run Locally func start
Endpoints will be available at: http://localhost:7071/api/...
Test API Endpoints

POST
curl -X POST http://localhost:7071/api/products
-H "Content-Type: application/json"
-d '{"id":"p100","name":"Wireless Mouse","price":249.5,"tags":["peripherals","wireless"]}'

GET All
curl http://localhost:7071/api/products
GET by ID
curl http://localhost:7071/api/products/p100

PUT
curl -X PUT http://localhost:7071/api/products/p100
-H "Content-Type: application/json"
-d '{"name":"Wireless Mouse Pro","price":299.5}'

DELETE
curl -X DELETE http://localhost:7071/api/products/p100
Deploy to Azure
Login to Azure:

az login
Create Function App in Azure

Deploy:
func azure functionapp publish
Sample Product Document { "id": "p100", "name": "Wireless Mouse", "price": 249.5, "tags": ["peripherals","wireless"] }

Notes:
Partition key must be /id in Cosmos DB.
Validate id and numeric price.
Proper HTTP status codes: 201, 200, 204, 404, 400.
Logs can be viewed in VS Code terminal or Azure Portal.
