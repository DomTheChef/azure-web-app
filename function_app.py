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
container = cosmos_client.get_database_client(
    COSMOS_DATABASE_NAME
).get_container_client(COSMOS_CONTAINER_NAME)
@app.route(route="track", methods=["GET"])
def track(req: func.HttpRequest) -> func.HttpResponse:
    try:
        client_ip = (
            req.headers.get("X-Forwarded-For", "").split(",")[0].strip()
            or req.headers.get("X-Client-IP")
            or "unknown"
        )

        item = {
            "id": str(uuid.uuid4()),
            "type": "pageview",
            "accessedAtUtc": datetime.now(timezone.utc).isoformat(),
            "visitorIp": client_ip,
        }

        container.create_item(item)

        count = sum(1 for _ in container.read_all_items())

        return func.HttpResponse(
            body=f'{{"status":"ok","totalVisits":{count}}}',
            status_code=200,
            mimetype="application/json",
        )

    except Exception as e:
        logging.error(f"Cosmos DB write failed: {e}")
        return func.HttpResponse(
            body=f'{{"status":"error","message":"{str(e)}"}}',
            status_code=500,
            mimetype="application/json",
        )