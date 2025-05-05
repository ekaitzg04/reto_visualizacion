import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
import requests

# Cargar variables de entorno
load_dotenv()
ES_PORT  = os.getenv("ES_PORT", "9200")
KB_PORT  = os.getenv("KIBANA_PORT", "5601")
PASSWORD = os.getenv("ELASTIC_PASSWORD")
PASSWORD_kibana = os.getenv("KIBANA_PASSWORD")
KB_USER  = "elastic"

# Cliente de Elasticsearch
es = Elasticsearch(
    f"https://localhost:{ES_PORT}",
    basic_auth=("elastic", PASSWORD),
    verify_certs=False
)

# Nombre de índice y comprobación previa
idx = "indice-operaciones-fabrica"
exists = es.indices.exists(index=idx)
print(f"¿Existe el índice '{idx}'? {exists}")

# Crear índice solo si no existe
if not exists:
    es.indices.create(
        index=idx,
        body={
            "settings": {"number_of_shards":1, "number_of_replicas":0},
            "mappings": {
                "properties": {
                    "id_máquina":     {"type":"keyword"},
                    "operación":      {"type":"keyword"},
                    "estado":         {"type":"keyword"},
                    "marca_temporal": {"type":"date"},
                    "duración":       {"type":"integer"},
                    "hora":           {"type":"keyword"},
                    "weekday":        {"type":"keyword"},
                    "ciudad":         {"type":"keyword"}
                }
            }
        }
    )
    print(f"Índice '{idx}' creado.")
else:
    print(f"No se crea el índice porque ya existe.")

# Datos de ejemplo
machines    = [f"Máquina-{i}" for i in range(1,21)]
ops         = ["Inicio", "Parada", "Mantenimiento", "Error", "Reinicio"]
stats       = ["Operativa", "No operativa", "En mantenimiento", "Defectuosa"]
weekdays_es = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

# Generación de datos
def gen(n=100):
    now = datetime.now()
    for _ in range(n):
        # timestamp aleatorio en las últimas 24h
        delta = timedelta(
            hours=random.randint(0,23),
            minutes=random.randint(0,59),
            seconds=random.randint(0,59)
        )
        ts = now - delta

        yield {
            "id_máquina":     random.choice(machines),
            "operación":      random.choice(ops),
            "estado":         random.choice(stats),
            "marca_temporal": ts.isoformat(),
            "duración":       random.randint(1,120),
            "hora":           random.randint(0,23),
            "weekday":        random.choice(weekdays_es),
        }

# Inserción de datos
for doc in gen(100):
    r = es.index(index=idx, document=doc)
    print("Insertado:", r["_id"])
print("✅ Inserción completa.")

# Creación de Data View en Kibana
kb_url = f"http://localhost:{KB_PORT}/api/data_views/data_view"
payload = {
    "data_view": {
        "title": idx,
        "timeFieldName": "marca_temporal",
        "name": "indice"
    }
}
resp = requests.post(
    kb_url,
    json=payload,
    auth=("elastic", PASSWORD),
    headers={"kbn-xsrf": "true"}
)
if resp.status_code in (200, 201):
    print("✅ Data View 'indice' creado en Kibana.")
else:
    print(f"❌ Error al crear Data View: {resp.status_code} {resp.text}")
