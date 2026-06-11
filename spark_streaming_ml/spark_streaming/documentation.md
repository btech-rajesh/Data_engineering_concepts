# Spark Streaming Python Azure - Complete Project Documentation

## 📋 Project Overview

This is a comprehensive Apache Spark streaming application built with Python for Azure cloud infrastructure. The project demonstrates a complete data pipeline using the Bronze-Silver-Gold architectural pattern with data encryption capabilities, infrastructure as code, and streaming operations.

---

## 📁 Project Structure

```
spark_streaming/
├── documentation.md                          # Project documentation
├── m13_sparkstreaming_python_azure/
│   ├── README.md                             # Setup and prerequisites
│   ├── setup-macos.md                        # MacOS environment setup
│   ├── setup-ubuntu.md                       # Ubuntu environment setup
│   ├── setup-windows.md                      # Windows environment setup
│   ├── AESModule/                            # Encryption utilities
│   │   ├── setup.py                          # AESModule package setup
│   │   └── AESUtils/
│   │       ├── __init__.py
│   │       └── AES.py                        # AES encryption/decryption service
│   ├── notebooks/                            # Jupyter notebooks for data pipeline
│   │   ├── 01_create_metadata.ipynb          # Create metadata
│   │   ├── 02_load_bronze_data.ipynb         # Load raw data (Bronze layer)
│   │   ├── 03_bronze_to_silver.ipynb         # Transform to Silver layer
│   │   ├── 04_silver_to_gold.ipynb           # Aggregate to Gold layer
│   │   ├── dashboard.ipynb                   # Visualization dashboard
│   │   └── StreamingApp.py                   # Streaming application
│   ├── screenshots/                          # Documentation screenshots
│   │   └── visualisation/                    # Visualization examples
│   └── terraform/                            # Infrastructure as Code
│       ├── main.tf                           # Main Terraform configuration
│       ├── variables.tf                      # Variable definitions
│       ├── versions.tf                       # Provider versions
│       └── terraform.plan                    # Terraform plan file
```

---

## 🔧 Core Components

### 1. **AESModule - Encryption Utility**

**Purpose**: Provides AES encryption/decryption functionality for PII (Personally Identifiable Information) data protection.

**Location**: `AESModule/`

**Dependencies**:
- `cryptography>=3.4.0` - Cryptographic library for AES operations
- `pyspark>=3.0.0` - Apache Spark for distributed computing

**Key Features**:
- `AESService` class for encryption/decryption operations
- PySpark UDF (User Defined Function) integration for distributed encryption
- Support for encrypting/decrypting multiple DataFrame columns
- Fernet-based symmetric encryption with SHA256 key hashing

**Installation**:
```bash
cd AESModule
pip install -e .
```

**Usage Example**:
```python
from AESUtils.AES import AESService

# Initialize service with encryption key
aes_service = AESService(key="my_encryption_key")

# Encrypt PII columns
encrypted_df = aes_service.encrypt_pii_columns(df, ["email", "phone"])

# Decrypt columns
decrypted_df = aes_service.decrypt_pii_columns(encrypted_df, ["email", "phone"])
```

---

### 2. **Notebooks - Data Pipeline**

**Location**: `notebooks/`

#### **01_create_metadata.ipynb**
- **Purpose**: Initialize and create metadata structures
- **Inputs**: N/A (setup phase)
- **Outputs**: Metadata configuration for downstream pipelines

#### **02_load_bronze_data.ipynb**
- **Purpose**: Load raw data from Azure storage (Bronze layer)
- **Data Pattern**: Bronze = Raw data layer
- **Operations**: 
  - Connect to Azure storage account
  - Read raw data files (CSV, Parquet, JSON, etc.)
  - Validate data integrity
  - Store in Bronze layer

#### **03_bronze_to_silver.ipynb**
- **Purpose**: Transform and clean Bronze data → Silver layer
- **Data Pattern**: Silver = Cleaned, deduplicated, validated data
- **Operations**:
  - Data cleaning (remove duplicates, handle nulls)
  - Data type conversions
  - PII encryption using AESModule
  - Data quality checks
  - Partitioning for performance

