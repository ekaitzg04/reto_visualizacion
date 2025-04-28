from elasticsearch import Elasticsearch

# Crear cliente de Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Documento a indexar
doc = {
    "titulo": "Operación de fábrica",
    "descripcion": "Detalles de la operación en la fábrica"
}

# Intentar indexar el documento
res = es.index(index="indice-operaciones-fabrica", document=doc, headers={"Content-Type": "application/json"})
print(res)

if not es.indices.exists(index="indice-operaciones-fabrica"):
    es.indices.create(index="indice-operaciones-fabrica")
