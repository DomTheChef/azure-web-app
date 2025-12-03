import azure.functions as func
import uuid
import logging
import os

from azure.identity import DefaultAzureCredential
from azure.cosmos import CosmosClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_DATABASE_NAME = os.getenv("COSMOS_DATABASE_NAME", "VisitCount")
COSMOS_CONTAINER_NAME = os.getenv("COSMOS_CONTAINER_NAME", "Visitors")

credential = DefaultAzureCredential()

cosmos_client = CosmosClient(COSMOS_ENDPOINT, credential=credential)
cosmos_container = cosmos_client.get_database_client(COSMOS_DATABASE_NAME).get_container_client(
    COSMOS_CONTAINER_NAME
)

@app.route(route="track", methods=["GET"])
def track(req: func.HttpRequest) -> func.HttpResponse:
    try:
        item = {
            "id": str(uuid.uuid4()),
            "note": "Prod test entry",
        }

        cosmos_container.create_item(item)

        return func.HttpResponse("Inserted into Cosmos via Managed Identity!", status_code=200)
    except Exception as e:
        logging.error(f"Cosmos DB write failed: {e}")
        return func.HttpResponse(f"Cosmos DB write failed: {e}", status_code=500)
