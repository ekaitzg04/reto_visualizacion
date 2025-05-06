# -*- coding: utf-8 -*-
import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
import requests

# Cargar variables de entorno
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)
ES_PORT     = os.getenv("ES_PORT", "9200")
KB_PORT     = os.getenv("KIBANA_PORT", "5601")
ES_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ES_USER     = "elastic"
KB_PASSWORD = os.getenv("KIBANA_PASSWORD")

# Verificar que las variables de entorno existan
if not ES_PASSWORD:
    raise RuntimeError("ELASTIC_PASSWORD no encontrada en .env")
if not KB_PASSWORD:
    raise RuntimeError("KIBANA_PASSWORD no encontrada en .env")

# Cliente de Elasticsearch
es = Elasticsearch(
    f"https://localhost:{ES_PORT}",
    basic_auth=(ES_USER, ES_PASSWORD),
    verify_certs=False
)

# Nombre de índice y comprobación previa
idx = "indice-operaciones-fabrica"
if not es.indices.exists(index=idx):
    es.indices.create(
        index=idx,
        body={
            "settings": {"number_of_shards": 2, "number_of_replicas": 1},
            "mappings": {
                "properties": {
                    "id_máquina":     {"type": "keyword"},
                    "operación":      {"type": "keyword"},
                    "estado":         {"type": "keyword"},
                    "marca_temporal": {"type": "date"},
                    "duración":       {"type": "integer"},
                    "hora":           {"type": "keyword"},
                    "weekday":        {"type": "keyword"},
                    "ubicación":      {"type": "geo_point"}
                }
            }
        }
    )
    print(f"Índice '{idx}' creado con mapping geo_point.")
else:
    print(f"Índice '{idx}' ya existe. No se crea.")

# Definición de fábricas con coordenadas separadas
fabricas = [
    {"nombre": "Madrid",       "lat": 40.4500, "lon": -3.7000},  # Ciudad operativa exclusiva
    {"nombre": "Barcelona",    "lat": 41.3900, "lon": 2.1200},
    {"nombre": "Valencia",     "lat": 39.4700, "lon": -0.3800},
    {"nombre": "Sevilla",      "lat": 37.3850, "lon": -5.9500},
    {"nombre": "Bilbao",       "lat": 43.2630, "lon": -2.9350},
    {"nombre": "Zaragoza",     "lat": 41.6500, "lon": -0.8900},
    {"nombre": "Málaga",       "lat": 36.7200, "lon": -4.4200},
    {"nombre": "A Coruña",     "lat": 43.3700, "lon": -8.4100},
    {"nombre": "Granada",      "lat": 37.1800, "lon": -3.6000},
    {"nombre": "Murcia",       "lat": 37.9920, "lon": -1.1300},
]

machines    = [f"Máquina-{i}" for i in range(1, 21)]
ops         = ["Inicio", "Parada", "Mantenimiento", "Error", "Reinicio"]
stats       = ["Operativa", "No operativa", "En mantenimiento", "Defectuosa"]
weekdays_es = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]

# Ciudad que tendrá únicamente fábricas operativas
especial_ciudad = "Madrid"

# Generación de datos con lógica de estados
def gen(n=100):
    now = datetime.now()
    for _ in range(n):
        # timestamp aleatorio en las últimas 24h
        delta = timedelta(
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )
        ts = now - delta

        fab = random.choice(fabricas)
        geopoint = {"lat": fab["lat"], "lon": fab["lon"]}

        # Estado fijo Operativa para la ciudad especial
        if fab["nombre"] == especial_ciudad:
            estado = "Operativa"
        else:
            estado = random.choice(stats)

        yield {
            "id_máquina":     random.choice(machines),
            "operación":      random.choice(ops),
            "estado":         estado,
            "marca_temporal": ts.isoformat(),
            "duración":       random.randint(1, 120),
            "hora":           str(ts.hour),
            "weekday":        random.choice(weekdays_es),
            "ubicación":      geopoint
        }

# Inserción de datos
for doc in gen(100):
    r = es.index(index=idx, document=doc)
    print("Insertado:", r["_id"])  
print("✅ Inserción completa.")

# Lógica mejorada para Data View en Kibana
kb_base = f"http://localhost:{KB_PORT}/api/data_views"

# Comprobar si ya existe la Data View
find_url = f"{kb_base}/_find?search={idx}&type=index_pattern"
resp_find = requests.get(
    find_url,
    auth=(ES_USER, KB_PASSWORD),
    headers={"kbn-xsrf": "true"}
)
if resp_find.status_code == 200 and resp_find.json().get("total", 0) > 0:
    print(f"✅ Data View para índice '{idx}' ya existe.")
else:
    # Crear Data View
    create_url = f"{kb_base}/data_view"
    payload = {
        "data_view": {
            "title": idx,
            "timeFieldName": "marca_temporal",
            "name": idx
        }
    }
    resp_create = requests.post(
        create_url,
        json=payload,
        auth=(ES_USER, KB_PASSWORD),
        headers={"kbn-xsrf": "true"}
    )
    if resp_create.status_code in (200, 201):
        print(f"✅ Data View '{idx}' creado en Kibana.")
    else:
        print(f"❌ Error al crear Data View: {resp_create.status_code} {resp_create.text}")
