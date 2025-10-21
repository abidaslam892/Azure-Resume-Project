# Azure Cloud Resume Challenge

[![Frontend CI/CD](https://github.com/abidaslam892/Azure-Resume-Project/actions/workflows/frontend.yml/badge.svg)](https://github.com/abidaslam892/Azure-Resume-Project/actions/workflows/frontend.yml)
[![Backend CI/CD](https://github.com/abidaslam892/Azure-Resume-Project/actions/workflows/backend.yml/badge.svg)](https://github.com/abidaslam892/Azure-Resume-Project/actions/workflows/backend.yml)

🌐 **Live Website**: [https://www.abidaslam.online](https://www.abidaslam.online)

A complete implementation of the [Cloud Resume Challenge](https://cloudresumechallenge.dev/docs/the-challenge/azure/) using Azure services with modern CI/CD practices.

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Custom Domain │    │  Azure Front Door │    │ Azure Storage   │
│ abidaslam.online├────┤      (CDN)       ├────┤   Static Web    │
│                 │    │                  │    │   Hosting       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                │
                       ┌────────▼────────┐    ┌─────────────────┐
                       │ Azure Functions │    │ Azure Storage   │
                       │   (Python 3.11) ├────┤     Tables      │
                       │   Visitor API   │    │  (Database)     │
                       └─────────────────┘    └─────────────────┘
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
GET https://func-resume-1760986821.azurewebsites.net/api/visitor-counter

# Increment count (new visitor)
POST https://func-resume-1760986821.azurewebsites.net/api/visitor-counter
```

### Health Check
```bash
GET https://func-resume-1760986821.azurewebsites.net/api/health
```

### Response Format
```json
{
  "success": true,
  "count": 42,
  "method": "POST",
  "timestamp": "2025-10-21T18:30:00.000Z",
  "message": "Visitor count incremented successfully",
  "source": "Azure Storage Tables"
}
```

## 🔧 Configuration

### Azure Resources
- **Storage Account**: `storresume1760986821`
- **Function App**: `func-resume-1760986821`
- **Resource Group**: `rg-cloud-resume`
- **Front Door**: `afd-resume-profile`

### DNS Configuration
- **Primary Domain**: `www.abidaslam.online` (CNAME → Azure Front Door)
- **Root Domain**: `abidaslam.online` (Forwards to www)
- **Validation**: `_dnsauth.abidaslam.online` (TXT record for Azure)

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