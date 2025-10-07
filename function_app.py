import azure.functions as func
from azure.cosmos import CosmosClient
import os
import uuid

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

COSMOS_CONN = os.environ["CosmosDBConnection"]   
DB_NAME = "VisitCount"                     
CONTAINER_NAME = "Visitors"                   

@app.route(route="track", methods=["GET", "POST"])
def track(req: func.HttpRequest) -> func.HttpResponse:
    try:
        conn = os.environ["CosmosDBConnection"]
        client = CosmosClient.from_connection_string(conn)
        database = client.get_database_client(DB_NAME)
        container = database.get_container_client(CONTAINER_NAME)

        # Testing insert into Cosmos container..
        item = {"id": str(uuid.uuid4()), "note": "testEntry"}
        container.create_item(item)

        return func.HttpResponse("Ok", status_code=200)
    except Exception as e:
        return func.HttpResponse(f"CosmosDB error: {e}", status_code=500)

