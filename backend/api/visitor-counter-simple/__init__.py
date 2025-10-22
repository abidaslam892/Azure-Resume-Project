import azure.functions as func
import json
import logging
from datetime import datetime, timezone

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple in-memory counter for testing (not persistent but works)
counter_state = {"count": 0}

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Simple visitor counter without database dependency"""
    try:
        logger.info(f"Visitor counter request: {req.method}")
        
        if req.method == "POST":
            # Increment counter
            counter_state["count"] += 1
            new_count = counter_state["count"]
            
            logger.info(f"📊 Counter incremented to: {new_count}")
            
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
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type",
                }
            )
        else:
            # Get current count
            current_count = counter_state["count"]
            
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
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type",
                }
            )
            
    except Exception as e:
        logger.error(f"❌ Visitor counter failed: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "success": False,
                "error": "Internal server error",
                "message": f"Failed to process visitor counter request: {str(e)}",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }),
            status_code=500,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            }
        )