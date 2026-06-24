import json
import time
import random
import uuid
from datetime import datetime
from kafka import KafkaProducer

# Initialize Kafka Producer pointing to our local Docker container
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TOPIC_NAME = 'security-logs'

# Sample entities to make logs look authentic
USERS = ['admin', 'm_sufyan', 'j_doe', 'svc_prod', 'root', 'guest']
IP_POOL = [f'192.168.1.{i}' for i in range(10, 250)]
PUBLIC_IPS = ['185.220.101.5', '45.133.193.22', '92.44.12.89', '104.244.42.1']
COMPROMISED_HOSTS = ['prod-web-server-01', 'db-primary-node', 'hr-portal-vm']

def generate_base_log(source_type, severity, action, message, src_ip, dest_ip, user=None):
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event_id": str(uuid.uuid4()),
        "log_source": source_type,
        "severity": severity,
        "event": {
            "action": action,
            "outcome": "success" if severity in ["low", "info"] else "failure",
            "message": message
        },
        "source": {
            "ip": src_ip,
            "user": user or random.choice(USERS)
        },
        "destination": {
            "ip": dest_ip,
            "host": random.choice(COMPROMISED_HOSTS)
        }
    }

def stream_logs():
    print(f"[*] Starting Security Log Generator. Streaming live to Kafka topic: '{TOPIC_NAME}'...")
    
    while True:
        # 85% chance to generate normal background noise, 15% chance for malicious anomalies
        is_attack = random.random() < 0.15
        
        if not is_attack:
            # Generate Standard, Healthy Network Noise
            log = generate_base_log(
                source_type=random.choice(["firewall", "edr", "cloudtrail"]),
                severity="info",
                action="user_login" if random.random() > 0.5 else "network_connection_allowed",
                message="Session established successfully" if random.random() > 0.5 else "Inbound traffic cleared by ACL rules",
                src_ip=random.choice(IP_POOL),
                dest_ip="10.0.0.5"
            )
        else:
            # Generate High-Value Security Alerts for our AI to correlate later
            attack_type = random.choice(["brute_force", "exfiltration", "malware_execution"])
            attacker_ip = random.choice(PUBLIC_IPS)
            target_host_ip = "10.0.0.100"
            
            if attack_type == "brute_force":
                log = generate_base_log(
                    source_type="edr",
                    severity="high",
                    action="ssh_login_failed",
                    message="Multiple invalid authentication attempts detected within 5 seconds.",
                    src_ip=attacker_ip,
                    dest_ip=target_host_ip,
                    user="root"
                )
            elif attack_type == "exfiltration":
                log = generate_base_log(
                    source_type="cloudtrail",
                    severity="critical",
                    action="s3_bucket_data_download",
                    message="Massive outbound data transfer threshold exceeded on sensitive cloud storage bucket.",
                    src_ip=attacker_ip,
                    dest_ip="10.0.0.200",
                    user="admin"
                )
            else:
                log = generate_base_log(
                    source_type="firewall",
                    severity="medium",
                    action="unauthorized_beaconing",
                    message="Internal asset communicating directly with known malicious Tor exit node infrastructure.",
                    src_ip=random.choice(IP_POOL),
                    dest_ip=attacker_ip
                )

        # Send to Kafka
        producer.send(TOPIC_NAME, value=log)
        print(f"[{log['timestamp']}] Sent -> {log['log_source'].upper()} | Severity: {log['severity'].upper()} | Action: {log['event']['action']}")
        
        # Adjust delay to simulate continuous live ingestion
        time.sleep(random.uniform(0.2, 1.5))

if __name__ == "__main__":
    try:
        stream_logs()
    except KeyboardInterrupt:
        print("\n[-] Log generation stopped safely.")