import azure.functions as func
import uuid
import json
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.cosmos_db_output(
    arg_name="doc",
    database_name="VisitCount",
    container_name="Visitors",
    connection="CosmosConn"
)
@app.route(route="track", methods=["GET"])
def track(req: func.HttpRequest, doc: func.Out[str]) -> func.HttpResponse:
    try:
        item = {
            "id": str(uuid.uuid4()),
            "note": "Prod test entry"
        }
        doc.set(json.dumps(item))
        return func.HttpResponse("Inserted into Cosmos!", status_code=200)
    except Exception as e:
        logging.error(f"Cosmos DB binding failed: {e}")
        return func.HttpResponse(f"Cosmos DB binding failed: {e}", status_code=500)
