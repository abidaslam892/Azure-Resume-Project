#!/bin/bash

# Azure Resume Backend Deployment Script
# Bypasses GitHub Actions for direct deployment

set -e

echo "🚀 Azure Resume Backend Deployment"
echo "=================================="

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

# Check if backend directory exists
if [ ! -d "$BACKEND_DIR" ]; then
    echo "❌ Backend directory not found: $BACKEND_DIR"
    exit 1
fi

# Check if required files exist
if [ ! -f "$BACKEND_DIR/function_app.py" ]; then
    echo "❌ function_app.py not found in $BACKEND_DIR"
    exit 1
fi

if [ ! -f "$BACKEND_DIR/requirements.txt" ]; then
    echo "❌ requirements.txt not found in $BACKEND_DIR"
    exit 1
fi

echo "📁 Preparing deployment package..."

# Create temporary deployment directory
DEPLOY_DIR="$(mktemp -d)"
echo "📦 Using temporary directory: $DEPLOY_DIR"

# Copy files to deployment directory
cp "$BACKEND_DIR/function_app.py" "$DEPLOY_DIR/"
cp "$BACKEND_DIR/requirements.txt" "$DEPLOY_DIR/"

# Copy host.json if it exists
if [ -f "$BACKEND_DIR/host.json" ]; then
    cp "$BACKEND_DIR/host.json" "$DEPLOY_DIR/"
else
    # Create a basic host.json
    cat > "$DEPLOY_DIR/host.json" << EOF
{
  "version": "2.0",
  "logging": {
    "applicationInsights": {
      "samplingSettings": {
        "isEnabled": true,
        "excludedTypes": "Request"
      }
    }
  },
  "extensionBundle": {
    "id": "Microsoft.Azure.Functions.ExtensionBundle",
    "version": "[2.*, 3.0.0)"
  },
  "functionTimeout": "00:05:00"
}
EOF
fi

# Check if Azure Functions Core Tools is installed
if ! command -v func &> /dev/null; then
    echo "🔧 Installing Azure Functions Core Tools..."
    curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
    sudo mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg
    sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/microsoft-ubuntu-$(lsb_release -cs)-prod $(lsb_release -cs) main" > /etc/apt/sources.list.d/dotnetdev.list'
    sudo apt-get update
    sudo apt-get install azure-functions-core-tools-4
fi

echo "🚀 Deploying to Azure Functions..."

# Navigate to deployment directory
cd "$DEPLOY_DIR"

# Deploy using Azure Functions Core Tools
func azure functionapp publish $FUNCTION_APP_NAME --python

# Clean up
cd - > /dev/null
rm -rf "$DEPLOY_DIR"

echo ""
echo "✅ Backend deployment completed successfully!"
echo ""
echo "🌐 Function App URLs:"
echo "   • Function App: https://$FUNCTION_APP_NAME.azurewebsites.net"
echo "   • Visitor Counter API: https://$FUNCTION_APP_NAME.azurewebsites.net/api/get-visitor-count"
echo "   • Health Check: https://$FUNCTION_APP_NAME.azurewebsites.net/api/health"
echo ""

# Test the deployment
echo "🧪 Testing deployment..."
echo "Health Check:"
curl -s "https://$FUNCTION_APP_NAME.azurewebsites.net/api/health" | jq . || echo "Health check response received"

echo ""
echo "Visitor Counter Test:"
curl -s -X POST "https://$FUNCTION_APP_NAME.azurewebsites.net/api/get-visitor-count" | jq . || echo "Visitor counter response received"

echo ""
echo "💡 Usage: ./deploy-backend.sh"
echo ""