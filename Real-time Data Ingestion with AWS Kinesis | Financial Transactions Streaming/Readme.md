# AWS Kinesis Data Streams - Real-time Financial Transactions

## Overview

This project demonstrates real-time data ingestion using **AWS Kinesis Data Streams**. It includes a **producer** to send financial transactions and a **consumer** to process the transactions from Kinesis using Python (Boto3). The project is designed to simulate real-world financial transaction processing with anomaly detection capabilities.

## Features

- **Real-time Data Ingestion** using AWS Kinesis Data Streams
- **Producer** generates financial transaction data
- **Consumer** reads and processes transaction data from Kinesis
- **Uses Trim Horizon starting position** to fetch all available data from the beginning
- **Extensible** for further analytics, anomaly detection, and visualization

## Architecture

1. **Producer:** Generates synthetic financial transactions and sends them to Kinesis Data Stream.
2. **Kinesis Data Stream:** Stores and streams transaction data in real-time.
3. **Consumer:** Reads transactions from Kinesis, processes them, and prints/logs the output.

## Installation & Setup

### Prerequisites

- Python 3.x
- AWS CLI configured with necessary permissions
- Boto3 (AWS SDK for Python)

### Install Dependencies

```sh
pip install boto3
```

## Running the Project

### Step 1: Create a Kinesis Data Stream

Run the following AWS CLI command to create a Kinesis Data Stream:

```sh
aws kinesis create-stream --stream-name financial-transactions-stream --shard-count 1
```

### Step 2: Run the Producer

```sh
python producer.py
```

This script generates transaction data and sends it to Kinesis.

### Step 3: Run the Consumer

```sh
python consumer.py
```

This script reads data from Kinesis and processes it.

## Configuration

Ensure your AWS credentials are configured properly in `~/.aws/credentials` or use environment variables:

```sh
export AWS_ACCESS_KEY_ID=your-access-key
export AWS_SECRET_ACCESS_KEY=your-secret-key
export AWS_REGION=us-east-1
```

## File Structure

```
📂 Kinesis_Data_Streams
 ├── producer.py  # Sends transactions to Kinesis
 ├── consumer.py  # Reads transactions from Kinesis
 ├── README.md    # Project documentation
```

## AWS IAM Permissions Required

Ensure the IAM role or user has the following permissions:

```json
{
  "Effect": "Allow",
  "Action": [
    "kinesis:PutRecord",
    "kinesis:PutRecords",
    "kinesis:GetRecords",
    "kinesis:GetShardIterator",
    "kinesis:DescribeStream"
  ],
  "Resource": "arn:aws:kinesis:us-east-1:YOUR_ACCOUNT_ID:stream/financial-transactions-stream"
}
```

## Future Enhancements

- Implement **Apache Flink** for real-time processing and anomaly detection.
- Store processed data in **AWS S3** or **DynamoDB** for further analysis.
- Visualize transaction insights using **Amazon QuickSight** or **Power BI**.

## License

This project is licensed under the MIT License.

---

Feel free to contribute or raise issues!

🚀 Happy Coding! 🎯

