#!/bin/bash

# ARM Template Deployment Validation Script
echo "🔍 ARM Template Deployment Validation"
echo "======================================"

# Set variables
TEMPLATE_FILE="./arm-template.json"
PARAMETERS_FILE="./arm-parameters.json"
RESOURCE_GROUP="rg-cloud-resume"
DEPLOYMENT_NAME="arm-template-$(date +%Y%m%d-%H%M%S)"

echo ""
echo "📋 Configuration:"
echo "Template: $TEMPLATE_FILE"
echo "Parameters: $PARAMETERS_FILE"
echo "Resource Group: $RESOURCE_GROUP"
echo "Deployment Name: $DEPLOYMENT_NAME"

echo ""
echo "🔍 Step 1: Validating JSON syntax..."
if python3 -m json.tool "$TEMPLATE_FILE" > /dev/null 2>&1; then
    echo "✅ Template JSON syntax is valid"
else
    echo "❌ Template JSON has syntax errors"
    exit 1
fi

if python3 -m json.tool "$PARAMETERS_FILE" > /dev/null 2>&1; then
    echo "✅ Parameters JSON syntax is valid"
else
    echo "❌ Parameters JSON has syntax errors"
    exit 1
fi

echo ""
echo "🔍 Step 2: Validating ARM template with Azure..."
az deployment group validate \
    --resource-group "$RESOURCE_GROUP" \
    --template-file "$TEMPLATE_FILE" \
    --parameters "@$PARAMETERS_FILE" \
    --output table

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ ARM template validation successful!"
    echo ""
    echo "🚀 Ready to deploy! Run the following command:"
    echo "az deployment group create \\"
    echo "  --name $DEPLOYMENT_NAME \\"
    echo "  --resource-group $RESOURCE_GROUP \\"
    echo "  --template-file $TEMPLATE_FILE \\"
    echo "  --parameters @$PARAMETERS_FILE"
else
    echo ""
    echo "❌ ARM template validation failed!"
    echo "Please check the errors above and fix them before deploying."
    exit 1
fi