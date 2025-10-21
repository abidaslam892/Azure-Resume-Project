# Azure Cloud Resume Challenge

[![Frontend CI/CD](https://github.com/abidaslam892/Azure-Resume-Project/actions/workflows/frontend.yml/badge.svg)](https://github.com/abidaslam892/Azure-Resume-Project/actions/workflows/frontend.yml)
[![Backend CI/CD](https://github.com/abidaslam892/Azure-Resume-Project/actions/workflows/backend.yml/badge.svg)](https://github.com/abidaslam892/Azure-Resume-Project/actions/workflows/backend.yml)

🌐 **Live Website**: [https://www.abidaslam.online](https://www.abidaslam.online)

A complete implementation of the [Cloud Resume Challenge](https://cloudresumechallenge.dev/docs/the-challenge/azure/) using Azure services with modern CI/CD practices.

## 🏗️ Complete Architecture

```
                    🌐 Internet Traffic
                           │
                           ▼
   ┌─────────────────────────────────────────────────────┐
   │                Azure Front Door                     │
   │   🔒 SSL/TLS    🌍 Global CDN    ⚡ Load Balancing  │
   │   • Custom Domain: abidaslam.online                 │
   │   • Auto SSL Certificate                            │
   │   • DDoS Protection                                 │
   └─────────────────┬───────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┏━━━━━━━━━━━━━━━━━━━┓         ┏━━━━━━━━━━━━━━━━━━━┓
┃   FRONTEND       ┃         ┃    BACKEND       ┃
┃                  ┃         ┃                  ┃
┃ Azure Storage    ┃         ┃ Azure Functions  ┃
┃ Static Websites  ┃         ┃ (Python 3.11)   ┃
┃                  ┃         ┃                  ┃
┃ • index.html     ┃    ────▶┃ • GET /health    ┃
┃ • script.js      ┃ API Call┃ • POST /get-     ┃
┃ • styles.css     ┃ (CORS)  ┃   visitor-count  ┃
┃ • images/        ┃         ┃                  ┃
┗━━━━━━━━━━━━━━━━━━━┛         ┗━━━━━━━━━━━━━━━━━━━┛
                                      │
                                      │ Persists Data
                                      ▼
                        ┏━━━━━━━━━━━━━━━━━━━━━━━┓
                        ┃   STORAGE LAYER     ┃
                        ┃                     ┃
                        ┃ Azure Storage Tables┃
                        ┃                     ┃
                        ┃ Table: VisitorCount ┃
                        ┃ PartitionKey: "main"┃
                        ┃ RowKey: "counter"   ┃
                        ┃ Count: [INTEGER]    ┃
                        ┗━━━━━━━━━━━━━━━━━━━━━━━┛

╔══════════════════════════════════════════════════════════════╗
║                      CI/CD PIPELINE                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  GitHub Repository                                           ║
║  │                                                           ║
║  ├── .github/workflows/                                      ║
║  │   ├── frontend.yml  ──────────▶ Azure Storage Deploy     ║
║  │   └── backend.yml   ──────────▶ Azure Functions Deploy  ║
║  │                                                           ║
║  ├── Triggers on:                                           ║
║  │   • Push to main/master                                  ║
║  │   • Manual workflow_dispatch                             ║
║  │                                                           ║
║  └── Secrets Used:                                          ║
║      • AZURE_STORAGE_CONNECTION_STRING                      ║
║      • AZURE_FUNCTIONAPP_PUBLISH_PROFILE                    ║
╚══════════════════════════════════════════════════════════════╝
```

## 🔄 Data Flow

```
┌─────────────┐    1. Page Load    ┌─────────────────┐
│   Browser   ├──────────────────▶│  Static Website │
│             │◀──────────────────┤  (Azure Storage)│
└─────────────┘   2. HTML/CSS/JS   └─────────────────┘
       │
       │ 3. JavaScript API Call
       │    fetch('/api/get-visitor-count')
       ▼
┌─────────────┐    4. HTTP POST    ┌─────────────────┐
│  JavaScript ├──────────────────▶│ Azure Functions │
│             │◀──────────────────┤   (Python API)  │
└─────────────┘   5. JSON Response └─────────────────┘
                     {"count": 1234}        │
                                            │ 6. Read/Write
                                            ▼
                                  ┌─────────────────┐
                                  │ Storage Tables  │
                                  │ Counter: 1234   │
                                  └─────────────────┘
```

## ✨ Features

- **📱 Responsive Design**: Mobile-first responsive layout
- **🔒 HTTPS**: SSL certificate auto-managed by Azure Front Door
- **🌍 Global CDN**: Fast loading worldwide via Azure Front Door
- **📊 Real Visitor Counter**: Persistent count stored in Azure Storage Tables
- **🚀 CI/CD Pipeline**: Automated deployment via GitHub Actions
- **🛡️ Security**: No hardcoded credentials, environment-based configuration
- **🎯 Custom Domain**: Professional domain with automatic SSL

## 🛠️ Tech Stack

### Frontend
- **HTML5/CSS3**: Modern semantic markup and styling
- **Vanilla JavaScript**: Real-time visitor counter with API integration
- **Azure Storage**: Static website hosting ($web container)
- **Azure Front Door**: Global CDN and SSL termination

### Backend
- **Azure Functions**: Serverless Python 3.11 runtime
- **Azure Storage Tables**: NoSQL database for visitor counter
- **CORS Enabled**: Cross-origin requests support
- **Health Monitoring**: Dedicated health check endpoint

### DevOps
- **GitHub Actions**: Automated CI/CD pipelines
- **Infrastructure as Code**: Azure resource management
- **Security**: Environment-based secrets management

## 🚀 Local Development

### Prerequisites
- Python 3.11+
- Azure Functions Core Tools
- Azure CLI
- Git

### Setup
```bash
# Clone repository
git clone https://github.com/abidaslam892/Azure-Resume-Project.git
cd Azure-Resume-Project

# Backend setup
cd backend/api
pip install -r requirements.txt

# Test locally (requires Azure storage connection)
func start
```

### Environment Variables
```bash
# Required for Azure Functions
AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;..."
```

## 📦 Deployment

### Automated Deployment
Deployments happen automatically via GitHub Actions:

- **Frontend**: Triggers on changes to `*.html`, `*.css`, `*.js`, `images/**`
- **Backend**: Triggers on changes to `backend/**`

### Required GitHub Secrets
```bash
AZURE_STORAGE_CONNECTION_STRING    # For blob uploads
AZURE_FUNCTIONAPP_PUBLISH_PROFILE  # For function deployment
```

### Manual Deployment
```bash
# Frontend
az storage blob upload-batch \
  --destination '$web' \
  --source . \
  --pattern "*.html" "*.css" "*.js" \
  --connection-string "$AZURE_STORAGE_CONNECTION_STRING"

# Backend
cd backend/api
func azure functionapp publish func-resume-1760986821
```

## 🏃‍♂️ API Endpoints

### Visitor Counter
```bash
# Get current count
GET https://func-cloud-resume-backend.azurewebsites.net/api/get-visitor-count

# Health check
GET https://func-cloud-resume-backend.azurewebsites.net/api/health
```

### Response Format
```json
{
  "success": true,
  "count": 1337,
  "method": "POST",
  "timestamp": "2025-10-22T12:00:00.000Z",
  "message": "Visitor count incremented successfully",
  "source": "Azure Storage Tables"
}
```

## � CI/CD Pipeline Details

### Frontend Workflow (`.github/workflows/frontend.yml`)
```yaml
Triggers:
  - Push to main/master (when HTML/CSS/JS files change)
  - Manual dispatch

Steps:
  1. 🧪 Validate HTML structure and responsive meta tags
  2. 🔍 Check for required elements (visitor-count)
  3. 📤 Deploy to Azure Storage using connection string
  4. 📁 Upload: index.html, script.js, styles.css, images/
  5. ✅ Set proper MIME types for each file
```

### Backend Workflow (`.github/workflows/backend.yml`)
```yaml
Triggers:
  - Push to main/master (when backend/ files change)
  - Manual dispatch

Steps:
  1. 🧪 Validate project structure and required files
  2. 🐍 Setup Python 3.11 and install dependencies
  3. 🔍 Validate code syntax and required imports
  4. 📦 Create deployment package with essential files
  5. 🚀 Deploy to Azure Functions using publish profile
  6. ✅ Verify deployment success
```

### Required GitHub Secrets
```bash
# Azure Storage Connection String
AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;..."

# Azure Functions Publish Profile (XML)
AZURE_FUNCTIONAPP_PUBLISH_PROFILE="<publishProfile>...</publishProfile>"
```

## �🔧 Configuration

### Azure Resources
- **Storage Account**: `storresume1760986821`
- **Function App**: `func-cloud-resume-backend`
- **Resource Group**: `rg-cloud-resume`
- **Front Door**: `resume-endpoint-gmd7e5g9f8c6gqgs.z01.azurefd.net`

### DNS Configuration
- **Primary Domain**: `www.abidaslam.online` (CNAME → Azure Front Door)
- **Root Domain**: `abidaslam.online` (Forwards to www)
- **Validation**: `_dnsauth.abidaslam.online` (TXT record for Azure)

## 🔍 Troubleshooting CI/CD Issues

### Common Frontend Deployment Errors

#### ❌ "az cli script failed"
```bash
# Check file existence before upload
if [ -f "styles.css" ]; then
  az storage blob upload ...
fi
```

#### ❌ "Connection string invalid"
```bash
# Verify GitHub secret format:
AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;..."
```

#### ❌ "Container '$web' not found"
```bash
# Enable static website hosting on storage account
az storage blob service-properties update \
  --account-name storresume1760986821 \
  --static-website \
  --index-document index.html
```

### Common Backend Deployment Errors

#### ❌ "Function app not found"
```bash
# Verify function app name in workflow:
app-name: func-cloud-resume-backend  # Correct name
```

#### ❌ "Publish profile invalid"
```bash
# Get new publish profile:
az functionapp deployment list-publishing-profiles \
  --name func-cloud-resume-backend \
  --resource-group rg-cloud-resume \
  --xml
```

#### ❌ "Python dependencies failed"
```bash
# Check requirements.txt format:
azure-functions==1.18.0
azure-data-tables==12.4.0
```

### Debugging Steps
1. **Check GitHub Actions logs** for detailed error messages
2. **Verify Azure resource names** match workflow configuration
3. **Test API endpoints manually** before deploying
4. **Validate file paths** in upload commands
5. **Check Azure portal** for function app logs

## 📊 Monitoring

### Application Insights
- Function execution metrics
- Error tracking and diagnostics
- Performance monitoring

### Health Checks
```bash
curl https://func-resume-1760986821.azurewebsites.net/api/health
```

## 🔐 Security

- **HTTPS Everywhere**: Automatic HTTP→HTTPS redirects
- **CORS Configuration**: Properly configured for custom domain
- **No Hardcoded Secrets**: All sensitive data in environment variables
- **Managed Certificates**: Auto-renewed SSL via Azure Front Door

## 📈 Performance

- **Global CDN**: Azure Front Door edge locations
- **Serverless Backend**: Auto-scaling Azure Functions
- **Optimized Assets**: Minified CSS/JS, compressed images
- **Fast Database**: Azure Storage Tables with low latency

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Cloud Resume Challenge

This project implements all requirements of the Azure Cloud Resume Challenge:

- ✅ **HTML**: Semantic HTML5 structure
- ✅ **CSS**: Responsive design with modern styling
- ✅ **Static Website**: Azure Storage static hosting
- ✅ **HTTPS**: SSL via Azure Front Door
- ✅ **DNS**: Custom domain with proper DNS configuration
- ✅ **Javascript**: Dynamic visitor counter
- ✅ **Database**: Azure Storage Tables for persistence
- ✅ **API**: Azure Functions HTTP triggers
- ✅ **Python**: Backend logic in Python 3.11
- ✅ **Tests**: Automated validation in CI/CD
- ✅ **Infrastructure as Code**: Azure resource management
- ✅ **Source Control**: Git with GitHub
- ✅ **CI/CD**: GitHub Actions automation
- ✅ **Blog Post**: [Implementation details and lessons learned](https://dev.to/abidaslam)

---

**Built with ❤️ using Azure Cloud Services**