#### **04_silver_to_gold.ipynb**
- **Purpose**: Aggregate Silver data → Gold layer
- **Data Pattern**: Gold = Business-ready aggregated data
- **Operations**:
  - Data aggregation and summarization
  - Business logic implementation
  - Creation of fact and dimension tables
  - Optimization for reporting and analytics

#### **dashboard.ipynb**
- **Purpose**: Create interactive dashboards and visualizations
- **Features**:
  - Data visualization and exploration
  - KPI tracking
  - Dashboard creation using Plotly/Matplotlib

#### **StreamingApp.py**
- **Purpose**: Standalone streaming application
- **Functionality**:
  - Real-time data ingestion from streaming sources
  - Processing pipeline for streaming data
  - Output to Azure storage or databases

---

### 3. **Terraform - Infrastructure as Code**

**Location**: `terraform/`

**Purpose**: Define and provision Azure cloud infrastructure automatically.

**Files**:
- `main.tf` - Primary Terraform configuration
- `variables.tf` - Input variables and defaults
- `versions.tf` - Required provider versions
- `terraform.plan` - Saved execution plan

**Azure Resources Managed**:
- **Resource Groups**: Logical containers for resources
- **Storage Accounts**: Data storage with hierarchical namespace (HNS)
- **State Backend**: Remote Terraform state management in Azure

**Key Configuration**:
```hcl
# Terraform State Backend
backend "azurerm" {
  resource_group_name  = "tfaccount"
  storage_account_name = "tfdataaccount"
  container_name       = "data"
}

# Azure Provider
provider "azurerm" {
  features {}
  subscription_id = "YOUR_SUBSCRIPTION_ID"
}
```

**Deployment Steps**:
```bash
cd terraform
terraform init
terraform plan -out=terraform.plan
terraform apply terraform.plan
```

---

### 4. **Screenshots & Visualizations**

**Location**: `screenshots/`

Contains documentation screenshots and visualization examples organized as follows:

```
screenshots/
├── azure_data_continer.png              # Azure data container setup screenshot
├── cluster_all_notebooks.png            # Spark cluster with all notebooks running
├── Data_2016_record.png                 # Sample data from 2016 records
├── Data_2016_record_3.png               # Additional 2016 data sample
├── data_after_2017.png                  # Data after 2017 processing
├── data_after_updating_2017_records.png # Updated 2017 records schemas
├── data_write_schemas.png               # Data schema write 
jobExecution
├── independent_job_run.png              # Independent Spark job execution
├── job_run_success.png                  # Successful job completion screen
├── Screenshot 2026-02-14 192437.png     # General system screenshot
├── desktop.ini                          # Windows desktop configuration
└── visualisation/                       # City-wise visualization dashboards
    ├── Amsterdam.png                    # Amsterdam data visualization
    ├── Barcelona.png                    # Barcelona data visualization
    ├── London.png                       # London data visualization
    ├── Milan.png                        # Milan data visualization
    └── Paris.png                        # Paris data visualization
```

**Screenshot Categories**:

1. **Infrastructure & Setup**
   - `azure_data_continer.png` - Azure storage container configuration
   - `cluster_all_notebooks.png` - Spark cluster deployment

2. **Data Processing & Results**
   - `Data_2016_record.png`, `Data_2016_record_3.png` - Input data samples
   - `data_after_2017.png` - Post-processing data (2017)
   - `data_after_updating_2017_records.png` - Updated records

3. **Job Execution**
   - `independent_job_run.png` - Spark job execution
   - `job_run_success.png` - Successful job completion
   - `data_write_schemas.png` - Schema definitions and writes

4. **Dashboard Visualizations** (`visualisation/`)
   - City-based data visualizations (Amsterdam, Barcelona, London, Milan, Paris)
   - Used for dashboard.ipynb demonstrations

---

## 📦 Project Dependencies

### Python Packages
```
cryptography>=3.4.0          # Encryption library
pyspark>=3.0.0               # Apache Spark
pandas                       # Data manipulation
plotly                       # Visualizations
matplotlib                   # Plotting library
numpy                        # Numerical computing
```

### External Tools
```
Azure CLI                    # Azure resource management
Terraform                    # Infrastructure as Code
Databricks                   # Spark cluster hosting (optional)
```

### Azure Resources
```
Resource Group               # Logical container
Storage Account              # Data storage with HNS enabled
Storage Container            # Blob storage partitions
Spark Cluster               # Compute resource (via Databricks)
```

