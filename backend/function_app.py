import azure.functions as func
import json
import logging
import os
from datetime import datetime, timezone
from azure.data.tables import TableServiceClient, TableEntity
from azure.core.exceptions import ResourceNotFoundError, ServiceRequestError
from azure.core.credentials import AzureKeyCredential
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Azure Function App
app = func.FunctionApp()

class TableStorageManager:
    """
    Manages Azure Table Storage operations for visitor counter
    """
    
    def __init__(self):
        """Initialize Table Storage client and configure table"""
        try:
            # Get connection details from environment variables
            self.account_name = os.environ.get('COSMOS_DB_ACCOUNT_NAME', 'cosmos-resume-1760986821')
            self.account_key = os.environ.get('COSMOS_DB_KEY')
            self.table_name = os.environ.get('COSMOS_DB_TABLE', 'VisitorCounter')
            self.connection_string = os.environ.get('COSMOS_DB_CONNECTION_STRING')
            
            if not self.connection_string and not self.account_key:
                raise ValueError("CosmosDB connection string or account key not found in environment variables")
            
            # Create Table Service Client using connection string (preferred for CosmosDB)
            if self.connection_string:
                self.table_service_client = TableServiceClient.from_connection_string(
                    conn_str=self.connection_string
                )
            else:
                # Fallback to endpoint + key
                account_url = f"https://{self.account_name}.table.cosmos.azure.com/"
                self.table_service_client = TableServiceClient(
                    endpoint=account_url,
                    credential=AzureKeyCredential(self.account_key)
                )
            
            # Get table client
            self.table_client = self.table_service_client.get_table_client(
                table_name=self.table_name
            )
            
            logger.info("Table Storage client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Table Storage client: {str(e)}")
            raise

    def get_visitor_count(self):
        """
        Retrieve current visitor count from Table Storage
        """
        try:
            # Query for the visitor counter entity
            entity = self.table_client.get_entity(
                partition_key="visitor-counter",
                row_key="count"
            )
            
            count = entity.get('Count', 0)
            logger.info(f"Retrieved visitor count: {count}")
            return count
            
        except ResourceNotFoundError:
            logger.info("Visitor counter not found, initializing...")
            return self.initialize_counter()
        except Exception as e:
            logger.error(f"Error retrieving visitor count: {str(e)}")
            # Return 0 instead of raising error for better UX
            return 0

    def increment_visitor_count(self):
        """
        Increment and return the visitor count
        """
        try:
            # Try to get existing counter
            try:
                entity = self.table_client.get_entity(
                    partition_key="visitor-counter",
                    row_key="count"
                )
                current_count = entity.get('Count', 0)
                etag = entity.metadata['etag']
            except ResourceNotFoundError:
                # Counter doesn't exist, start with 0
                current_count = 0
                etag = None
            
            # Increment the count
            new_count = current_count + 1
            
            # Create or update the counter entity
            counter_entity = TableEntity()
            counter_entity['PartitionKey'] = "visitor-counter"
            counter_entity['RowKey'] = "count"
            counter_entity['Count'] = new_count
            counter_entity['LastUpdated'] = datetime.now(timezone.utc)
            counter_entity['Version'] = str(uuid.uuid4())
            
            if etag:
                # Update existing entity
                self.table_client.update_entity(
                    entity=counter_entity,
                    mode="replace"
                )
            else:
                # Create new entity
                self.table_client.create_entity(entity=counter_entity)
            
            logger.info(f"Visitor count incremented to: {new_count}")
            return new_count
            
        except Exception as e:
            logger.error(f"Error incrementing visitor count: {str(e)}")
            # Return current count + 1 as fallback
            current = self.get_visitor_count()
            return current + 1

    def initialize_counter(self):
        """
        Initialize the visitor counter with count 1
        """
        try:
            counter_entity = TableEntity()
            counter_entity['PartitionKey'] = "visitor-counter"
            counter_entity['RowKey'] = "count"
            counter_entity['Count'] = 1
            counter_entity['LastUpdated'] = datetime.now(timezone.utc)
            counter_entity['Version'] = str(uuid.uuid4())
            counter_entity['CreatedAt'] = datetime.now(timezone.utc)
            
            self.table_client.create_entity(entity=counter_entity)
            logger.info("Visitor counter initialized with count: 1")
            return 1
            
        except Exception as e:
            logger.error(f"Error initializing visitor counter: {str(e)}")
            return 1

    def get_visitor_stats(self):
        """
        Get comprehensive visitor statistics
        """
        try:
            entity = self.table_client.get_entity(
                partition_key="visitor-counter",
                row_key="count"
            )
            
            return {
                'count': entity.get('Count', 0),
                'lastUpdated': entity.get('LastUpdated', '').isoformat() if entity.get('LastUpdated') else None,
                'createdAt': entity.get('CreatedAt', '').isoformat() if entity.get('CreatedAt') else None,
                'version': entity.get('Version', ''),
            }
            
        except ResourceNotFoundError:
            return {
                'count': 0,
                'lastUpdated': None,
                'createdAt': None,
                'version': '',
            }
        except Exception as e:
            logger.error(f"Error getting visitor stats: {str(e)}")
            return {
                'count': 0,
                'lastUpdated': None,
                'createdAt': None,
                'version': '',
                'error': str(e)
            }

