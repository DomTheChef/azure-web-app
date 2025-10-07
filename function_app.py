import azure.functions as func
from azure.cosmos import CosmosClient
import os, uuid

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="track", methods=["GET", "POST"])
def track(req: func.HttpRequest) -> func.HttpResponse:
    try:
        conn = os.environ.get("CosmosDBConnection")
        if not conn:
            return func.HttpResponse("Missing CosmosDBConnection setting", status_code=500)

        client = CosmosClient.from_connection_string(conn)
        database = client.get_database_client("VisitCount")
        container = database.get_container_client("Visitors")

        item = {"id": str(uuid.uuid4()), "note": "testEntry"}
        container.create_item(item)

        return func.HttpResponse("Ok", status_code=200)
    except Exception as e:
        return func.HttpResponse(f"CosmosDB error: {e}", status_code=500)
