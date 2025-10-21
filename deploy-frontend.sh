#!/bin/bash

# Azure Resume Frontend Deployment Script (Secure Version)
# Uses environment variables or Azure CLI to get credentials

set -e

echo "🚀 Azure Resume Frontend Deployment"
echo "=================================="

# Check if Azure CLI is logged in
if ! az account show > /dev/null 2>&1; then
    echo "❌ Please login to Azure CLI first:"
    echo "   az login"
    exit 1
fi

# Storage account details
STORAGE_ACCOUNT="storresume1760986821"
CONTAINER_NAME="\$web"
RESOURCE_GROUP="rg-cloud-resume"

# Get storage account key if not provided via environment
if [ -z "$AZURE_STORAGE_KEY" ]; then
    echo "🔑 Getting storage account key from Azure..."
    ACCOUNT_KEY=$(az storage account keys list --account-name $STORAGE_ACCOUNT --resource-group $RESOURCE_GROUP --query "[0].value" -o tsv)
    if [ -z "$ACCOUNT_KEY" ]; then
        echo "❌ Failed to retrieve storage account key"
        exit 1
    fi
else
    echo "🔑 Using provided storage account key from environment"
    ACCOUNT_KEY="$AZURE_STORAGE_KEY"
fi

echo "📁 Uploading files to Azure Storage..."

# Upload HTML file
echo "  📄 Uploading index.html..."
az storage blob upload \
    --account-name $STORAGE_ACCOUNT \
    --container-name $CONTAINER_NAME \
    --name index.html \
    --file index.html \
    --content-type 'text/html' \
    --account-key $ACCOUNT_KEY \
    --overwrite

# Upload JavaScript file
echo "  📜 Uploading script.js..."
az storage blob upload \
    --account-name $STORAGE_ACCOUNT \
    --container-name $CONTAINER_NAME \
    --name script.js \
    --file script.js \
    --content-type 'application/javascript' \
    --account-key $ACCOUNT_KEY \
    --overwrite

# Upload CSS files
echo "  🎨 Uploading styles.css..."
az storage blob upload \
    --account-name $STORAGE_ACCOUNT \
    --container-name $CONTAINER_NAME \
    --name styles.css \
    --file styles.css \
    --content-type 'text/css' \
    --account-key $ACCOUNT_KEY \
    --overwrite

echo "  🎨 Uploading visitor-counter-styles.css..."
az storage blob upload \
    --account-name $STORAGE_ACCOUNT \
    --container-name $CONTAINER_NAME \
    --name visitor-counter-styles.css \
    --file visitor-counter-styles.css \
    --content-type 'text/css' \
    --account-key $ACCOUNT_KEY \
    --overwrite

# Upload images
echo "  🖼️  Uploading images..."
az storage blob upload \
    --account-name $STORAGE_ACCOUNT \
    --container-name $CONTAINER_NAME \
    --name images/Screenshot_1.png \
    --file images/Screenshot_1.png \
    --content-type 'image/png' \
    --account-key $ACCOUNT_KEY \
    --overwrite

az storage blob upload \
    --account-name $STORAGE_ACCOUNT \
    --container-name $CONTAINER_NAME \
    --name images/image.jpg \
    --file images/image.jpg \
    --content-type 'image/jpeg' \
    --account-key $ACCOUNT_KEY \
    --overwrite

echo ""
echo "✅ Frontend deployment completed successfully!"
echo ""
echo "🌐 Access your resume at:"
echo "   • Storage URL: https://$STORAGE_ACCOUNT.z13.web.core.windows.net"
echo "   • Custom Domain: https://www.abidaslam.online"
echo "   • CDN: https://resume-endpoint-gmd7e5g9f8c6gqgs.z01.azurefd.net/"
echo ""
echo "💡 Usage Options:"
echo "   • Direct: ./deploy-frontend.sh"
echo "   • With key: AZURE_STORAGE_KEY='your-key' ./deploy-frontend.sh"
echo ""