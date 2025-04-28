from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
import random
import json

# Conexión a Elasticsearch 8.x
es = Elasticsearch(
    "http://localhost:9200",
    verify_certs=False
)

# Datos simulados de máquinas y operaciones
machine_ids = [f'Máquina-{i}' for i in range(1, 21)]
operations = ['Inicio', 'Parada', 'Mantenimiento', 'Error', 'Reinicio']
statuses = ['Operativa', 'No operativa', 'En mantenimiento', 'Defectuosa']

# Función para generar datos de ejemplo
def generate_data():
    timestamps = [datetime.now() - timedelta(hours=i) for i in range(100)]
    for _ in range(100):
        doc = {
            'id_máquina': random.choice(machine_ids),
            'operación': random.choice(operations),
            'estado': random.choice(statuses),
            'marca_temporal': random.choice(timestamps).isoformat(),
            'duración': random.randint(1, 120)
        }
        yield doc

# Insertar los datos generados
for doc in generate_data():
    res = es.index(index="indice-operaciones-fabrica", document=doc)
    print(f'ID del documento: {res["_id"]} insertado.')

print("✅ Inserción de datos completa.")