---

## 🚀 Getting Started

### Prerequisites
1. **Azure Account** - Free tier or paid subscription
2. **Python 3.8+** - For local development
3. **Azure CLI** - For authentication and resource management
4. **Terraform** - For infrastructure provisioning

### Installation Steps

#### 1. Clone and Setup
```bash
cd spark_streaming/m13_sparkstreaming_python_azure
```

#### 2. Choose Your OS and Follow Setup Guide
- **Windows**: `setup-windows.md`
- **MacOS**: `setup-macos.md`
- **Ubuntu**: `setup-ubuntu.md`

#### 3. Install AESModule
```bash
cd AESModule
pip install -e .
cd ..
```

#### 4. Setup Azure Infrastructure with Terraform
```bash
cd terraform
terraform init
terraform plan
terraform apply
cd ..
```

#### 5. Run Notebooks in Order
1. Open `01_create_metadata.ipynb` → Run all cells
2. Open `02_load_bronze_data.ipynb` → Run all cells
3. Open `03_bronze_to_silver.ipynb` → Run all cells
4. Open `04_silver_to_gold.ipynb` → Run all cells
5. Open `dashboard.ipynb` → Create visualizations

---

## 🔐 Security & Data Protection

### Encryption Strategy
- **PII Protection**: Sensitive columns encrypted using AES-256 (via Fernet)
- **Key Management**: Keys derived from SHA256 hashing of seed values
- **Distributed Processing**: Safe encryption across Spark workers

### Azure Security
- **Authentication**: Azure CLI login
- **RBAC**: Role-based access control via Azure
- **Storage**: Encrypted storage accounts
- **Network**: Configured network rules

---

## 📊 Data Pipeline Architecture

```
Raw Data (External Sources)
         ↓
    [Bronze Layer]
  (Raw data storage)
         ↓
  02_load_bronze_data.ipynb
         ↓
    [Silver Layer]
  (Cleaned, encrypted, validated)
         ↓
  03_bronze_to_silver.ipynb
         ↓
    [Gold Layer]
  (Aggregated, business-ready)
         ↓
  04_silver_to_gold.ipynb
         ↓
  [Dashboard/Analytics]
```

---

## 🛠️ Common Operations

### Run All Notebooks Sequentially
```bash
jupyter nbconvert --to notebook --execute 01_create_metadata.ipynb
jupyter nbconvert --to notebook --execute 02_load_bronze_data.ipynb
jupyter nbconvert --to notebook --execute 03_bronze_to_silver.ipynb
jupyter nbconvert --to notebook --execute 04_silver_to_gold.ipynb
```

### Check Terraform Plan
```bash
cd terraform
terraform plan -out=terraform.plan
terraform show terraform.plan
```

### Encrypt DataFrame Columns
```python
from AESUtils.AES import AESService

service = AESService(key="your-secret-key")
encrypted_df = service.encrypt_pii_columns(df, ["email", "phone", "ssn"])
```

### Clean Up Azure Resources
```bash
cd terraform
terraform destroy
```

---

## 📚 Environment Setup Files

All OS-specific setup instructions are provided:
- **setup-windows.md**: Windows 10/11 setup with Visual Studio or WSL
- **setup-macos.md**: MacOS installation guide
- **setup-ubuntu.md**: Ubuntu 24.10 environment setup

---

## ⚠️ Important Notes

### Azure Quotas
- Free-tier accounts have strict resource limits
- **Clean up resources before deploying new ones**
- Monitor Azure cost to avoid unexpected charges

### Terraform State
- Remote state stored in Azure Storage Account
- State file contains sensitive information - restrict access
- Always backup state files before terraform destroy

### Data Encryption Keys
- Securely manage encryption keys
- Use Azure Key Vault for production deployments
- Never hardcode keys in notebooks

---

## 📞 Support & Documentation

- **Official Databricks Documentation**: https://docs.databricks.com
- **PySpark Documentation**: https://spark.apache.org/docs/latest/api/python/
- **Azure Documentation**: https://docs.microsoft.com/en-us/azure/
- **Terraform Documentation**: https://www.terraform.io/docs/

---

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Feb 2026 | Initial project documentation |

---

**Last Updated**: February 14, 2026