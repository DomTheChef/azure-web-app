import azure.functions as func
import uuid

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="track", methods=["GET", "POST"])
@app.cosmos_db_output(
    arg_name="doc",
    database_name="VisitCount",
    container_name="Visitors",
    connection="CosmosDBConnection"   
)
def track(req: func.HttpRequest, doc: func.Out[dict]) -> func.HttpResponse:
    try:
        item = {
            "id": str(uuid.uuid4()),   
            "note": "testEntry"
        }
        doc.set(item)

        return func.HttpResponse("Ok", status_code=200)
    except Exception as e:
        return func.HttpResponse(f"CosmosDB error: {e}", status_code=500)
