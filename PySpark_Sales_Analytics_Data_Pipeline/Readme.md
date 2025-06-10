# Sales Analytics Data Pipeline with PySpark and Star Schema Modeling

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![PySpark](https://img.shields.io/badge/PySpark-3.5+-orange.svg)](https://spark.apache.org)
[![SQL](https://img.shields.io/badge/SQL-MySQL%208.0+-green.svg)](https://mysql.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Project Overview

This project demonstrates a production-ready ETL/ELT data pipeline that transforms raw sales transaction data into a comprehensive star-schema modeled data warehouse using PySpark, SQL, and data engineering best practices. The pipeline handles large-scale datasets with robust data quality validation, optimization, and monitoring capabilities.

### 🏆 Key Achievements
- **Scale**: Processes 100K+ sales transactions across 10K customers, 1K products, and 100 locations
- **Performance**: Optimized PySpark transformations with partitioning and caching strategies
- **Quality**: Comprehensive data validation with 20+ quality checks and business rule enforcement
- **Architecture**: Industry-standard star schema with fact and dimension tables
- **Monitoring**: Built-in data quality monitoring and ETL job logging

## 📋 Table of Contents
- [Architecture](#-architecture)
- [Data Model](#-data-model)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Pipeline Details](#-pipeline-details)
- [Data Quality](#-data-quality)
- [Performance Optimization](#-performance-optimization)
- [Monitoring & Validation](#-monitoring--validation)
- [Business Intelligence Views](#-business-intelligence-views)
- [Contributing](#-contributing)

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │    │  ETL Pipeline   │    │  Data Warehouse │
│                 │    │                 │    │                 │
│ • sales.csv     │───▶│ • Data Extract  │───▶│ • fact_sales    │
│ • customers.csv │    │ • Transform     │    │ • dim_customers │
│ • products.csv  │    │ • Validate      │    │ • dim_products  │
│ • locations.csv │    │ • Load          │    │ • dim_locations │
│                 │    │                 │    │ • dim_dates     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │                        │
                              ▼                        ▼
                    ┌─────────────────┐    ┌─────────────────┐
                    │ Data Validation │    │ BI Views & Apps │
                    │ & Quality Checks│    │ • Power BI      │
                    └─────────────────┘    │ • Analytics     │
                                          └─────────────────┘
```

## 📊 Data Model

### Star Schema Design

The data warehouse implements a classic star schema optimized for analytical queries:

```
                    ┌─────────────────┐
                    │   dim_dates     │
                    │ • date_id (PK)  │
                    │ • full_date     │
                    │ • year, month   │
                    │ • quarter       │
                    │ • day_name      │
                    │ • is_weekend    │
                    │ • season        │
                    └─────────┬───────┘
                              │
┌─────────────────┐          │          ┌─────────────────┐
│  dim_customers  │          │          │  dim_products   │
│ • customer_id   │          │          │ • product_id    │
│ • full_name     │          │          │ • product_name  │
│ • email         │          │          │ • category      │
│ • age_group     │          │          │ • brand         │
│ • segment       │          │          │ • unit_price    │
│ • loyalty_pts   │          │          │ • profit_margin │
└─────────┬───────┘          │          └─────────┬───────┘
          │                  │                    │
          │     ┌─────────────────────────┐       │
          │     │      fact_sales         │       │
          └────▶│ • transaction_id (PK)   │◀──────┘
                │ • customer_id (FK)      │
                │ • product_id (FK)       │
                │ • location_id (FK)      │
                │ • date_id (FK)          │
                │ • quantity              │
                │ • unit_price            │
                │ • gross_amount          │
                │ • discount_amount       │
                │ • revenue               │
                │ • profit                │
                │ • channel               │
                │ • payment_method        │
                └────────┬────────────────┘
                         │
              ┌─────────────────┐
              │  dim_locations  │
              │ • location_id   │
              │ • city, state   │
              │ • region        │
              │ • store_type    │
              │ • store_size    │
              └─────────────────┘
```

## ✨ Features

### 🔄 ETL Pipeline Capabilities
- **Data Extraction**: Robust CSV ingestion with schema validation
- **Data Transformation**: 
  - Deduplication using window functions
  - Null value handling and data type conversions
  - Business rule validation and enforcement
  - Calculated fields (profit, margins, date attributes)
- **Data Loading**: Partitioned storage with optimized indexing

### 📈 Data Quality & Validation
- **Automated Quality Checks**: 20+ validation rules covering:
  - Referential integrity
  - Business rule compliance
  - Data consistency
  - Null value detection
  - Duplicate identification
- **Data Profiling**: Statistical analysis and distribution checks
- **Error Handling**: Comprehensive logging and error recovery

### ⚡ Performance Optimization
- **Spark Optimizations**:
  - Adaptive query execution
  - Automatic coalescing of partitions
  - Strategic caching of frequently used datasets
- **Database Optimizations**:
  - Composite indexes for query patterns
  - Table partitioning by date
  - Query result caching

### 📊 Business Intelligence Ready
- **Pre-built Views**: Ready-to-use analytical views
- **Aggregate Tables**: Pre-calculated metrics for performance
- **KPI Dashboards**: Sample Power BI integration

## 🚀 Quick Start

### Prerequisites
```bash
# Python 3.8+
python --version

# Required packages
pip install pyspark pandas numpy faker
```

### Database Setup (MySQL)
```sql
-- Create database
CREATE DATABASE SalesAnalyticsDW;

-- Run DDL script
mysql -u username -p SalesAnalyticsDW < data_model.sql
```

### Running the Pipeline
```bash
# 1. Generate sample data (already provided)
# Files: sales.csv, customers.csv, products.csv, locations.csv

# 2. Update paths in main.py
# data_path = "/path/to/csv/files"
# output_path = "/path/to/warehouse"

# 3. Execute ETL pipeline
python main.py

# 4. Run validation queries
mysql -u username -p SalesAnalyticsDW < validation_queries.sql
```

## 📁 Project Structure

```
sales-analytics-pipeline/
├── README.md                 # This file
├── main.py                   # Main PySpark ETL pipeline
├── data_model.sql           # Star schema DDL
├── validation_queries.sql   # Data quality validation queries
├── data/                    # Sample datasets
│   ├── sales.csv           # 100K+ sales transactions
│   ├── customers.csv       # 10K customers
│   ├── products.csv        # 1K products
│   └── locations.csv       # 100 store locations
├── docs/                   # Additional documentation
│   ├── ERD_diagram.png     # Entity relationship diagram
│   └── pipeline_flow.png   # Data flow visualization
└── tests/                  # Unit tests (future enhancement)
    └── test_etl.py
```

## 🔧 Pipeline Details

### Extract Phase
```python
# Schema-aware data extraction
sales_schema = StructType([
    StructField("transaction_id", StringType(), False),
    StructField("customer_id", StringType(), False),
    # ... additional fields
])

raw_sales = spark.read \\
    .option("header", "true") \\
    .schema(sales_schema) \\
    .csv("sales.csv")
```

### Transform Phase
```python
# Deduplication with window functions
window_spec = Window.partitionBy("customer_id", "product_id", "transaction_date")
clean_sales = raw_sales \\
    .withColumn("row_num", row_number().over(window_spec)) \\
    .filter(col("row_num") == 1)

# Business calculations
clean_sales = clean_sales \\
    .withColumn("revenue", col("gross_amount") - col("discount_amount")) \\
    .withColumn("profit", col("revenue") - (col("quantity") * col("cost_price")))
```

### Load Phase
```python
# Partitioned storage for performance
fact_sales.write \\
    .mode("overwrite") \\
    .partitionBy("year", "month") \\
    .saveAsTable("fact_sales")
```

## 🔍 Data Quality

### Validation Framework
The pipeline includes comprehensive data quality checks:

| Check Category | Validation Rules | Expected Result |
|---|---|---|
| **Referential Integrity** | Foreign key constraints | 0 orphaned records |
| **Business Rules** | Revenue ≥ 0, Quantity > 0 | 0 violations |
| **Data Consistency** | Calculated fields accuracy | 100% match |
| **Completeness** | Required fields not null | 0 null values |
| **Uniqueness** | Primary key constraints | 0 duplicates |

### Quality Metrics Dashboard
```sql
-- Sample quality score calculation
SELECT 
    'Data Quality Score' as metric,
    ROUND(100 * (1 - total_issues / total_records), 2) as score
FROM (
    SELECT 
        COUNT(*) as total_records,
        SUM(CASE WHEN revenue < 0 THEN 1 ELSE 0 END +
            CASE WHEN quantity <= 0 THEN 1 ELSE 0 END) as total_issues
    FROM fact_sales
) quality_check;
```

## ⚡ Performance Optimization

### Spark Configuration
```python
spark = SparkSession.builder \\
    .appName("SalesAnalyticsETL") \\
    .config("spark.sql.adaptive.enabled", "true") \\
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \\
    .config("spark.sql.adaptive.skewJoin.enabled", "true") \\
    .getOrCreate()
```

### Database Indexing Strategy
```sql
-- Composite indexes for common query patterns
CREATE INDEX idx_fact_sales_date_customer ON fact_sales(date_id, customer_id);
CREATE INDEX idx_fact_sales_date_product ON fact_sales(date_id, product_id);
CREATE INDEX idx_fact_sales_revenue ON fact_sales(revenue);
```

### Partitioning Strategy
- **Fact Table**: Partitioned by year/month for time-based queries
- **Spark DataFrames**: Optimal partition count based on data size
- **Memory Management**: Strategic caching of dimension tables

## 📈 Monitoring & Validation

### ETL Job Monitoring
```sql
-- ETL execution log
CREATE TABLE etl_job_log (
    job_id INT AUTO_INCREMENT PRIMARY KEY,
    job_name VARCHAR(100),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    status ENUM('RUNNING', 'SUCCESS', 'FAILED'),
    records_processed INT,
    error_message TEXT
);
```

### Data Quality Dashboard
The pipeline provides real-time data quality metrics:
- **Record Counts**: Track data volume across all tables
- **Quality Score**: Overall data health percentage
- **Trend Analysis**: Quality metrics over time
- **Alert System**: Notifications for quality threshold breaches

## 📊 Business Intelligence Views

### Pre-built Analytical Views
```sql
-- Comprehensive sales detail view
CREATE VIEW vw_sales_detail AS
SELECT 
    f.transaction_id,
    d.full_date,
    c.customer_name,
    p.product_name,
    p.category,
    l.region,
    f.revenue,
    f.profit
FROM fact_sales f
JOIN dim_dates d ON f.date_id = d.date_id
JOIN dim_customers c ON f.customer_id = c.customer_id
JOIN dim_products p ON f.product_id = p.product_id
JOIN dim_locations l ON f.location_id = l.location_id;
```

### Sample Analytics Queries
```sql
-- Monthly revenue trend with growth rate
WITH monthly_revenue AS (
    SELECT 
        year, month,
        SUM(revenue) as monthly_revenue,
        LAG(SUM(revenue)) OVER (ORDER BY year, month) as prev_month
    FROM vw_sales_detail
    GROUP BY year, month
)
SELECT 
    year, month, monthly_revenue,
    ROUND((monthly_revenue - prev_month) / prev_month * 100, 2) as growth_rate
FROM monthly_revenue;
```

## 🎯 Business Value & Use Cases

### Key Performance Indicators (KPIs)
1. **Revenue Metrics**: Total sales, growth rates, seasonal trends
2. **Customer Analytics**: Segmentation, lifetime value, retention
3. **Product Performance**: Category analysis, profit margins, inventory turnover
4. **Operational Efficiency**: Channel performance, regional analysis

### Use Case Examples
- **Executive Dashboards**: High-level KPI monitoring
- **Sales Analytics**: Territory and rep performance analysis
- **Customer Insights**: Behavior analysis and segmentation
- **Inventory Management**: Product performance and demand forecasting
- **Financial Reporting**: Revenue recognition and profitability analysis

## 🛠️ Technologies & Skills Demonstrated

### Technical Stack
- **Big Data Processing**: PySpark for large-scale data transformation
- **Database Technologies**: MySQL with advanced SQL techniques
- **Data Modeling**: Dimensional modeling with star schema design
- **Data Quality**: Comprehensive validation and monitoring framework
- **Performance Optimization**: Indexing, partitioning, and query optimization
- **Python Programming**: Advanced pandas, data manipulation, and automation

### Data Engineering Best Practices
- **Schema Evolution**: Flexible schema design for changing requirements
- **Error Handling**: Robust exception handling and logging
- **Code Organization**: Modular, maintainable code structure
- **Documentation**: Comprehensive documentation and commenting
- **Testing**: Data validation and quality assurance
- **Monitoring**: Production-ready monitoring and alerting

## 📊 Sample Results & Insights

### Data Volume
- **Sales Transactions**: 100,100 records (including test duplicates)
- **Customers**: 10,000 unique customers
- **Products**: 1,000 products across 8 categories
- **Locations**: 100 stores across 5 regions
- **Date Range**: 3+ years of historical data (2022-2024)

### Key Insights Generated
- **Revenue Distribution**: Identified top-performing product categories
- **Seasonal Trends**: Detected quarterly sales patterns
- **Customer Segmentation**: Analyzed behavior by demographic groups
- **Geographic Performance**: Regional sales variations
- **Channel Effectiveness**: Online vs in-store performance comparison

## 🔮 Future Enhancements

### Technical Roadmap
1. **Real-time Processing**: Implement streaming ETL with Apache Kafka
2. **Machine Learning**: Add predictive analytics for sales forecasting
3. **Cloud Migration**: Deploy on AWS/Azure with S3/Data Lake integration
4. **API Development**: REST APIs for data access and integration
5. **Advanced Analytics**: Customer lifetime value, churn prediction

### Scalability Improvements
1. **Auto-scaling**: Dynamic resource allocation based on data volume
2. **Data Catalog**: Automated metadata management and lineage tracking
3. **Security**: Row-level security and data masking capabilities
4. **Multi-tenant**: Support for multiple business units or regions

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone repository
git clone https://github.com/tariqulismail/Data-Engineering/PySpark Sales Analytics Data Pipeline.git

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Run pipeline
python main.py
```

## 📞 Support & Contact

For questions, issues, or contributions:
- **GitHub Issues**: [Project Issues Page](https://github.com/tariqulismail/Data-Engineering/PySpark_Sales_Analytics_Data_Pipeline/issues)
- **Documentation**: [Wiki Pages](https://github.com/ariqulismail/Data-Engineering/PySpark_Sales_Analytics_Data_Pipeline/wiki)
- **Email**: connect@tariqulismail.com

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ by the Data Engineering Team**

*This project demonstrates production-ready data engineering skills including ETL/ELT pipeline development, dimensional modeling, data quality management, and performance optimization using modern big data technologies.*
'''
