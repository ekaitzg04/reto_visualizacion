# reto_visualizacion

## Pasos seguidos
### Script - docker-compose.yml
Archivo de configuración que permite lanzar de forma automática elastic y kibana. Al cual le hemos añadido un servicio llamado setup que se encarga de dotar de seguridad tanto a kibana como a elastic. Se ha usado la versión 8.7.0 de elastic.

### Script - introducir_datos.py
Script para crear un indice con su data view asociado. En este script, se añaden 100 documentos aleatorizados al indice. 

### .env
Archivo que guarda las variables de entorno que el usuario puede adaptar a su gusto (principalmente para la contraseña de elastic y de kibana)

### requirements.txt
Archivo con las dependencias a descargar en el venv

### Dashboards.ndjson
Archivo exportado desde elastic con los dashboards a importar

## Instrucciones de uso
- Clonar el repositorio con los siguientes comandos:
```
  git clone https://github.com/ekaitzg04/reto_visualizacion.git
```
- En una terminal, ir a la carpeta raiz del proyecto (donde esta el archivo docker-compose.yml) y ejecutar lo siguiente:
```
  docker-compose up
```
- Con eso, se levantan todos los contenedores. Una vez levantados, acceder a http://localhost:5601/. Alli, acceder con el usuario "elastic" y la contraseña que hayas configurado (admin1 por defecto)
- En VSCode, crear y activar un venv con los siguientes comandos:
```
python3 -m venv venv
```
```
source venv/bin/activate
```
- Una vez activado, descargar las dependencias con este comando:
```
pip install -r requirements.txt
```
- Una vez todo instalado, ejecutar el archivo "introducir_datos.py" de la siguiente manera:
```
python3 introducir_datos.py
```
- Una vez terminado, entrar en elastic y importar los dashboards desde el archivo "Dashboards.ndjson". Para hacerlo, en http://localhost:5601/, ir a Stack Management -> Saved Objects e importar los dashboards.
- Para verlos, acceder a Analytics -> Dashboard y alli, elegir el que se desee ver.

## Posibles vias de mejora
- Inserción de datos constante: Para una simulación mas realista de este ejercicio, estaría bien tener un programa que añada datos de forma periódica simulando la recepción de datos constante en tiempo real. De esa forma, podríamos comprobar en un entorno mas realista el funcionamiento de nuestra solución
- Importación automacica de dashboards (y indice y dataview) desde el docker compose.
- Descarga automatica del venv con la descarga del requirements.txt en el docker compose

## Problemas o retos encontrados
- Seguridad. Problemas de unhealthiness al levantar contenedores al intentar añadir seguridad simple del tipo usuario/contraseña.
- Importación de dashboards. Al no saber desde donde se hacía, hemos perdido varios dashboards.
- Inserción automática de los dashboards.

## Alternativas posibles
Grafana. Es una plataforma de análisis y monitoreo para todo tipo de bases de datos (incluyendo Elasticsearch). 
Su principal ventaja es que ofrece un amplio rango de plugins y una gran flexibilidad en la creación de dashboards. También es muy efectivo para el monitoreo en tiempo real.

## Fuentes
https://www.youtube.com/watch?v=2gIyPvVZmeE&ab_channel=code215

## Enlace al video
https://www.veed.io/view/162b8ca5-31b6-4e8d-8075-71a048a96de5?panel=share

## Integrantes del grupo
- Eneko Fuente
- Ekaitz Garcia
- Gaizka Miranda
