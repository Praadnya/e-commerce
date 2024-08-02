from fastapi import FastAPI, HTTPException
from rdflib import Graph, Namespace, RDF
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from collections import defaultdict

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
    SELECT ?class
    WHERE {
        ?class rdf:type owl:Class .
        FILTER NOT EXISTS {
            ?subclass rdfs:subClassOf ?class .
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

    # Calculate Jaccard similarity between the sets of properties
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    
    if len(union) == 0:
        similarity_score = 0.0
    else:
        similarity_score = len(intersection) / len(union)

    return {"similarity_score": similarity_score}


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
