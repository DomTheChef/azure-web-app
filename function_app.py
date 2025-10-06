import azure.functions as func
import os
import uuid
from datetime import datetime, timezone
from azure.cosmos import CosmosClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.function_name(name="track_visit")
@app.route(route="track")
def track_visit(req: func.HttpRequest) -> func.HttpResponse:
    try:
        visit = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        }

        return func.HttpResponse("Site visit recorded", status_code=200)
    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)