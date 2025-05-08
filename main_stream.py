import json
import boto3
from datetime import datetime
import time
import pandas as pd
from dataset_builder.default_batch_generator import DefaultBatchGenerator

# --- CONFIGURATIONS ---

USE_REAL_KINESIS = False  # Toggle between mock and real sending
KINESIS_STREAM_NAME = "your-kinesis-stream-name"
AWS_REGION = "us-east-1"

# Define generation schema
schema = [
    {"channel": "call", "interaction_type": "call_transfer", "count": 5},
    {"channel": "chat", "interaction_type": "standard", "count": 3}
]

# --- Sending functions ---

def mock_send_to_kinesis(event: dict):
    print(f"🛰️ Mock sent to Kinesis: {event['interaction_id']} - {event['event_type']}")

def real_send_to_kinesis(event: dict):
    kinesis_client = boto3.client("kinesis", region_name=AWS_REGION)
    response = kinesis_client.put_record(
        StreamName=KINESIS_STREAM_NAME,
        Data=json.dumps(event),
        PartitionKey=event["interaction_id"]
    )
    print(f"✅ Real sent to Kinesis. ShardID: {response['ShardId']}")

def send_event(event: dict):
    if USE_REAL_KINESIS:
        real_send_to_kinesis(event)
    else:
        mock_send_to_kinesis(event)

# --- Initialize generator ---

generator = DefaultBatchGenerator(
    cxm="CXM1",
    apply_anomalies=True,
    anomaly_config_path="config/anomaly_profiles/test_profile.yaml"
)

# --- Streaming loop ---

print("\n🚀 Starting streaming of synthetic events...\n")

streamed_events = []

for event in generator.stream(
    schema=schema,
    base_timestamp=datetime.utcnow(),
    interaction_spacing_seconds=5
):
    print(event)
    streamed_events.append(event)
    send_event(event)
    time.sleep(0.5)

print("\n✅ Streaming finished!")

# --- Export streamed events ---

df_streamed = pd.DataFrame(streamed_events)
df_streamed.to_csv("datasets/streamed_output.csv", index=False)
print("✅ Streamed events saved to datasets/streamed_output.csv")
