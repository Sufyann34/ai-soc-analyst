# AI-Powered Security Operations Center (SOC) Analyst

Built by Muhammad Sufyan.

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

## 📁 Project Structure
```text
ai-soc-analyst/
├── frontend/             # Next.js & React Dashboard UI
│   ├── app/              # Dashboard pages and layout routes
│   └── public/           # Static asset vectors
├── ai_analyst.py         # LLM pipeline engine (Llama 3.1 via Groq)
├── api.py                # FastAPI REST endpoints
├── log_generator.py      # Automated security log simulator
├── log_consumer.py       # Kafka consumer & Elasticsearch indexer
├── docker-compose.yml    # Kafka & Elasticsearch container network
└── requirements.txt      # Python dependencies list
```

## 📋 Prerequisites
Before running this project locally, ensure you have the following installed:
* **Docker & Docker Compose** (For running Kafka and Elasticsearch)
* **Python 3.10+** (For the backend API and data pipelines)
* **Node.js v18+ & npm** (For the Next.js frontend dashboard)

## 🔑 Environment Configuration
Create a `.env` file in the root directory to securely store your AI API credentials. Do not commit this file to version control.
```env
GROQ_API_KEY=your_groq_api_key_here
```

## 🛠️ How to Run Locally

**1. Start the Infrastructure (Docker)**
```bash
docker-compose up -d
```
**2. Start the Data Pipeline**
Open two separate terminal windows and run:
```bash
python3 log_generator.py
python3 log_consumer.py
```
**3. Start the Backend API**
Open a new terminal window and run:
```bash
uvicorn api:app --reload
```

**4. Start the Frontend UI**
Open a new terminal window, navigate to the frontend folder, and start the development server:
```bash
cd frontend
npm run dev
```
The dashboard will now be live at http://localhost:3000.

**5. Generate AI Incident Report**
To trigger the AI to analyze the live database and print a correlated attack report:
```bash
python3 ai_analyst.py
```




