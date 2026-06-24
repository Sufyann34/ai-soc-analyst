import os
from elasticsearch import Elasticsearch
from groq import Groq

es = Elasticsearch(["http://localhost:9200"])
INDEX_NAME = "security-alerts"
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def fetch_recent_alerts():
    query = {
        "query": {
            "terms": {
                "severity.keyword": ["medium", "high", "critical"]
            }
        },
        "size": 15,
        "sort": [{"timestamp": {"order": "desc"}}]
    }
    
    try:
        response = es.search(index=INDEX_NAME, body=query)
        return [hit["_source"] for hit in response["hits"]["hits"]]
    except Exception:
        return []

def analyze_with_ai(alerts):
    if not alerts:
        print("No significant alerts found to analyze.")
        return

    prompt = (
        "You are an expert AI Security Operations Center (SOC) Analyst.\n"
        "Analyze the following recent security alerts. Identify if there is a coordinated attack occurring.\n"
        "Provide your output exactly in this format:\n"
        "1. INCIDENT SUMMARY: (1 paragraph)\n"
        "2. ATTACK CHAIN: (Step-by-step bullet points of the suspected attack)\n"
        "3. RECOMMENDATIONS: (3 immediate remediation steps)\n\n"
        "Here are the raw alerts:\n"
    )
    
    for a in alerts:
        source_ip = a.get('source', {}).get('ip', 'Unknown')
        dest_ip = a.get('destination', {}).get('ip', 'Unknown')
        action = a.get('event', {}).get('action', 'Unknown')
        prompt += f"- [{a['timestamp']}] SOURCE: {a['log_source'].upper()} | SEVERITY: {a['severity'].upper()} | ACTION: {action} | SRC_IP: {source_ip} -> DEST_IP: {dest_ip}\n"

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-8b-instant",
        )
        print("\n========== AI INCIDENT REPORT ==========\n")
        print(chat_completion.choices[0].message.content)
        print("\n========================================")
    except Exception as e:
        print(f"AI Generation failed: {e}")

if __name__ == "__main__":
    alerts = fetch_recent_alerts()
    analyze_with_ai(alerts)