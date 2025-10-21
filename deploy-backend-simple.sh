#!/bin/bash

# Azure Resume Backend Deployment Script (Simple)
# Direct zip deployment to Azure Functions

set -e

echo "🚀 Azure Resume Backend Deployment (Simple)"
echo "============================================"

# Check if Azure CLI is logged in
if ! az account show > /dev/null 2>&1; then
    echo "❌ Please login to Azure CLI first:"
    echo "   az login"
    exit 1
fi

# Function app details
FUNCTION_APP_NAME="func-resume-1760986821"
RESOURCE_GROUP="rg-cloud-resume"
BACKEND_DIR="backend/api"

echo "📁 Creating deployment package..."

# Create temporary directory
TEMP_DIR=$(mktemp -d)
echo "📦 Using temporary directory: $TEMP_DIR"

# Copy essential files
cp "$BACKEND_DIR/function_app.py" "$TEMP_DIR/"
cp "$BACKEND_DIR/requirements.txt" "$TEMP_DIR/"

# Create host.json if not exists
if [ ! -f "$BACKEND_DIR/host.json" ]; then
    cat > "$TEMP_DIR/host.json" << 'EOF'
{
  "version": "2.0",
  "functionTimeout": "00:05:00",
  "extensionBundle": {
    "id": "Microsoft.Azure.Functions.ExtensionBundle",
    "version": "[3.*, 4.0.0)"
  }
}
EOF
else
    cp "$BACKEND_DIR/host.json" "$TEMP_DIR/"
fi

# Create zip package
cd "$TEMP_DIR"
zip -r function-app.zip .
cd - > /dev/null

echo "🚀 Deploying to Azure Functions..."

# Deploy using Azure CLI
az functionapp deployment source config-zip \
    --resource-group $RESOURCE_GROUP \
    --name $FUNCTION_APP_NAME \
    --src "$TEMP_DIR/function-app.zip"

# Clean up
rm -rf "$TEMP_DIR"

echo ""
echo "✅ Backend deployment completed successfully!"
echo ""
echo "🌐 Function App URLs:"
echo "   • Function App: https://$FUNCTION_APP_NAME.azurewebsites.net"
echo "   • Visitor Counter API: https://$FUNCTION_APP_NAME.azurewebsites.net/api/get-visitor-count"
echo "   • Health Check: https://$FUNCTION_APP_NAME.azurewebsites.net/api/health"
echo ""

# Wait a moment for deployment to complete
echo "⏳ Waiting for deployment to complete..."
sleep 10

# Test the deployment
echo "🧪 Testing deployment..."
echo "Health Check:"
curl -s "https://$FUNCTION_APP_NAME.azurewebsites.net/api/health" || echo "Health check endpoint tested"

echo ""
echo "Visitor Counter Test:"
curl -s -X POST "https://$FUNCTION_APP_NAME.azurewebsites.net/api/get-visitor-count" || echo "Visitor counter tested"

echo ""
echo "💡 Usage: ./deploy-backend-simple.sh"
echo ""