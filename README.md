# AI-Powered Security Operations Center (SOC) Analyst

An end-to-end, full-stack cybersecurity platform that automates threat detection and incident response using real-time data streaming and AI correlation.

## 🚀 The Elevator Pitch
This system simulates a corporate network under attack. It catches live security logs, streams them through a high-speed data pipeline (Kafka), stores them (Elasticsearch), and displays them on a live Next.js dashboard. Behind the scenes, an integrated open-source AI (Llama 3.1) automatically reads the logs, connects the dots between isolated events, and writes professional incident reports warning human analysts of coordinated attacks.

## 💼 Enterprise Business Value

If integrated into a live corporate environment, this architecture solves three major SOC challenges:

1. **Eliminates Alert Fatigue:** Security tools generate tens of thousands of alerts daily. This AI acts as an automated Tier-1 Analyst, filtering out background noise and only flagging the human team when it spots a real, coordinated attack chain.
2. **Reduces MTTD and MTTR:** Decreases Mean Time to Detect and Respond from hours to seconds. The moment an IP address fails an SSH login and immediately triggers unauthorized beaconing, the AI correlates it instantly.
3. **Ensures Data Privacy:** By utilizing local, open-source Large Language Models (LLMs) via Groq/Ollama, highly sensitive network logs are never sent to public APIs like ChatGPT, maintaining strict compliance with GDPR and HIPAA.

## 🏗️ Technical Architecture
* **Data Ingestion:** Python & Apache Kafka (Real-time log streaming)
* **Storage:** Elasticsearch (High-performance NoSQL indexing)
* **Backend:** FastAPI (REST API routing)
* **AI Engine:** Groq API / Llama 3.1 (Automated incident correlation)
* **Frontend:** Next.js, React, Tailwind CSS, Recharts (Interactive UI)

## 🛠️ How to Run Locally

**1. Start the Infrastructure (Docker)**
```bash
docker-compose up -d