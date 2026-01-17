#!/usr/bin/env python
# coding: utf-8

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

IMAGE_FILE_PATH = "C:\\Users\\usuario\\Downloads\\cara1descarga.jpg"
with open(IMAGE_FILE_PATH, 'rb') as image_file:
    image_bytes = image_file.read()


# <h4 style="color:orange;">Paso 3. Realizamos la solicitud a DETECT_LABELS</h4>
# 

# In[4]:


# Realizar la solicitud DetectFaces al servicio de Rekognition. En este caso, cambian ligeramente los parámetros que recibe el método
response = rekognition_client.detect_labels(
    Image={'Bytes': image_bytes},
    MaxLabels=15,            # Mostrar hasta 15 etiquetas
    MinConfidence=95.0       # Solo etiquetas con confianza >= 95%    
)


# <h4 style="color:orange;">Paso 4. Procesamos la respuesta</h4>
# 

# In[5]:


print(response)


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


# Mostrar etiquetas detectadas
for label in response['Labels']:
    print(f"Etiqueta: {label['Name']}, Confianza: {label['Confidence']}, Categorías superiores:{label['Parents']}")


# In[ ]:
