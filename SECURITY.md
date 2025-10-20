# 🔒 Security & Credentials Setup

## ⚠️ Important Security Notice

This is a **PUBLIC REPOSITORY** - credentials are **NEVER** stored in code!

### 🔑 Required GitHub Secrets

Only **ONE** secret is required for CI/CD deployment:

| Secret Name | Description | Source |
|-------------|-------------|---------|
| `AZURE_CREDENTIALS` | Service Principal JSON | Azure CLI (`az ad sp create-for-rbac`) |

### 🛡️ Security Best Practices Applied

✅ **No hardcoded credentials** in source code  
✅ **No sensitive data** in commit history  
✅ **GitHub Secrets** used for secure storage  
✅ **Minimal permissions** (Contributor only on resource group)  
✅ **Public repository safe** - all credentials externalized  

### 🔧 Setup Process

1. **Create Service Principal** (Azure CLI)
2. **Add to GitHub Secrets** (Repository Settings)
3. **Test Deployment** (Push to trigger CI/CD)
4. **Monitor Results** (GitHub Actions)

> **Note**: Detailed setup instructions are provided separately for security.

### 🚀 Deployment Architecture

```
GitHub Repository (PUBLIC) → GitHub Actions (SECURE) → Azure Resources
                                     ↓
                            GitHub Secrets (ENCRYPTED)
                                     ↓
                            Azure Service Principal
                                     ↓
                            Resource Group: rg-cloud-resume
```

### 📊 Monitoring & Validation

- **GitHub Actions**: https://github.com/abidaslam892/Azure-Resume-Project/actions
- **Live Website**: https://resume-endpoint-gmd7e5g9f8c6gqgs.z01.azurefd.net/
- **API Health**: Validated during CI/CD pipeline

---

**🔒 This repository follows security best practices for public cloud projects.**