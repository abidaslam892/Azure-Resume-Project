import azure.functions as func
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)

# Simple function using traditional method
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    return func.HttpResponse(
        json.dumps({
            "status": "success",
            "message": "Simple function is working!",
            "timestamp": datetime.utcnow().isoformat()
        }),
        status_code=200,
        headers={
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        }
    )