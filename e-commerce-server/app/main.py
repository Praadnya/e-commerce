from fastapi import FastAPI, HTTPException
from rdflib import Graph, Namespace, RDF
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from collections import defaultdict
import numpy as np
from scipy.spatial.distance import euclidean

def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union

def cosine_similarity(set1, set2):
    # Create a combined set of elements
    combined = list(set1.union(set2))
    # Create vectors
    vec1 = [1 if elem in set1 else 0 for elem in combined]
    vec2 = [1 if elem in set2 else 0 for elem in combined]
    # Calculate cosine similarity
    dot_product = np.dot(vec1, vec2)
    norm_a = np.linalg.norm(vec1)
    norm_b = np.linalg.norm(vec2)
    return dot_product / (norm_a * norm_b)

def euclidean_distance(set1, set2):
    # Create a combined set of elements
    combined = list(set1.union(set2))
    # Create vectors
    vec1 = np.array([1 if elem in set1 else 0 for elem in combined])
    vec2 = np.array([1 if elem in set2 else 0 for elem in combined])
    # Calculate Euclidean distance
    return euclidean(vec1, vec2)


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

@app.get("/classes")
async def get_classes():
    query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?class
    WHERE {
        ?class rdf:type owl:Class .
        FILTER (STRSTARTS(STR(?class), "http://"))
        FILTER NOT EXISTS {
            ?subclass rdfs:subClassOf ?class .
            FILTER (STRSTARTS(STR(?subclass), "http://"))
        }
    }
    """
    results = g.query(query, initNs={"rdf": RDF, "owl": Namespace("http://www.w3.org/2002/07/owl#"), "rdfs": Namespace("http://www.w3.org/2000/01/rdf-schema#")})
    classes = [str(row["class"]) for row in results]
    return classes

class InstanceData(BaseModel):
    class_name: str

@app.post("/instances")
async def get_instances(data: InstanceData):
    class_name = data.class_name

    query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ex:  <http://book_triples.org/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX gr: <http://purl.org/goodrelations/v1#>
    PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
    PREFIX : <http://www.semanticweb.org/user/ontologies/2021/1/e-commerce#>
    SELECT ?instance
    WHERE {
        ?instance rdf:type <#PLACEHOLDER#> .
    }
    """

    query = query.replace("#PLACEHOLDER#", class_name)

    results = g.query(query, initNs={"rdf": RDF, "owl": Namespace("http://www.w3.org/2002/07/owl#")})
    instances = [str(row["instance"]) for row in results]
    return instances

class SimilarityRequest(BaseModel):
    instance1: str
    instance2: str

@app.post("/similarity")
async def get_similarity(request: SimilarityRequest):
    instance1 = request.instance1
    instance2 = request.instance2

    if instance1 == instance2:
        raise HTTPException(status_code=400, detail="Instances must be different")

    properties1 = get_instance_properties(instance1)
    properties2 = get_instance_properties(instance2)

    if not properties1 or not properties2:
        raise HTTPException(status_code=404, detail="Instance properties not found")

    # Convert properties to hashable format (tuples of property and value)
    set1 = set((prop, val) for prop, vals in properties1.items() for val in vals)
    set2 = set((prop, val) for prop, vals in properties2.items() for val in vals)


    similarity_scores = {
        "jaccard_similarity": jaccard_similarity(set1, set2),
        "cosine_similarity": cosine_similarity(set1, set2),
        "euclidean_distance": euclidean_distance(set1, set2)
    }

    return similarity_scores


def get_instance_properties(instance):
    query = f"""
    SELECT ?property ?value
    WHERE {{
        <{instance}> ?property ?value .
    }}
    """
    results = g.query(query)
    properties = defaultdict(list)
    for row in results:
        properties[str(row.property)].append(str(row.value))
    return properties

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
