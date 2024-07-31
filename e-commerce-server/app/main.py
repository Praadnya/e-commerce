# app/main.py
from fastapi import FastAPI, HTTPException
from rdflib import Graph
from fastapi.middleware.cors import CORSMiddleware
from sparql_queries import queries

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def load_graph():
    global g
    g = Graph()
    g.parse("e-commerce.ttl", format="ttl")

@app.get("/execute_query")
def execute_query(query_name: str):
    if query_name not in queries:
        raise HTTPException(status_code=404, detail="Query not found")

    sparql_query = queries[query_name]
    result = g.query(sparql_query)
    return {
        "query_name": query_name,
        "results": [str(row) for row in result]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
