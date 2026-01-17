#!/usr/bin/env python
# coding: utf-8

"""
Escribe un programa en Python que te permita interactuar con el servicio AWS
Rekognition. La operativa de la aplicación es muy sencilla. 

    1--Nos debe pedir la ruta de una carpeta en la que tengamos imágenes en 
        formato .jpg o .png. Esa carpeta puede residir en nuestro sistema de 
        archivos o en una carpeta pública del servicio de AWS S3, que nos 
        permite almacenar objetos en la Nube. 
        En el caso de trabajar con el sistema de archivos local, deberemos enviarle 
        los datos binarios de las imágenes al servicio de Rekognition, ya que no 
        podrá acceder directamente a archivos que tengamos en nuestro sistema local.

    2--Una vez que le pasemos la carpeta, la aplicación recorrerá todas las imágenes
        que contenga y se las pasará al servicio AWS Rekognition para que nos indique
        en cuales de ellas aparecen coches. 
    
    2.1-Para ello, invocaremos al método detect_labels de la instancia del cliente de 
        Rekognition que hayamos abierto.
    ---Para aquellas imágenes que tengan coches, queremos detectar las matrículas
        que tienen, por lo que será necesario, pasarle nuevamente la imagen al servicio
        de AWS Rekognition, pero en esta ocasión invocando al método detect_text.

    ---La aplicación deberá indicar con mensajes si en las distintas imágenes de la
        carpeta aparecen o no coches y, en el caso de que lo hagan, las posibles
        matrículas detectadas.

Consulta los ejemplos proporcionados para ver cómo interactuar con los
servicios de AWS desde Python. Recuerda que lo primero que tendremos que
hacer es poner en marcha el Learner Lab y con las credenciales temporales que
nos den, abrir instancias clientes de los distintos servicios desde nuestro código
Python. Las credenciales podríamos pasárselas directamente (método menos
recomendable), o mediante un archivo de credenciales.

▪ Para establecer qué entendemos por vehículo, usaremos las label:
"car", "vehicle" o "automobile"

La confianza en la detección debe ser mayor al 90%

▪ Para detectar las matrículas, nos quedaremos únicamente con los
textos identificados del tipo “LINE”, con una confianza mayor al 90% y
que tengan una longitud entre 5 y 10 y al menos una letra y un número.
"""

# Si en lugar de usar el servicio **Detect Faces** de **AWS Rekognition**, quisiéramos usar el de **Detect Labels**, procederíamos de la misma forma, cambiando únicamente el método a llamar y el procesamiento de la respuesta.
# 
# **Detect Labels** permite identificar automáticamente los objetos, escenas y conceptos que aparecen en una imagen. Para ello, analiza una imagen (ya sea un archivo en S3 o en memoria) y devuelve una lista de etiquetas ("labels") que describen lo que el servicio “ve” en ella. Cada etiqueta incluye:
# * El nombre del objeto o escena detectada (por ejemplo: "Car", "Person", "Tree", "Dog", "Building", "Road", etc.).
# * Un nivel de confianza (Confidence), expresado como un porcentaje (0–100), que indica cuán seguro está Rekognition de su detección.
# * En muchos casos, coordenadas de los cuadros delimitadores (BoundingBox) donde se encuentran los objetos en la imagen.
# * Posibles categorías superiores o jerarquías de etiquetas (por ejemplo, “Vehicle → Car → Sedan”).

# In[1]:


import boto3


# <h4 style="color:orange;">Paso 1. Creamos el cliente de Rekognition</h4>

# In[2]:


REGION = 'us-east-1'  # Cambia a la región donde tienes habilitado Rekognition. También se podría especificar en un fichero de configuración análogo al de credenciales

# En este caso creamos el cliente haciendo uso del fichero de credenciales
# Recuerda que debes modificar los valores de acuerdo a los datos de sesión proporcionados al poner en marchar el Learner Lab
rekognition_client = boto3.client('rekognition', region_name=REGION)


# <h4 style="color:orange;">Paso 2. Leemos el fichero con el que queremos trabajar</h4>

# In[3]:


# Leemos la imagen desde el archivo en formato binario

#IMAGE_FILE_PATH = "C:\\Users\\Celia\\Downloads\\Tarea_2\\Imágenes_probadas\\cara1descarga.jpg"
IMAGE_FILE_PATH = "C:\\Users\\Celia\\Downloads\\Tarea_2\\Imágenes_probadas\\coches2.jpeg"
#IMAGE_FILE_PATH = "C:\\Users\\Celia\\Downloads\\Tarea_2\\Imágenes_probadas\\CochesVariados.jpeg"
with open(IMAGE_FILE_PATH, 'rb') as image_file:
    image_bytes = image_file.read()


# <h4 style="color:orange;">Paso 3. Realizamos la solicitud a DETECT_LABELS</h4>
# 

# In[4]:


# Realizar la solicitud DetectLabels al servicio de Rekognition. En este caso, cambian ligeramente los parámetros que recibe el método
response = rekognition_client.detect_labels(
    Image={'Bytes': image_bytes},
    MaxLabels=15,            # Mostrar hasta 15 etiquetas
    MinConfidence=90.0       # Solo etiquetas con confianza >= 90%    
)


# <h4 style="color:orange;">Paso 4. Procesamos la respuesta</h4>
# 

# In[5]:


#print(response)


# **Estructura de la respuesta**
# 
# La respuesta de **detect_labels** es un **diccionario** que contiene información sobre las **etiquetas detectadas**. Donde: 
# * **Labels**: Contiene las etiquetas detectadas con:
#     1. **Name**: El nombre de la etiqueta (por ejemplo, "Person", "Tree"). OJO, se especifican en inglés.
#     2. **Confidence**: La confianza de que la etiqueta sea correcta, en porcentaje.
#     3. **Instances**: Si aplica, contiene instancias de los objetos detectados con su BoundingBox (rectángulo de localización).
#     4. **Parents**: Las categorías generales a las que pertenece la etiqueta (por ejemplo, "Person" puede tener "Human" como padre).
# 
# 

# In[6]:


# Mostrar etiquetas detectadas filtrando por los objetos objetivos
objObjetivos = ['car', 'vehicle', 'automobile']

for label in response['Labels']:
    if label['Name'].lower() in objObjetivos and label['Confidence'] > 90.0:
            print(f"Etiqueta: {label['Name']}, Confianza: {label['Confidence']}, Categorías superiores:{label['Parents']}")
            
            # --- DETECTAR MATRICULA --- #
            responseTexto = rekognition_client.detect_text(
                Image={'Bytes': image_bytes}
            )

            print("Buscando matriculas...")
            #print(responseTexto)
            for texto in responseTexto['TextDetections']:
                if texto['Type'] == 'LINE' and texto['Confidence'] > 90.0:
                    contenido = texto['DetectedText']
                    #print(contenido)
                    if 5 <= len(contenido) <= 10 and any(c.isalpha() for c in contenido) and any(c.isdigit() for c in contenido):
                        print(f" Matrícula detectada: {contenido} (Confianza: {texto['Confidence']})")

# In[ ]:
