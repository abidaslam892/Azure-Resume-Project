#!/bin/bash

echo "🔍 Monitoring Azure Resume Deployment"
echo "===================================="

# Function to test endpoints
test_endpoint() {
    local url=$1
    local name=$2
    
    echo "Testing $name..."
    response=$(curl -s -w "HTTPSTATUS:%{http_code}" "$url")
    http_code=$(echo $response | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
    body=$(echo $response | sed -e 's/HTTPSTATUS:.*//g')
    
    if [ "$http_code" -eq "200" ]; then
        echo "✅ $name: SUCCESS (200)"
        if [ ! -z "$body" ]; then
            echo "   Response: $body"
        fi
    elif [ "$http_code" -eq "404" ]; then
        echo "❌ $name: NOT FOUND (404)"
    elif [ "$http_code" -eq "503" ]; then
        echo "⏳ $name: SERVICE UNAVAILABLE (503) - Still deploying..."
    else
        echo "⚠️  $name: HTTP $http_code"
    fi
    echo ""
}

# Function to test website
test_website() {
    echo "Testing main website..."
    response=$(curl -s -L -w "HTTPSTATUS:%{http_code}" "https://abidaslam.online" 2>/dev/null || echo "HTTPSTATUS:000")
    http_code=$(echo $response | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
    
    if [ "$http_code" -eq "200" ]; then
        echo "✅ Website: SUCCESS (200)"
    elif [ "$http_code" -eq "404" ]; then
        echo "❌ Website: NOT FOUND (404)"
    elif [ "$http_code" -eq "000" ]; then
        echo "⚠️  Website: SSL/Connection issues"
    else
        echo "⚠️  Website: HTTP $http_code"
    fi
    echo ""
}

# Wait and monitor
echo "⏳ Waiting for GitHub Actions deployment to complete..."
echo "   - This usually takes 3-5 minutes"
echo "   - You can monitor progress at: https://github.com/abidaslam892/Azure-Resume-Project/actions"
echo ""

# Test every 30 seconds for 10 minutes
for i in {1..20}; do
    echo "🔄 Check #$i ($(date))"
    echo "----------------------------------------"
    
    # Test backend endpoints
    test_endpoint "https://func-resume-1760986821.azurewebsites.net/api/health" "Backend Health"
    test_endpoint "https://func-resume-1760986821.azurewebsites.net/api/visitor-counter" "Visitor Counter"
    
    # Test website
    test_website
    
    # Check if everything is working
    health_status=$(curl -s -w "%{http_code}" "https://func-resume-1760986821.azurewebsites.net/api/health" -o /dev/null)
    
    if [ "$health_status" -eq "200" ]; then
        echo "🎉 SUCCESS! Backend is now responding!"
        echo ""
        echo "✅ Your Azure Resume Challenge is now working:"
        echo "   🌐 Website: https://abidaslam.online"
        echo "   🔧 API Health: https://func-resume-1760986821.azurewebsites.net/api/health"
        echo "   📊 Visitor Counter: https://func-resume-1760986821.azurewebsites.net/api/visitor-counter"
        echo ""
        echo "🚀 GitHub Actions deployment completed successfully!"
        exit 0
    fi
    
    if [ $i -lt 20 ]; then
        echo "⏳ Still deploying... checking again in 30 seconds"
        echo ""
        sleep 30
    fi
done

echo "⚠️  Deployment is taking longer than expected."
echo "   Please check the GitHub Actions workflow for any issues:"
echo "   https://github.com/abidaslam892/Azure-Resume-Project/actions"