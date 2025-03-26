import boto3
import json
import time
import random
from datetime import datetime


# ✅ Initialize Kinesis client
kinesis_client = boto3.client('kinesis', aws_access_key_id='aws_access_key_id',
                                 aws_secret_access_key='aws_secret_access_key',
                              region_name='us-east-1')
# Stream Name
stream_name = 'financial-transactions-stream'

# Simulate real-time transactions
def generate_transaction():
    return {
        "transaction_id": random.randint(100000, 999999),
        "user_id": random.randint(1000, 9999),
        "amount": round(random.uniform(10.0, 5000.0), 2),
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "location": random.choice(["New York", "San Francisco", "Chicago", "London"]),
        "fraud_flag": random.choice([0, 1])  # 1 = Fraud, 0 = Normal
    }


# ✅ Define the function properly before calling it
def send_transaction():
    transaction = generate_transaction()
    response = kinesis_client.put_record(
        StreamName="financial-transactions-stream",
        Data=json.dumps(transaction),
        PartitionKey=str(transaction["user_id"])  # Distributes data across shards
    )
    print("Sent transaction:", transaction)
    print("Response:", response)

# ✅ Call function inside __main__
if __name__ == "__main__":
    send_transaction()