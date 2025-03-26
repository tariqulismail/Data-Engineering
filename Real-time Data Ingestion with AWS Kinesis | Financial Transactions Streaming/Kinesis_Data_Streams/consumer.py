import boto3
import json

# AWS Kinesis client
kinesis_client = boto3.client('kinesis', aws_access_key_id='aws_access_key_id',
                                 aws_secret_access_key='aws_access_key_id',
                              region_name='us-east-1')
# Stream Name
stream_name = 'financial-transactions-stream'

# Get shard iterator
response = kinesis_client.describe_stream(StreamName="financial-transactions-stream")
shard_id = response['StreamDescription']['Shards'][0]['ShardId']
shard_iterator = kinesis_client.get_shard_iterator(
    StreamName="financial-transactions-stream",
    ShardId=shard_id,
    ShardIteratorType='LATEST'
)['ShardIterator']

# Read data continuously
while True:
    records_response = kinesis_client.get_records(ShardIterator=shard_iterator, Limit=10)
    shard_iterator = records_response['NextShardIterator']

    for record in records_response['Records']:
        transaction = json.loads(record['Data'])
        print(f"Received Transaction: {transaction}")