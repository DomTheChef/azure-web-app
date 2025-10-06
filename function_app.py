import azure.functions as func


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="track", methods=["GET", "POST"])
def track(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("OK", status_code=200)