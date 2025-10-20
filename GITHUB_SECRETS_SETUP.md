# 🔐 GitHub Secrets Configuration Guide

To enable automated CI/CD deployment, you need to configure the following secrets in your GitHub repository settings.

## 📝 Required GitHub Secrets

Navigate to: **Repository → Settings → Secrets and variables → Actions → New repository secret**

### 🔑 Azure Authentication
```bash
AZURE_CREDENTIALS
```
**Value**: Service Principal JSON (create using Azure CLI)
```json
{
  "clientId": "your-service-principal-client-id",
  "clientSecret": "your-service-principal-secret",
  "subscriptionId": "your-azure-subscription-id", 
  "tenantId": "your-azure-tenant-id"
}
```

### 🏗️ Azure Resources
```bash
AZURE_STORAGE_ACCOUNT=storresume1760986821
AZURE_FUNCTIONAPP_NAME=func-resume-1760986821
AZURE_RESOURCE_GROUP=rg-cloud-resume
AZURE_CDN_PROFILE=afd-resume-profile
AZURE_CDN_ENDPOINT=resume-endpoint-gmd7e5g9f8c6gqgs

# CosmosDB Configuration
COSMOS_DB_ACCOUNT_NAME=cosmos-resume-1760986821
COSMOS_DB_KEY=your-cosmosdb-primary-key
```

## 🛠️ Creating Azure Service Principal

Run this command in Azure CLI to create the service principal:

```bash
az ad sp create-for-rbac \
  --name "github-actions-resume" \
  --role "Contributor" \
  --scopes "/subscriptions/YOUR_SUBSCRIPTION_ID/resourceGroups/rg-cloud-resume" \
  --json-auth
```

Copy the entire JSON output and paste it as the `AZURE_CREDENTIALS` secret.

## 🔍 Getting CosmosDB Key

```bash
az cosmosdb keys list \
  --name cosmos-resume-1760986821 \
  --resource-group rg-cloud-resume \
  --query "primaryMasterKey" \
  --output tsv
```

## ✅ Verification

After adding all secrets, push a commit to trigger the GitHub Actions workflows:

```bash
git commit --allow-empty -m "Trigger CI/CD pipeline"
git push origin main
```

Check the **Actions** tab in your GitHub repository to see the deployment progress.

## 🚀 Manual Trigger

You can also manually trigger deployments:
1. Go to **Actions** tab
2. Select **Deploy Frontend** or **Deploy Backend**
3. Click **Run workflow**
4. Select the branch and click **Run workflow**

---

**📖 For detailed documentation, see the main [README.md](README.md)**