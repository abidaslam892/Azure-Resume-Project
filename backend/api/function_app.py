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

# Initialize the Azure Function App - Extension Bundle Fix Oct 23, 2025
app = func.FunctionApp()

# Simple test endpoint to verify deployment
@app.route(route="test", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def test_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    """Simple test endpoint to verify deployment is working"""
    return func.HttpResponse(
        json.dumps({
            "message": "Deployment successful!",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": "extension-bundle-fix"
        }),
        status_code=200,
        mimetype="application/json",
        headers={"Access-Control-Allow-Origin": "*"}
    )

def get_table_client():
    """Initialize and return table client for Azure Storage Tables"""
    try:
        # Use AzureWebJobsStorage which contains the storage account connection
        connection_string = os.environ.get('AzureWebJobsStorage')
        
        if not connection_string:
            raise ValueError("AzureWebJobsStorage connection string not found")
        
        # Create table service client
        table_service = TableServiceClient.from_connection_string(connection_string)
        table_name = "VisitorCounter"
        
        # Get table client and create table if it doesn't exist
        table_client = table_service.get_table_client(table_name)
        
        try:
            table_client.create_table()
            logger.info(f"📊 Table {table_name} created or already exists")
        except Exception as e:
            logger.info(f"📊 Table {table_name} already exists: {str(e)}")
        
        logger.info("✅ Table client initialized successfully")
        return table_client
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize table client: {str(e)}")
        raise

def get_visitor_count():
    """Get current visitor count from Azure Storage Table"""
    try:
        client = get_table_client()
        entity = client.get_entity(partition_key="visitor", row_key="counter")
        count = entity.get('Count', 0)
        logger.info(f"📊 Retrieved visitor count: {count}")
        return count
    except ResourceNotFoundError:
        logger.info("📊 No existing counter found, initializing to 0")
        # Initialize the counter
        try:
            client = get_table_client()
            entity = TableEntity()
            entity['PartitionKey'] = "visitor"
            entity['RowKey'] = "counter"
            entity['Count'] = 0
            entity['LastUpdated'] = datetime.now(timezone.utc)
            client.create_entity(entity)
            logger.info("📊 Counter initialized to 0")
        except Exception as e:
            logger.info(f"📊 Counter may already exist: {e}")
        return 0
    except Exception as e:
        logger.error(f"❌ Error getting visitor count: {str(e)}")
        return 0

def increment_visitor_count():
    """Increment visitor count in Azure Storage Table"""
    try:
        client = get_table_client()
        
        # Get current count
        current_count = get_visitor_count()
        new_count = current_count + 1
        
        # Create or update entity
        entity = TableEntity()
        entity['PartitionKey'] = "visitor"
        entity['RowKey'] = "counter"
        entity['Count'] = new_count
        entity['LastUpdated'] = datetime.now(timezone.utc)
        
        # Upsert the entity (create or replace)
        client.upsert_entity(entity, mode="replace")
        
        logger.info(f"📈 Visitor count incremented to: {new_count}")
        return new_count
        
    except Exception as e:
        logger.error(f"❌ Error incrementing visitor count: {str(e)}")
        return 0

@app.route(route="visitor-counter", methods=["GET", "POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def visitor_counter(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function HTTP trigger for visitor counter with Azure Storage Tables
    """
    
    try:
        # Handle CORS preflight requests
        if req.method == "OPTIONS":
            return func.HttpResponse(
                "",
                status_code=200,
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type, Authorization",
                    "Access-Control-Max-Age": "86400",
                }
            )
        
        logger.info(f"🚀 Visitor counter triggered via {req.method}")
        
        if req.method == "POST":
            # Increment and return new count
            count = increment_visitor_count()
            message = "Visitor count incremented successfully"
            logger.info(f"📈 POST request - count incremented to: {count}")
        else:
            # GET - return current count without incrementing
            count = get_visitor_count()
            message = "Current visitor count retrieved"
            logger.info(f"📊 GET request - current count: {count}")
        
        response_data = {
            "success": True,
            "count": count,
            "method": req.method,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": message,
            "source": "Azure Storage Tables"
        }
        
        logger.info(f"✅ Returning response: count={count}, method={req.method}")
        
        return func.HttpResponse(
            json.dumps(response_data),
            status_code=200,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
        
    except Exception as e:
        logger.error(f"❌ Error in visitor counter function: {str(e)}")
        
        error_response = {
            "success": False,
            "error": "Internal server error",
            "message": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": "Azure Storage Tables"
        }
        
        return func.HttpResponse(
            json.dumps(error_response),
            status_code=500,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            }
        )

@app.route(route="health", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def health_check(req: func.HttpRequest) -> func.HttpResponse:
    """
    Health check endpoint - simplified for deployment testing
    """
    try:
        logger.info("🏥 Health check requested")
        
        # Simple health response without database dependency for now
        health_data = {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": "2.1-extension-bundle-fix",
            "runtime": "Python 3.11",
            "message": "Backend is running successfully"
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
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "runtime": "Python 3.11"
            }),
            status_code=503,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            }
        )