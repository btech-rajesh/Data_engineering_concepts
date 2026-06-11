# Spark SQL Data Pipeline Documentation

## Overview
This project implements a data pipeline using Apache Spark, Azure Databricks, and AES encryption for secure data processing. The pipeline follows the medallion architecture: Bronze (raw data) → Silver (cleaned data) → Gold (aggregated data).

---

## Notebook Execution Steps

### Step 1: Create Metadata (Notebook 01_create_metadata.ipynb)
**Purpose**: Initialize the data warehouse schema structure and set up Azure storage connections.

**Tasks**:
1. **Configure Azure Storage Connection**
   - Set up Storage Account credentials (`tfdataaccount`)
   - Configure Container name (`data`)
   - Construct base path using `abfss://` protocol
   - Test connection to Azure Blob Storage

2. **Create Schema Layers**
   - **Bronze Schema**: Raw data layer - stores unprocessed data from source systems
   - **Silver Schema**: Cleaned/processed data layer - applies transformations and data quality rules
   - **Gold Schema**: Business-ready aggregated layer - serves analytics and reporting needs
   
3. **Verify Schema Creation**
   - Display all created schemas
   - Print detailed schema information and locations
   - Confirm paths are properly configured in Azure storage

**Execution Note**: This notebook should be run **first** to ensure all schema locations are created before loading data.

---

### Step 2: Load Bronze Data (Notebook 02_load_bronze_data.ipynb)
**Purpose**: Load raw data from source systems and store in Bronze layer with encryption applied to PII columns.

**Tasks**:
1. **Configure Storage Paths**
   - Define paths for Expedia and Hotel-Weather source data
   - Verify connectivity to Azure storage

2. **Initialize AES Encryption Service**
   - Load encryption key from Environment
   - Create AESService instance for encrypting sensitive data
   - Prepare PII columns list for encryption

3. **Load Source Data**
   - Read Expedia data in AVRO format
   - Read Hotel-Weather data in Parquet format
   - Infer schemas automatically

4. **Apply Encryption to PII**
   - Encrypt sensitive columns: `user_id`, `user_location_country`, `user_location_region`, `user_location_city`
   - Encrypt hotel details: `address`, `name`
   - Store encrypted data in Bronze schema

**Execution Note**: Run this notebook **second**, after schema setup is complete. Ensure AES key is available.

---

### Step 3: Bronze to Silver Transformation (Notebook 03_bronze_to_silver.ipynb)
**Purpose**: Clean and standardize data, apply business rules, and prepare for analytics.

**Tasks**:
1. **Data Cleaning**
   - Trim whitespace from string columns
   - Replace empty strings with NULL values
   - Remove duplicate records
   - Handle data type conversions

2. **Data Standardization**
   - Convert date columns to standard format
   - Standardize numeric fields (integers, doubles)
   - Apply data quality checks and validation rules

3. **PII Data Handling**
   - Keep sensitive data encrypted during transformation
   - Maintain data lineage for audit purposes
   - Apply consistent transformations to all records

4. **Write to Silver Layer**
   - Store cleaned data in `silver.hotel_weather_processed` table
   - Store cleaned data in `silver.expedia_processed` table
   - Maintain partition strategy for performance

**Execution Note**: Run this notebook **third**, after Bronze data is loaded.

---

### Step 4: Silver to Gold Aggregation (Notebook 04_silver_to_gold.ipynb)
**Purpose**: Create business-ready aggregated datasets, decrypt PII for analysis, and generate insights.

**Tasks**:
1. **Load Silver Data**
   - Read `silver.hotel_weather_processed` table
   - Read `silver.expedia_processed` table
   - Verify data quality and completeness

2. **Decrypt PII Columns**
   - Decrypt user location information from Expedia data
   - Decrypt hotel details (address, name)
   - Verify decryption integrity

3. **Create Aggregations**
   - Join hotel weather and booking data on common keys
   - Create summary tables for business metrics
   - Apply window functions for time-series analysis
   - Generate KPIs and business intelligence views

4. **Write to Gold Layer**
   - Store aggregated data in `gold.*` tables
   - Make data available for BI tools and dashboards
   - Ensure data is properly indexed and partitioned

**Execution Note**: Run this notebook **fourth** to complete the pipeline. This layer serves analytics and reporting.

---

## AES Encryption Utilities

### Overview
The `AESModule` provides encryption and decryption services using Fernet (symmetric AES encryption). It's designed to work seamlessly with Apache Spark DataFrames to encrypt/decrypt PII (Personally Identifiable Information) columns.

### AESService Class

#### **Constructor: `__init__(self, key)`**
```python
aes_service = AESService("encryption_key")
```
- **Purpose**: Initialize the AES encryption service with a master key
- **Parameters**:
  - `key`: Master encryption key (string)
- **Process**:
  1. Takes the provided key (or uses default: `"my_default_secret_key"`)
  2. Encodes key as UTF-8 bytes
  3. Hashes using SHA-256 algorithm
  4. Base64 URL-safe encodes the hash for Fernet compatibility
- **Use Case**: Create service instance at the start of a notebook session

---

#### **Method: `_encrypt_data(self, data)`**
- **Purpose**: Encrypts individual string values using Fernet cipher
- **Parameters**:
  - `data`: String value to encrypt (any data type gets converted to string)
