import os
import json
from urllib import response
from aws_lambda_powertools.event_handler.api_gateway import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Response

app = APIGatewayRestResolver()

@app.get("/contents")
def get_contents():

    response = {
        "url": os.environ["URL"]
    }

    return Response(
        status_code=200,
        content_type="application/json",
        body=json.dumps(response)
    )


def handler(event, context):
    return app.resolve(event, context)