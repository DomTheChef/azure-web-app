import azure.functions as func
import uuid
import json
import os  

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


@app.route(route="debug-conn", methods=["GET"])
def debug_conn(req: func.HttpRequest) -> func.HttpResponse:
    conn_val = os.getenv("CosmosConn")
    if conn_val:
        return func.HttpResponse(
            f"CosmosConn is set. Starts with: {conn_val[:40]}...",
            status_code=200
        )
    else:
        return func.HttpResponse("CosmosConn is NOT set!", status_code=500)
