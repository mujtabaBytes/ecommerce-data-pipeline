# E-Commerce Data Engineering Pipeline

A end-to-end data engineering pipeline built to extract e-commerce product data from the DummyJSON API, store raw responses, process and transform data across multi-layer architectures using Python, SQL, and PySpark, and export analytics-ready datasets in Parquet format.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Technologies Used](#technologies-used)
- [Key Features](#key-features)
- [Data Architecture & Layers](#data-architecture--layers)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [Running the Pipeline](#running-the-pipeline)
- [Output](#output)
- [Future Roadmap](#future-roadmap)
- [Author](#author)

---

## Overview

This repository contains a modular data pipeline designed to demonstrate core data engineering fundamentals, including REST API data ingestion, data transformation via PySpark and SQL, and implementation of a **Medallion (Raw-Silver-Gold) Architecture**.

The core objective is to deliver processed, clean, and aggregated datasets in optimized **Parquet** format suitable for downstream analytics and business intelligence tools.

---

## Architecture

```
+------------------+     +------------------+     +------------------+
|   DummyJSON API  | --> | Extraction (Py)  | --> |   Raw Storage    |
+------------------+     +------------------+     |   (JSON Files)   |
                                                  +------------------+
                                                           |
+------------------+     +------------------+              v
| Analytics Ready  | <-- | PySpark / SQL    | <-- +------------------+
| (Parquet Export) |     | Transformations  |     |   Data Loading   |
+------------------+     +------------------+     +------------------+
       |                         |
       v                         v
+------------------+     +------------------+
|    Gold Layer    |     |   Silver Layer   |
| (Aggregations)   |     | (Cleaned Records)|
+------------------+     +------------------+
```

---

## Technologies Used

| Category | Technology / Tool |
| :--- | :--- |
| **Language** | Python 3.10+, SQL, Bash |
| **Data Processing** | PySpark, Pandas |
| **Storage Formats** | JSON, Apache Parquet |
| **Database** | PostgreSQL |
| **API Integration** | REST API (DummyJSON) |
| **Version Control** | Git, GitHub |

---

## Key Features

- **Automated Ingestion:** Fetches e-commerce product payloads seamlessly from REST endpoints.
- **Raw Data Preservation:** Persists source JSON responses for auditability and replayability.
- **Modular Pipeline Design:** Decouples Extraction, Loading, and Transformation logic into dedicated modules.
- **Distributed Processing:** Utilizes PySpark to handle cleaning, typing, and schema enforcement.
- **Medallion Data Architecture:** Segregates raw inputs, cleansed data (Silver layer), and aggregated business metrics (Gold layer).
- **Columnar Storage:** Exports datasets to compressed Parquet format for optimal querying performance.
- **One-Command Execution:** Provides a bash wrapper (`run_pipeline.sh`) to automate sequential stage execution.

---

## Data Architecture & Layers

### 1. Raw Layer
Stores unchanged API responses in JSON format, providing complete data traceability and supporting re-processing needs.

### 2. Silver Layer
Contains cleansed, normalized, and structured product-level data:
- `Product ID`
- `Product Title`
- `Category`
- `Price`
- `Rating`
- `Stock Quantity`

### 3. Gold Layer
Features business-level summaries and category metrics suitable for direct analytical querying and reporting dashboard support.

---

## Project Structure

```text
ecommerce_pipeline/
├── data/
│   ├── raw/                        # Ingested API responses (JSON)
│   └── processed/                  # Processed datasets (Parquet)
│       ├── silver/
│       │   └── products/           # Cleansed product data
│       └── gold/
│           └── category_summary/   # Aggregated analytics data
├── src/
│   ├── extract.py                  # API Extraction script
│   ├── load.py                     # Raw storage script
│   ├── transform.py                # Python/Pandas logic
│   ├── spark_transform.py          # PySpark transformation jobs
│   ├── transform.sql               # SQL transformations
│   └── verify_spark.py             # Pipeline validation helper
├── sql/
│   └── schema.sql                  # Database DDL scripts
├── README.md                       # Project documentation
├── run_pipeline.sh                 # Sequential pipeline shell script
└── .gitignore                      # Git ignore file
```

> **Note:** Raw/processed data directories and Python virtual environment (`.venv`) are excluded from version control via `.gitignore`.

---

## Prerequisites

Ensure you have the following software installed:

- **Python:** Version 3.10 or higher
- **Java Runtime Environment (JRE/JDK):** Required for PySpark execution
- **Git:** For source control management

---

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/mujtabaBytes/ecommerce-data-pipeline.git
cd ecommerce-data-pipeline
```

### 2. Set Up Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Required Dependencies

```bash
pip install -r requirements.txt
```

*If `requirements.txt` is missing, manual setup can be run as follows:*

```bash
pip install requests pyspark pandas
```

---

## Running the Pipeline

### Automatic Pipeline Run

Grant execution permissions to the shell script and run the complete sequence:

```bash
chmod +x run_pipeline.sh
./run_pipeline.sh
```

### Manual Execution

Specific pipeline modules can also be run individually for testing or debugging:

```bash
# Step 1: Extract data
python3 src/extract.py

# Step 2: Load raw data
python3 src/load.py

# Step 3: Run PySpark transformation scripts
python3 src/spark_transform.py
```

---

## Output

Processed analytics-ready files are written to columnar Parquet files within the processed data layer directory:

```text
data/processed/
├── silver/
│   └── products/
└── gold/
    └── category_summary/
```

These Parquet datasets can easily be queried using SQL engines (DuckDB, Trino, Athena) or integrated into dashboards.

---

## Future Roadmap

- [ ] **Cloud Migration:** Integrate Azure Data Lake Storage Gen2 (ADLS Gen2) for scalable cloud storage.
- [ ] **Databricks:** Move transformations to Azure Databricks jobs.
- [ ] **Data Quality:** Implement automated quality checks with Great Expectations.
- [ ] **Orchestration:** Introduce Apache Airflow for job scheduling and dependency handling.
- [ ] **Monitoring:** Add integrated logging and failure retry handlers.
- [ ] **BI Dashboards:** Build visual dashboards connected to the Gold-layer output.

---

## Author

**Muhammad Mujtaba**  
- **GitHub:** [@mujtabaBytes](https://github.com/mujtabaBytes)

---

*Developed as part of a practical portfolio project to demonstrate core principles in data extraction, data modeling, batch processing, and end-to-end data pipeline orchestration.*