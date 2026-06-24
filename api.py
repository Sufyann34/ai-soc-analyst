from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from elasticsearch import Elasticsearch

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

es = Elasticsearch(["http://localhost:9200"])
INDEX_NAME = "security-alerts"

@app.get("/api/alerts")
def get_alerts(limit: int = 50):
    query = {
        "query": {"match_all": {}},
        "size": limit,
        "sort": [{"timestamp": {"order": "desc"}}]
    }
    try:
        response = es.search(index=INDEX_NAME, body=query)
        alerts = [hit["_source"] for hit in response["hits"]["hits"]]
        return {"status": "success", "total": len(alerts), "data": alerts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))