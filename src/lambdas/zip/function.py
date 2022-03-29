import os
import requests
import json
import zipfile
from aws_lambda_powertools.event_handler.api_gateway import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Response

app = APIGatewayRestResolver()


def download_file(url):
    """
    Download the file to the /tmp directory and return the file name.
    """
    zip_filename = f"/tmp/{url.split('/')[-1]}"
    
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(zip_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)

    return zip_filename

def extract_file(filename):
    """
    Extract the zip file to the /tmp directory.
    """
    with zipfile.ZipFile(filename, "r") as z:
        z.extractall("/tmp/")

def get_file_contents(filename):
    """
    Get the contents of yml file from extracted zip.
    """
    data = None
    with open(filename[:-4] + "/resource/descriptor.yml") as f:
        data = f.read()
    return data

@app.get("/contents")
def get_contents():
    """
    Get the contents of a yaml file extracted from a zip file.
    """
    file = download_file(os.environ["URL"])
    extract_file(file)
    data = get_file_contents(file)   
    
    response = {
        "data": data
    }

    return Response(
        status_code=200,
        content_type="application/json",
        body=json.dumps(response)
    )


def handler(event, context):
    return app.resolve(event, context)