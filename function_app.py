import azure.functions as func
import os
import uuid
from datetime import datetime, timezone
from azure.cosmos import CosmosClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

COSMOS_CONN = os.environ["CosmosDBConnection"]   
DB_NAME = "VisitCount"                     
CONTAINER_NAME = "Visitors"                   

client = CosmosClient.from_connection_string(COSMOS_CONN)
database = client.get_database_client(DB_NAME)
container = database.get_container_client(CONTAINER_NAME)

@app.function_name(name="track_visit")
@app.route(route="track")
def track_visit(req: func.HttpRequest) -> func.HttpResponse:
    try:
        visit = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        }

        container.create_item(body=visit)

        return func.HttpResponse("Site visit recorded", status_code=200)
    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)