# Azure Resume Challenge 🚀

A complete cloud resume website built with Azure services, featuring real-time visitor tracking and modern web design.

## 🌐 Live Website
- **Production URL**: [https://abidaslam.online](https://abidaslam.online)
- **WWW Subdomain**: [https://www.abidaslam.online](https://www.abidaslam.online)
- **API Endpoint**: [https://func-resume-1760986821.azurewebsites.net/api/visitor-counter](https://func-resume-1760986821.azurewebsites.net/api/visitor-counter)

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Custom Domain │───▶│  Azure Front    │───▶│  Azure Storage  │
│  abidaslam.online │    │     Door        │    │  Static Website │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │ Azure Functions │───▶│   CosmosDB      │
                       │  (Visitor API)  │    │  Table Storage  │
                       └─────────────────┘    └─────────────────┘
```

## ✅ Features

- **Modern Resume Design**: Professional CV with dark theme and responsive layout
- **Real-time Visitor Counter**: Tracks page views using Azure Functions and CosmosDB
- **Custom Domain**: SSL-secured custom domain with Azure Front Door CDN
- **Global Performance**: Azure Front Door provides global content delivery
- **Infrastructure as Code**: Complete ARM templates for deployment automation
- **CI/CD Ready**: GitHub Actions workflows for automated deployment

## 🛠️ Technology Stack

### Frontend
- **HTML5/CSS3**: Modern responsive design with CSS Grid and Flexbox
- **JavaScript**: Vanilla JS for API integration and animations
- **Azure Storage**: Static website hosting with $web container

### Backend
- **Azure Functions**: Python 3.11 runtime with HTTP triggers
- **CosmosDB**: Table API for visitor counter storage
- **Application Insights**: Monitoring and telemetry

### Infrastructure
- **Azure Front Door**: Global CDN with custom domain and SSL
- **ARM Templates**: Infrastructure as Code for reproducible deployments
- **Azure DNS**: Custom domain management and SSL certificates

## 📁 Project Structure

```
📦 Azure-Resume-Challenge
├── 📁 backend/
│   ├── function_app.py          # Azure Functions Python code
│   ├── host.json               # Functions runtime configuration
│   ├── requirements.txt        # Python dependencies
│   └── 📁 tests/              # Unit tests
├── 📁 frontend/
│   ├── index.html             # Main resume webpage
│   ├── styles.css             # Stylesheet with modern design
│   └── script-simple.js       # Visitor counter JavaScript
├── 📁 scripts/
│   ├── deploy-backend.sh      # Backend deployment script
│   ├── deploy-frontend.sh     # Frontend deployment script
│   └── validate-deployment.sh # Template validation
├── arm-template.json          # Complete infrastructure template
├── arm-parameters.json        # Deployment parameters
└── README.md                  # This file
```

## 🚀 Deployment

### Prerequisites
- Azure CLI installed and configured
- Azure subscription with appropriate permissions  
- Python 3.11 and Azure Functions Core Tools

### Quick Start
```bash
# Clone repository
git clone <repository-url>
cd Azure-Resume-Challenge

# Deploy backend
cd backend
func azure functionapp publish func-resume-1760986821 --python

# Deploy frontend  
cd ../frontend
az storage blob upload-batch --destination '$web' --source . --account-name storresume1760986821

# Verify deployment
curl https://func-resume-1760986821.azurewebsites.net/api/visitor-counter
```

### Infrastructure Deployment
```bash
# Deploy complete infrastructure
az deployment group create \
  --name azure-resume-deployment \
  --resource-group rg-cloud-resume \
  --template-file arm-template.json \
  --parameters @arm-parameters.json
```

## 📊 Monitoring & Analytics

- **Application Insights**: Function performance and error tracking
- **Azure Front Door Analytics**: Global traffic patterns and performance
- **CosmosDB Metrics**: Database performance and request units
- **Custom Visitor Counter**: Real-time page view tracking

## 🔧 Configuration

### Environment Variables
```bash
# Azure Functions Configuration
COSMOS_DB_CONNECTION_STRING="AccountEndpoint=https://cosmos-resume-1760986821.documents.azure.com:443/;AccountKey=<key>;TableEndpoint=https://cosmos-resume-1760986821.table.cosmos.azure.com:443/;"
COSMOS_DB_ACCOUNT_NAME="cosmos-resume-1760986821"
COSMOS_DB_TABLE="VisitorCounter"
```

### DNS Configuration
```
# Custom Domain DNS Records
Type: CNAME
Name: www
Value: resume-endpoint-gmd7e5g9f8c6gqgs.z01.azurefd.net

Type: A  
Name: @
Value: 13.107.213.63, 13.107.246.63
```

## 🧪 Testing

### API Testing
```bash
# Test visitor counter
curl -X POST https://func-resume-1760986821.azurewebsites.net/api/visitor-counter

# Health check
curl https://func-resume-1760986821.azurewebsites.net/api/health

# Get visitor stats
curl https://func-resume-1760986821.azurewebsites.net/api/visitor-stats
```

### Website Testing
- **Performance**: Lighthouse score optimization
- **Responsiveness**: Cross-device compatibility testing
- **SSL**: Certificate validation and security headers
- **SEO**: Meta tags and structured data

## 📈 Performance Metrics

- **Global CDN**: Azure Front Door edge locations
- **API Response**: ~200-300ms average response time
- **Database**: CosmosDB Table API with millisecond latency
- **SSL Score**: A+ rating with TLS 1.2+ encryption
- **Uptime**: 99.9% availability (Azure SLA)

## 🔐 Security

- **HTTPS Only**: All traffic encrypted with TLS 1.2+
- **CORS Configuration**: Proper cross-origin resource sharing
- **Function Authentication**: Anonymous level for public API
- **Secret Management**: Azure Key Vault integration ready
- **Network Security**: Azure Front Door WAF capabilities

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Abid Aslam**
- LinkedIn: [linkedin.com/in/abid-aslam-75520330](https://www.linkedin.com/in/abid-aslam-75520330/)
- Email: abidaslam.123@gmail.com
- Website: [abidaslam.online](https://abidaslam.online)

## 🎯 Azure Cloud Resume Challenge

This project successfully completes the [Azure Cloud Resume Challenge](https://cloudresumechallenge.dev/docs/the-challenge/azure/) with all requirements:

- ✅ HTML/CSS Resume
- ✅ Static Website Hosting  
- ✅ HTTPS Custom Domain
- ✅ Visitor Counter with JavaScript
- ✅ Database Integration
- ✅ API Development
- ✅ Python Backend
- ✅ Infrastructure as Code
- ✅ Source Control
- ✅ CI/CD Pipeline Ready

---

**🚀 Live Demo**: [abidaslam.online](https://abidaslam.online)
