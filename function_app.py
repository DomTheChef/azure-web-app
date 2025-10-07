import azure.functions as func
import uuid
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.cosmos_db_output(
    arg_name="doc",
    database_name="VisitCount",
    container_name="Visitors",
    connection="CosmosDBConnection"
)
@app.route(route="track", methods=["GET", "POST"])
def track(req: func.HttpRequest, doc: func.Out[str]) -> func.HttpResponse:
    try:
        item = {
            "id": str(uuid.uuid4()),
            "note": "testEntry"
        }

        doc.set(json.dumps(item))

        return func.HttpResponse("Ok", status_code=200)
    except Exception as e:
        return func.HttpResponse(f"CosmosDB error: {e}", status_code=500)
