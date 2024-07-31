# app/sparql_queries.py
queries = {
   "Bought-Together": """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX gr: <http://purl.org/goodrelations/v1#>
PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
PREFIX : <http://www.semanticweb.org/user/ontologies/2021/1/e-commerce#>

SELECT DISTINCT ?product1 ?product2 ?user ?datetime
WHERE {
?buy1 :ofProduct ?p1;
:ofProduct ?p2;
a :ProductBuying;
:performedByUser ?user;
:actionDatetime ?datetime.
?p1 gr:name ?product1.
?p2 gr:name ?product2.
#avoid duplicates
FILTER (?product1 < ?product2)
}
    """,
    "Gold-Customers-infos": """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX gr: <http://purl.org/goodrelations/v1#>
PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
PREFIX : <http://www.semanticweb.org/user/ontologies/2021/1/e-commerce#>

SELECT DISTINCT ?user_account ?name ?birthday ?gender ?country
(COUNT (?buy) AS ?n_buy) (SUM (?spent) AS ?total_spent)
WHERE {
#Gather info about people and accounts
?user_account a foaf:OnlineEcommerceAccount.
?user a foaf:Person;
foaf:name ?name;
foaf:birthday ?birthday;
foaf:gender ?gender;
foaf:account ?user_account.
#Buying activity of these users
?buy a :ProductBuying;
:performedByUser ?user_account;
:totalImport ?spent;
:deliveryLocation ?delivery_location.
?delivery_location :locatedInCity ?city.
?city :locatedInCountry ?country. }
GROUP BY ?user_account ?name ?birthday ?gender ?country
ORDER BY DESC (?total_spent)
    """,
"One-Category-Buyers":"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX gr: <http://purl.org/goodrelations/v1#>
PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
PREFIX : <http://www.semanticweb.org/user/ontologies/2021/1/e-commerce#>

SELECT DISTINCT ?username ?category
WHERE {
?buy a :ProductBuying;
:performedByUser ?username;
:ofProduct ?p.
?p a ?type.
?type rdfs:subClassOf ?category.
?category rdfs:subClassOf :Product.
FILTER (?category != owl:NamedIndividual)
FILTER ( NOT EXISTS {
?buy2 a :ProductBuying;
:performedByUser ?username;
:ofProduct ?p2.
?p2 a ?type2.
?type2 rdfs:subClassOf ?category2.
FILTER (?category2 != ?category) } )
}""",
"Product-Recommendation":"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX gr: <http://purl.org/goodrelations/v1#>
PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
PREFIX : <http://www.semanticweb.org/user/ontologies/2021/1/e-commerce#>

SELECT DISTINCT ?product_name ?price
WHERE {
?buy a :ProductBuying;
:performedByUser :Cristian_the_gamer;
:ofProduct ?product.
?product gr:name ?product_name;
:hasPrice ?price;
FILTER ( !EXISTS {
?buy2 a :ProductBuying;
:performedByUser :alessioNeri87;
:ofProduct ?product. })
}""",
"Product-Retrieval":"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX gr: <http://purl.org/goodrelations/v1#>
PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
PREFIX : <http://www.semanticweb.org/user/ontologies/2021/1/e-commerce#>

SELECT DISTINCT ?property ?value
WHERE {
:B07HN8WJN7 ?property ?value
FILTER ( ?property != rdf:type )
}""",
"Related-Products":"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX gr: <http://purl.org/goodrelations/v1#>
PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
PREFIX : <http://www.semanticweb.org/user/ontologies/2021/1/e-commerce#>

SELECT DISTINCT ?productID ?name ?price ?brand ?category
WHERE { #Products of the same category
{:B08L5PKKRJ a ?category.
?productID a ?category;
gr:name ?name;
gr:hasBrand ?brand;
:hasPrice ?price.
FILTER (?productID != :B08L5PKKRJ) }
UNION #Products of the same brand
{?productID a ?category;
gr:name ?name;
gr:hasBrand ?brand;
:hasPrice ?price.
:B08L5PKKRJ gr:hasBrand ?brand. }
FILTER (?category != owl:NamedIndividual) }""",
"Similar-Customers-Brand":"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX gr: <http://purl.org/goodrelations/v1#>
PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
PREFIX : <http://www.semanticweb.org/user/ontologies/2021/1/e-commerce#>

SELECT DISTINCT ?user1 ?user2 ?brand (COUNT (?action) AS ?n_actions)
WHERE {
?action a ?actionClass;
:ofProduct ?p1;
:performedByUser ?user1.
?action2 a ?actionClass;
:ofProduct ?p2;
:performedByUser ?user2.
?user1 foaf:accountName ?name1.
?user2 foaf:accountName ?name2.
#They like the same brands
?p1 gr:name ?product;
gr:hasBrand ?brand.
?p2 gr:name ?product;
gr:hasBrand ?brand.
?actionClass rdfs:subClassOf :UserAction.
#To avoid duplicates (<x,y> and <y,x>)
FILTER (?name1 < ?name2) }
GROUP BY ?user1 ?user2 ?brand""",
"Similar-Customers-Purchases":"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX gr: <http://purl.org/goodrelations/v1#>
PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
PREFIX : <http://www.semanticweb.org/user/ontologies/2021/1/e-commerce#>

SELECT ?user1 ?user2 (COUNT (?product) AS ?n_common_products)
WHERE {
?buy a :ProductBuying;
:ofProduct ?p;
:performedByUser ?user1.
?buy2 a :ProductBuying;
:ofProduct ?p;
:performedByUser ?user2.
?user1 foaf:accountName ?name1.
?user2 foaf:accountName ?name2.
?p gr:name ?product.
#To avoid duplicates (<x,y> and <y,x>)
FILTER (?name1 < ?name2) }
GROUP BY ?user1 ?user2""",
"User-History":"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX gr: <http://purl.org/goodrelations/v1#>
PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
PREFIX : <http://www.semanticweb.org/user/ontologies/2021/1/e-commerce#>

SELECT ?datetime ?action ?product
WHERE {
?a :performedByUser :Cristian_the_gamer;
a ?action;
:actionDatetime ?datetime;
:ofProduct ?p.
?p gr:name ?product.
FILTER (?action != owl:NamedIndividual)
}
ORDER BY ?datetime""",
"Verified-Purchase":"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX gr: <http://purl.org/goodrelations/v1#>
PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
PREFIX : <http://www.semanticweb.org/user/ontologies/2021/1/e-commerce#>

SELECT ?review ?user ?product
WHERE {
?review a :ProductReview;
:ofProduct ?product;
:performedByUser ?user.
?buy a :ProductBuying;
:ofProduct ?product;
:performedByUser ?user.
}"""
}
