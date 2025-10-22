import azure.functions as func
import json
import logging
import os
from datetime import datetime, timezone
from azure.data.tables import TableServiceClient, TableEntity
from azure.core.exceptions import ResourceNotFoundError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_table_client():
    """Initialize and return table client for Azure Storage Tables"""
    try:
        connection_string = os.environ.get('AzureWebJobsStorage')
        
        if not connection_string:
            raise ValueError("AzureWebJobsStorage connection string not found")
        
        table_service = TableServiceClient.from_connection_string(connection_string)
        table_name = "VisitorCounter"
        table_client = table_service.get_table_client(table_name)
        
        try:
            table_client.create_table()
            logger.info(f"📊 Table {table_name} created or already exists")
        except Exception as e:
            logger.info(f"📊 Table {table_name} already exists: {str(e)}")
        
        return table_client
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize table client: {str(e)}")
        raise

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Health check endpoint"""
    try:
        logger.info("🏥 Health check requested")
        
        # Basic health response
        health_data = {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": "1.0.0",
            "runtime": "Python 3.11",
            "services": {
                "function_app": "running"
            }
        }
        
        return func.HttpResponse(
            json.dumps(health_data),
            status_code=200,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            }
        )
        
    except Exception as e:
        logger.error(f"❌ Health check failed: {str(e)}")
        
        return func.HttpResponse(
            json.dumps({
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }),
            status_code=503,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            }
        )