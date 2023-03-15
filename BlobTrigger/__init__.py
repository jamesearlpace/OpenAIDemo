#Ejecutar en Azure Functions cuando se sube un archivo .txt a un contenedor de Blob Storage

import os
import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.core.exceptions import ResourceNotFoundError, HttpResponseError
import openai
import datetime

def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")


# Analizar la cadena de conexión y el nombre del contenedor desde las variables de entorno
connection_string = os.environ.get("STORAGE_CONNECTION_STRING")

# Crear BlobServiceClient utilizando la cadena de conexión
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Modificar el nombre del archivo agregando '_editado' al final
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") # generar marca de tiempo

file_name = myblob.name.replace(".txt", f"_{timestamp}.json")

# Crear BlobClient para el nuevo blob con el nombre modificado en el mismo contenedor
new_blob_client = blob_service_client.get_blob_client(container="destination", blob=file_name)

# Copiar el contenido del blob original a una nueva variable
file_content = myblob.read().decode('utf-8')


# Establecer el contenido del nuevo archivo en la salida de la llamada de la API de OpenAI
prompt = file_content
beginning_text = "Esta es una conversación del centro de llamadas ###"
ending_text = """### Resumir esto en json por
            satisfacción del cliente en una escala de 1 a 10 con 1 siendo el menos satisfecho,
            sentimiento del cliente,
            duración del chat en segundos,
            problema resuelto verdadero/falso,
            categoría de problema,
            subcategoría de problema,
            nombre del agente,
            nombre del cliente."""
prompt = beginning_text + prompt + ending_text



openai.api_type = "azure"
openai.api_base = "https://openai-sandbox-jep.openai.azure.com/"
openai.api_version = "2022-12-01"
openai.api_key = os.environ.get("OPENAI_API_KEY")

response = openai.Completion.create(
engine="davinci3",
prompt=prompt,
temperature=0.7,
max_tokens=256,
top_p=1,
frequency_penalty=0,
presence_penalty=0
)

file_content = response.choices[0].text

# Guardar el contenido modificado en el nuevo blob
new_blob_client.upload_blob(file_content, overwrite=True)

logging.info(f"Blob {myblob.name} duplicado en el mismo contenedor con completaciones de texto y renombrado a {file_name}.")
