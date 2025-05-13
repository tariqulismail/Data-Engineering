

# Customer 360 Data Integration Project

## 📋 Overview
This project implements a comprehensive Customer 360 Data Integration solution that extracts, transforms, and loads customer-related data from various sources into a centralized data warehouse (Amazon Redshift). The goal is to create a unified customer view for analytics and business intelligence dashboards.

![Customer 360 Data Integration Mindmap](https://cdn1.genspark.ai/user-upload-image/imagen_generated/80467853-7a20-42be-bea0-fa73e9b2efcd)

## 🏗️ Architecture

The solution follows a modern data architecture with the following components:

- **Data Sources**: Multiple customer data touchpoints
- **Ingestion Layer**: Apache Airflow for orchestration
- **Staging Area**: Amazon S3 for raw data storage
- **Transformation Layer**: dbt for data modeling and transformation
- **Serving Layer**: Amazon Redshift as the data warehouse
- **BI Layer**: Power BI/Tableau for visualization and analytics

## 🔄 Data Pipeline

### Data Sources
- **CRM Data** (MySQL)
  - Generated with Faker library
  - Contains customer profile information
- **Salesforce Data**
  - Extracted via simple-salesforce Python package
  - Captures sales interactions and opportunities
- **Marketing Data** (Google Analytics)
  - BigQuery public datasets: `bigquery-public-data.google_analytics_sample.ga_sessions_*`
  - Provides digital customer journey data
- **Offline Transactions** (CSV Files)
  - Generated with Mockaroo
  - Contains in-store/offline purchase information

### ETL Process
1. **Extract**: Airflow DAGs pull data from each source
2. **Load**: Raw data stored in S3 buckets
3. **Transform**: dbt models clean, standardize, and join data
4. **Validate**: great_expectations library ensures data quality
5. **Load**: Final models deployed to Amazon Redshift REPORTING schema

## 🛠️ Technologies

- **Orchestration**: Apache Airflow
- **Storage**: Amazon S3, Amazon Redshift
- **Transformation**: dbt (data build tool)
- **Data Validation**: great_expectations
- **Visualization**: Power BI/Tableau
- **Infrastructure**: Docker, GitHub Actions

## 📦 Project Structure

```
customer_360/
│
├── README.md                     # Project documentation
│
├── architecture/
│   └── architecture_diagram.png  # High-level architecture visualization
│
├── dags/                         # Airflow DAG definitions
│   ├── crm_extract.py            # MySQL CRM data extraction
│   ├── salesforce_extract.py     # Salesforce data extraction
│   ├── ga_extract.py             # Google Analytics extraction
│   └── offline_extract.py        # CSV offline transaction extraction
│
├── mock_data/                    # Data generation scripts
│   ├── generate_crm_data.py      # Faker script for CRM data
│   └── generate_transactions.py  # Mockaroo script for transaction data
│
├── models/                       # dbt models
│   ├── dbt_project.yml           # dbt project configuration
│   ├── sources.yml               # Data source definitions
│   ├── staging/                  # Staging models
│   │   ├── stg_crm.sql
│   │   ├── stg_salesforce.sql
│   │   ├── stg_ga.sql
│   │   └── stg_transactions.sql
│   ├── intermediate/             # Intermediate models
│   │   ├── int_customer_profile.sql
│   │   └── int_customer_activity.sql
│   └── marts/                    # Final dimensional models
│       ├── dim_customer.sql
│       ├── fct_transactions.sql
│       └── customer_360.sql
│
├── validation/                   # Data validation
│   ├── expectations/             # great_expectations configurations
│   └── validate_data.py          # Validation script
│
├── sql_scripts/                  # Helper SQL scripts
│   ├── create_schemas.sql        # Schema creation scripts
│   └── reporting_views.sql       # View definitions for reporting
│
├── docker/                       # Docker configuration
│   ├── Dockerfile                # Base image definition
│   └── docker-compose.yml        # Service configuration
│
└── .github/                      # CI/CD configuration
    └── workflows/
        ├── dbt_test.yml          # Workflow for dbt tests
        └── deploy.yml            # Deployment workflow
```

## ⚙️ Setup and Installation

### Prerequisites
- Docker and Docker Compose
- AWS Account with S3 and Redshift access
- Salesforce Developer Account
- Python 3.8+

### Getting Started

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/customer_360.git
cd customer_360
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. **Start the local environment**
```bash
docker-compose up -d
```

4. **Initialize Airflow connections**
```bash
docker-compose exec airflow airflow connections add 'aws_default' \
    --conn-type 'aws' \
    --conn-login '<your-access-key>' \
    --conn-password '<your-secret-key>' \
    --conn-extra '{"region_name": "us-east-1"}'
```

5. **Initialize dbt**
```bash
cd models
dbt deps
dbt seed
```

## 📊 Data Models

### Core Models

#### Customer 360 Unified Profile
- Combines data from all sources into a single customer view
- Includes demographic, behavioral, and transactional data
- Provides a 360-degree view of the customer journey

#### Customer Engagement Metrics
- Tracks customer interactions across channels
- Calculates engagement scores and activity levels
- Identifies preferred communication channels

#### Channel Attribution
- Attributes conversions to marketing channels
- Provides insight into the customer acquisition journey
- Helps optimize marketing spend

## 🔍 Monitoring & CI/CD

- **GitHub Actions**: Automated testing and deployment
- **Docker**: Containerized environment for consistent execution
- **dbt tests**: Data quality and integrity validation
- **Airflow monitoring**: DAG execution tracking and alerts

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

If you have any questions or want to contribute, please reach out!

---

*This README is part of the Customer 360 Data Integration Project*
