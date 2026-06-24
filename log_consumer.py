import json
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch

# 1. Initialize Elasticsearch client pointing to our local Docker container
es = Elasticsearch(["http://localhost:9200"])

# 2. Initialize Kafka Consumer to read from the 'security-logs' topic
consumer = KafkaConsumer(
    'security-logs',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',  # Start reading from the beginning of the queue if available
    enable_auto_commit=True,       # Automatically acknowledge messages
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

INDEX_NAME = "security-alerts"

def start_consumer():
    print(f"[*] Connecting to Elasticsearch...")
    # Verify connection to Elasticsearch before listening to Kafka
    if es.ping():
        print("[+] Successfully connected to Elasticsearch!")
    else:
        print("[-] Critical Error: Could not connect to Elasticsearch.")
        return

    print(f"[*] Monitoring Kafka topic 'security-logs'. Waiting for incoming alerts...")
    
    # 3. Process the live message stream
    for message in consumer:
        log_data = message.value
        event_id = log_data.get("event_id")
        severity = log_data.get("severity", "INFO").upper()
        source = log_data.get("log_source", "UNKNOWN").upper()
        action = log_data.get("event", {}).get("action", "UNKNOWN")

        # Index the log into Elasticsearch
        try:
            response = es.index(index=INDEX_NAME, id=event_id, document=log_data)
            print(f"[✓] Stored in ES -> Index: {INDEX_NAME} | ID: {event_id} | {source} | {severity} | Action: {action}")
        except Exception as e:
            print(f"[-] Failed to index log {event_id}: {e}")

if __name__ == "__main__":
    try:
        start_consumer()
    except KeyboardInterrupt:
        print("\n[-] Consumer service stopped safely.")