- **Returns**: Encrypted string (or None if encryption fails)
- **Process**:
  1. Checks if data is not None/empty
  2. Instantiates Fernet cipher locally (Spark worker safe)
  3. Converts data to UTF-8 bytes
  4. Encrypts bytes and encodes result as string
  5. Returns encrypted string (can be safely stored)
- **Security**: Re-instantiates Fernet for each call to ensure Spark worker compatibility
- **Error Handling**: Returns None if encryption fails (silently)

---

#### **Method: `_decrypt_data(self, data)`**
- **Purpose**: Decrypts Fernet-encrypted string values
- **Parameters**:
  - `data`: Encrypted string to decrypt
- **Returns**: Decrypted original string (or None if decryption fails)
- **Process**:
  1. Checks if data is not None/empty
  2. Instantiates Fernet cipher locally
  3. Encodes encrypted string as UTF-8 bytes
  4. Decrypts bytes using Fernet
  5. Returns decrypted string
- **Use Case**: Retrieve original values when analysis requires unencrypted PII
- **Error Handling**: Returns None if decryption fails (wrong key, corrupted data, etc.)

---

#### **Method: `encrypt_pii_columns(self, df, columns_to_encrypt)`**
- **Purpose**: Encrypt specified columns in a Spark DataFrame
- **Parameters**:
  - `df`: Apache Spark DataFrame
  - `columns_to_encrypt`: List of column names (strings) to encrypt
- **Returns**: DataFrame with encrypted columns
- **Process**:
  1. Creates Spark UDF from `_encrypt_data` method with StringType output
  2. Iterates through columns to encrypt
  3. Validates column exists in DataFrame
  4. Applies encryption UDF to each column
  5. Returns modified DataFrame with encrypted values
- **Output**: Logs encrypted column names for audit trail
- **Example**:
  ```python
  encrypted_df = aes_service.encrypt_pii_columns(
      df, 
      ["user_id", "email", "address"]
  )
  ```

---

#### **Method: `decrypt_pii_columns(self, df, columns_to_decrypt)`**
- **Purpose**: Decrypt specified columns in a Spark DataFrame
- **Parameters**:
  - `df`: Apache Spark DataFrame (containing encrypted columns)
  - `columns_to_decrypt`: List of column names (strings) to decrypt
- **Returns**: DataFrame with decrypted columns
- **Process**:
  1. Creates Spark UDF from `_decrypt_data` method with StringType output
  2. Iterates through columns to decrypt
  3. Validates column exists in DataFrame
  4. Applies decryption UDF to each column
  5. Returns modified DataFrame with decrypted values
- **Output**: Logs decrypted column names for audit trail
- **Use Case**: Convert encrypted data back to readable format for analysis or reporting
- **Example**:
  ```python
  decrypted_df = aes_service.decrypt_pii_columns(
      df,
      ["user_id", "email", "address"]
  )
  ```

---

### Key Features
- **Spark Compatible**: Designed to work with distributed Spark DataFrames
- **Worker Safe**: Re-instantiates Fernet on each call to avoid pickling issues across workers
- **PII Protection**: Encrypts sensitive columns to meet compliance requirements
- **Error Resilience**: Gracefully handles encryption/decryption failures
- **Audit Trail**: Logs which columns are being encrypted/decrypted

### Usage Pattern
```python
from AESUtils import AESService

# Initialize with key from Azure Key Vault
aes_key = os.getenv("AES_KEY")
aes_service = AESService(aes_key)

# Encrypt sensitive columns
encrypted_df = aes_service.encrypt_pii_columns(df, ["user_id", "email"])

# Process data...

# Decrypt when needed
decrypted_df = aes_service.decrypt_pii_columns(encrypted_df, ["user_id", "email"])
```

---

## Screenshots

Below are screenshots documenting the pipeline architecture and execution:

### 1. Azure Data

**Screenshots/azure data.png**

---

### 2. Databricks Pipeline Flow

**Screenshots/Databricks Pipeline flow.png**

---

### 3. ETL Pipeline Execution

**Screenshots/ETL Pipeline execution.png**

---

### 4. Individual Notebook Execution

**Screenshots/individual notebook execution.png**

---

## Quick Reference: Execution Order

| Step | Notebook | Purpose | Prerequisites |
|------|----------|---------|----------------|
| 1 | 01_create_metadata | Create schema structure | Azure credentials |
| 2 | 02_load_bronze_data | Load raw data with encryption | Step 1 complete |
| 3 | 03_bronze_to_silver | Clean and standardize data | Step 2 complete |
| 4 | 04_silver_to_gold | Aggregate and prepare for analytics | Step 3 complete |

---

## Configuration Requirements

- **Azure Storage Account**: `tfdataaccount`
- **Container**: `data`
- **AES Encryption Key**: Available from Databricks Environment
- **Source Data Formats**: 
  - Expedia: AVRO
  - Hotel-Weather: Parquet

---

## Notes

- Always execute notebooks in order (01 → 02 → 03 → 04)
- Ensure AES key is properly configured before loading data
- Data in Silver layer contains encrypted PII
- Data in Gold layer contains decrypted PII for analytics