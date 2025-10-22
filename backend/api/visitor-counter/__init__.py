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

def get_visitor_count():
    """Get current visitor count"""
    try:
        client = get_table_client()
        entity = client.get_entity(partition_key="visitor", row_key="counter")
        return entity.get('Count', 0)
    except ResourceNotFoundError:
        return 0
    except Exception as e:
        logger.error(f"Error getting count: {str(e)}")
        return 0

def increment_visitor_count():
    """Increment visitor count"""
    try:
        client = get_table_client()
        
        try:
            entity = client.get_entity(partition_key="visitor", row_key="counter")
            current_count = entity.get('Count', 0)
            new_count = current_count + 1
            entity['Count'] = new_count
            entity['LastUpdated'] = datetime.now(timezone.utc)
            client.update_entity(entity)
            return new_count
        except ResourceNotFoundError:
            entity = TableEntity()
            entity['PartitionKey'] = "visitor"
            entity['RowKey'] = "counter"
            entity['Count'] = 1
            entity['LastUpdated'] = datetime.now(timezone.utc)
            client.create_entity(entity)
            return 1
    except Exception as e:
        logger.error(f"Error incrementing count: {str(e)}")
        return 0

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Visitor counter endpoint"""
    try:
        logger.info(f"Visitor counter request: {req.method}")
        
        if req.method == "POST":
            # Increment counter
            new_count = increment_visitor_count()
            return func.HttpResponse(
                json.dumps({
                    "success": True,
                    "count": new_count,
                    "message": f"Visitor count updated to {new_count}",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }),
                status_code=200,
                headers={
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                }
            )
        else:
            # Get current count
            current_count = get_visitor_count()
            return func.HttpResponse(
                json.dumps({
                    "success": True,
                    "count": current_count,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }),
                status_code=200,
                headers={
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                }
            )
            
    except Exception as e:
        logger.error(f"❌ Visitor counter failed: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "success": False,
                "error": "Internal server error",
                "message": "Failed to process visitor counter request",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }),
            status_code=500,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            }
        )