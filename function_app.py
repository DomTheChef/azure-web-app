import azure.functions as func
from azure.cosmos import CosmosClient
import os

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

COSMOS_CONN = os.environ["CosmosDBConnection"]   
DB_NAME = "VisitCount"                     
CONTAINER_NAME = "Visitors"                   

client = CosmosClient.from_connection_string(COSMOS_CONN)
database = client.get_database_client(DB_NAME)
container = database.get_container_client(CONTAINER_NAME)

@app.route(route="track", methods=["GET", "POST"])
def track(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("OK", status_code=200)