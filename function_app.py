import azure.functions as func
import uuid
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.cosmos_db_output(
    arg_name="doc",
    database_name="VisitCount",       
    container_name="Visitors",     
    connection="CosmosConn"          
)
@app.route(route="track", methods=["GET"])
def track(req: func.HttpRequest, doc: func.Out[str]) -> func.HttpResponse:

    item = {
        "id": str(uuid.uuid4()),     
        "note": "Test entry"
    }

    doc.set(json.dumps(item))

    return func.HttpResponse("Inserted into Cosmos!", status_code=200)
