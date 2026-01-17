
"""
    Escribe un programa en Python que te permita interactuar con el servicio AWS
    Rekognition. La operativa de la aplicación es muy sencilla. 

    Nos debe pedir la ruta de una carpeta en la que tengamos imágenes en 
    formato .jpg o .png. Esa carpeta puede residir en nuestro sistema de 
    archivos o en una carpeta pública del servicio de AWS S3, que nos 
    permite almacenar objetos en la Nube. 
    En el caso de trabajar con el sistema de archivos local, deberemos enviarle 
    los datos binarios de las imágenes al servicio de Rekognition, ya que no 
    podrá acceder directamente a archivos que tengamos en nuestro sistema local.

    Una vez que le pasemos la carpeta, la aplicación recorrerá todas las imágenes
    que contenga y se las pasará al servicio AWS Rekognition para que nos indique
    en cuales de ellas aparecen coches. 

    Para ello, invocaremos al método detect_labels de la instancia del cliente de 
    Rekognition que hayamos abierto.

    Para aquellas imágenes que tengan coches, queremos detectar las matrículas
    que tienen, por lo que será necesario, pasarle nuevamente la imagen al servicio
    de AWS Rekognition, pero en esta ocasión invocando al método detect_text.

    La aplicación deberá indicar con mensajes si en las distintas imágenes de la
    carpeta aparecen o no coches y, en el caso de que lo hagan, las posibles
    matrículas detectadas.


    ▪ Para establecer qué entendemos por vehículo, usaremos las label:
    "car", "vehicle" o "automobile"

    La confianza en la detección debe ser mayor al 90%

    ▪ Para detectar las matrículas, nos quedaremos únicamente con los
    textos identificados del tipo “LINE”, con una confianza mayor al 90% y
    que tengan una longitud entre 5 y 10 y al menos una letra y un número.

"""

import boto3
import os

# Región donde está habilitado Rekognition.
REGION = 'us-east-1'

# Creamos el cliente haciendo uso del fichero de credenciales
rekognition_client = boto3.client('rekognition', region_name=REGION)


# --- DETECTAR MATRICULA --- #
def detectar_matricula(image_bytes_matr):
        # Invocar al método detect_text para analizar el texto de la imagen actual
        responseTexto = rekognition_client.detect_text(
            Image={'Bytes': image_bytes_matr}
        )

        print("Buscando matriculas...")
        # Variable de control para saber si existe alguna válida o no
        matricula = False

        for texto in responseTexto['TextDetections']:
            
            # Filtro 1 -> Solo nos interesan líneas completas ('LINE') y con confianza > 90%
            if texto['Type'] == 'LINE' and texto['Confidence'] > 90.0:
                contenido = texto['DetectedText']
            
                # Validación de formato de matrícula
                if 5 <= len(contenido) <= 10 and any(c.isalpha() for c in contenido) and any(c.isdigit() for c in contenido):
                    matricula = True
                    print(f"\tMatrícula detectada: {contenido} (Confianza: {texto['Confidence']})")
        
        # Si tras recorrer todo no encontramos nada o nada que cumpla los requisitos
        if matricula == False:
            print(f"\tNo se detectó ninguna matrícula o esta no supera el 90% de confianza")


# --- Paso 2. Pedir la ruta al usuario ---
# El usuario escribirá la ruta de la carpeta
ruta_carpeta = input("Por favor, introduce la ruta de la carpeta con las imágenes: ")

# Definimos las etiquetas y extensiones admitidas
etiquetas_vehiculo = ['car', 'vehicle', 'automobile']
extensiones_admitidas = ('.jpg', '.jpeg', '.png')

# Verificamos si la carpeta existe
if os.path.isdir(ruta_carpeta):
    # Listamos todos los archivos de la carpeta
    archivos = os.listdir(ruta_carpeta)

    for nombre_archivo in archivos:
        # Verificar que el archivo es una imagen
        if nombre_archivo.lower().endswith(extensiones_admitidas):
            # Crear ruta completa del archivo [carpeta + fichero]
            ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)

            # Leer la imagen en formato binario ya que usamos archivos locales
            with open(ruta_completa, 'rb') as image_file:
                image_bytes = image_file.read()

            # Realizar la solicitud DetectLabels al servicio de Rekognition.
            response = rekognition_client.detect_labels(
                Image={'Bytes': image_bytes},
                MaxLabels=15,            # Mostrar hasta 15 etiquetas
                MinConfidence=90.0       # Solo etiquetas con confianza >= 90%    
            )

            # --- Paso 4. Procesamos y filtramos ---
            print("-" * 60)
            print(f"Analizando archivo: {nombre_archivo}")
            
            # Variable de control para verificar la existencia de vehículo/s
            is_car = False
            for label in response['Labels']:
                # Filtro: Nombre en objetivos Y confianza estrictamente mayor a 90.0
                if label['Name'].lower() in etiquetas_vehiculo and label['Confidence'] > 90.0:
                    is_car = True
                    print(f"\tEtiqueta: {label['Name']}, Confianza: {label['Confidence']}")
            
            # --- Paso 5. Detectar Matricula ---
            if is_car:
                detectar_matricula(image_bytes)
            else:
                print("\tNo se detectó ningún vehículo")
else:
    print("La ruta introducida no es válida o no es una carpeta.")