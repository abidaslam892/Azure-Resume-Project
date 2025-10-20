# 🚀 Deployment Guide - Azure Resume Project

## 📋 Prerequisites

Before deploying this project, ensure you have:

- ✅ **Azure Subscription** with appropriate permissions
- ✅ **GitHub Account** for CI/CD integration  
- ✅ **Azure CLI** installed and configured
- ✅ **Git** for source code management

## 🏗️ Infrastructure Setup

### 1. Azure Resource Group
```bash
az group create --name rg-cloud-resume --location eastus
```

### 2. Storage Account (Static Website)
```bash
az storage account create \
  --name storresume$(date +%s) \
  --resource-group rg-cloud-resume \
  --location eastus \
  --sku Standard_LRS \
  --kind StorageV2

az storage blob service-properties update \
  --account-name <STORAGE_ACCOUNT_NAME> \
  --static-website \
  --index-document index.html \
  --404-document 404.html
```

### 3. CosmosDB Account  
```bash
az cosmosdb create \
  --name cosmos-resume-$(date +%s) \
  --resource-group rg-cloud-resume \
  --capabilities EnableTable \
  --locations regionName=eastus
```

### 4. Azure Functions App
```bash
az functionapp create \
  --name func-resume-$(date +%s) \
  --resource-group rg-cloud-resume \
  --storage-account <STORAGE_ACCOUNT_NAME> \
  --consumption-plan-location eastus \
  --runtime python \
  --runtime-version 3.9 \
  --functions-version 4
```

### 5. Azure Front Door CDN
```bash
az afd profile create \
  --profile-name afd-resume-profile \
  --resource-group rg-cloud-resume \
  --sku Standard_AzureFrontDoor

az afd endpoint create \
  --profile-name afd-resume-profile \
  --resource-group rg-cloud-resume \
  --endpoint-name resume-endpoint-$(date +%s) \
  --origin-host-header <STORAGE_ACCOUNT_NAME>.z13.web.core.windows.net
```

## 🔐 Security Configuration

### 1. Create Service Principal
```bash
az ad sp create-for-rbac \
  --name "github-actions-resume-project" \
  --role "Contributor" \
  --scopes "/subscriptions/$(az account show --query id -o tsv)/resourceGroups/rg-cloud-resume" \
  --json-auth
```

### 2. Configure GitHub Secrets
Add the following secrets to your GitHub repository:

| Secret Name | Description | Value Source |
|-------------|-------------|--------------|
| `AZURE_CREDENTIALS` | Service Principal JSON | Output from step 1 |

## 📦 Repository Setup

### 1. Clone Repository
```bash
git clone https://github.com/abidaslam892/Azure-Resume-Project.git
cd Azure-Resume-Project
```

### 2. Update Configuration
Update the following files with your resource names:
- `.github/workflows/frontend.yml` - Storage account name
- `.github/workflows/backend.yml` - Function app name
- `backend/api/function_app.py` - CosmosDB configuration

### 3. Deploy Code
```bash
# Trigger CI/CD pipeline
git add .
git commit -m "Deploy to Azure infrastructure"
git push origin main
```

## 🔄 CI/CD Pipeline

### Frontend Workflow
1. **Code Validation**: HTML, CSS, JavaScript syntax checking
2. **Azure Authentication**: Service principal login
3. **Asset Deployment**: Upload files to Azure Storage
4. **CDN Cache Purge**: Invalidate cached content
5. **Health Check**: Verify deployment success

### Backend Workflow  
1. **Dependency Installation**: Python packages and requirements
2. **Code Testing**: Unit tests and integration tests
3. **Azure Authentication**: Service principal login
4. **Function Deployment**: Deploy to Azure Functions
5. **Configuration**: Environment variables and app settings
6. **API Testing**: Endpoint validation and health checks

## 🧪 Testing & Validation

### Local Testing
```bash
# Frontend validation
cd frontend
python -m http.server 8000

# Backend testing (requires Azure credentials)
cd backend
python -m pytest tests/ -v
```

### Production Testing
```bash
# Test website
curl -I https://your-cdn-endpoint.azurefd.net/

# Test API
curl https://your-function-app.azurewebsites.net/api/visitor-counter
```

## 📊 Monitoring & Maintenance

### Application Insights
- **Performance Metrics**: Response times and throughput
- **Error Tracking**: Exception logging and alerting
- **User Analytics**: Traffic patterns and user behavior
- **Custom Metrics**: Business-specific measurements

### Health Checks
- **Website Availability**: Uptime monitoring via Azure Monitor
- **API Functionality**: Function app health and response validation
- **Database Connectivity**: CosmosDB connection and query performance
- **CDN Performance**: Cache hit rates and edge location metrics

### Cost Management
- **Budget Alerts**: Automated notifications for cost thresholds
- **Resource Optimization**: Right-sizing recommendations
- **Usage Analysis**: Monthly cost breakdown and trending
- **Reserved Instances**: Cost savings for long-term usage

## 🔧 Troubleshooting

### Common Issues

#### Deployment Failures
```bash
# Check Azure CLI authentication
az account show

# Verify resource group exists
az group show --name rg-cloud-resume

# Check GitHub Actions logs
# Navigate to repository Actions tab
```

#### Function App Issues
```bash
# Check function app logs
az functionapp log tail --name <FUNCTION_APP_NAME> --resource-group rg-cloud-resume

# Verify environment variables
az functionapp config appsettings list --name <FUNCTION_APP_NAME> --resource-group rg-cloud-resume
```

#### CDN/DNS Issues
```bash
# Check Front Door status
az afd profile show --profile-name afd-resume-profile --resource-group rg-cloud-resume

# Purge CDN cache manually
az afd endpoint purge --profile-name afd-resume-profile --endpoint-name <ENDPOINT_NAME> --resource-group rg-cloud-resume --content-paths "/*"
```

### Support Resources
- **Azure Documentation**: https://docs.microsoft.com/azure/
- **GitHub Actions Help**: https://docs.github.com/actions
- **Azure Support**: https://azure.microsoft.com/support/
- **Community Forums**: https://stackoverflow.com/questions/tagged/azure

## 🎯 Production Checklist

Before going live, verify:

- [ ] **SSL Certificate**: HTTPS working correctly
- [ ] **Custom Domain**: DNS properly configured  
- [ ] **Security Headers**: CSP, HSTS, and other protections
- [ ] **Performance**: Page load times under 3 seconds
- [ ] **Accessibility**: WCAG compliance and screen reader support
- [ ] **SEO**: Meta tags, structured data, and sitemap
- [ ] **Analytics**: Tracking and monitoring configured
- [ ] **Backup**: Data backup and disaster recovery plan

---

**📞 Support Contact**: abidaslam.123@gmail.com  
**📖 Documentation**: See project README and individual service docs  
**🐛 Issues**: Report via GitHub Issues tab