# Initialize Table Storage Manager
table_manager = None

def get_table_manager():
    """
    Get or create table manager instance
    """
    global table_manager
    if table_manager is None:
        table_manager = TableStorageManager()
    return table_manager

@app.route(route="visitor-counter", methods=["GET", "POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def visitor_counter(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function HTTP trigger for visitor counter
    
    GET: Returns current visitor count
    POST: Increments and returns visitor count
    OPTIONS: CORS preflight support
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
        
        logger.info(f"Visitor counter function triggered via {req.method}")
        
        # Get table manager
        manager = get_table_manager()
        
        if req.method == "GET":
            # Return current count without incrementing
            count = manager.get_visitor_count()
            
            response_data = {
                "success": True,
                "count": count,
                "method": "GET",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "message": "Current visitor count retrieved"
            }
            
        elif req.method == "POST":
            # Increment and return new count
            count = manager.increment_visitor_count()
            
            response_data = {
                "success": True,
                "count": count,
                "method": "POST",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "message": "Visitor count incremented"
            }
            
        else:
            return func.HttpResponse(
                json.dumps({
                    "success": False,
                    "error": f"Method {req.method} not allowed",
                    "allowedMethods": ["GET", "POST", "OPTIONS"]
                }),
                status_code=405,
                headers={
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                }
            )
        
        logger.info(f"Visitor counter response: {response_data}")
        
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
        logger.error(f"Error in visitor counter function: {str(e)}")
        
        error_response = {
            "success": False,
            "error": "Internal server error",
            "message": "Failed to process visitor counter request",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        return func.HttpResponse(
            json.dumps(error_response),
            status_code=500,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            }
        )

@app.route(route="visitor-stats", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def visitor_stats(req: func.HttpRequest) -> func.HttpResponse:
    """
    Get detailed visitor statistics
    """
    try:
        logger.info("Visitor stats function triggered")
        
        manager = get_table_manager()
        stats = manager.get_visitor_stats()
        
        response_data = {
            "success": True,
            "stats": stats,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        return func.HttpResponse(
            json.dumps(response_data),
            status_code=200,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            }
        )
        
    except Exception as e:
        logger.error(f"Error in visitor stats function: {str(e)}")
        
        return func.HttpResponse(
            json.dumps({
                "success": False,
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }),
            status_code=500,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            }
        )

@app.route(route="health", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def health_check(req: func.HttpRequest) -> func.HttpResponse:
    """
    Health check endpoint
    """
    try:
        # Test table connection
        manager = get_table_manager()
        
        health_data = {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": "1.0.0",
            "services": {
                "table_storage": "connected",
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
        logger.error(f"Health check failed: {str(e)}")
        
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
        )# Deployment test Tue Oct 21 01:40:04 AM PKT 2025
