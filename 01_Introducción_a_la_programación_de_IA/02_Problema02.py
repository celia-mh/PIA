'''
    Escribe una función que reciba por parámetro una lista de palabras 
    y la ruta a un fichero de texto y devuelva un diccionario que muestre 
    cuantas veces aparecen las distintas palabras de la lista en el fichero 
    de texto. Haz un pequeño programa que la ponga a prueba.
    Requisitos:
        - Eliminar signos de puntuación y convertir todo a minúsculas.
        - Usar un diccionario donde la clave sea la palabra y el valor su frecuencia.
        - Mostrar las palabras y sus frecuencias de forma ordenada por la palabra.
'''
import string

lista = ["Hola", "Vero", "Paciente"]
fichero = "./02_Problema02.txt"

def busqueda_palabras (palabras,ruta):

    try:
        with open(ruta, 'r', encoding='utf-8') as txt:
            # Extraer contenido del fichero
            contenido = txt.read()

            # Minúsculas
            contenido = contenido.lower()
            palabras = [palabra.lower() for palabra in palabras]

            # Eliminar signo de puntuación
            signos = string.punctuation
            for signo in signos:
                contenido = contenido.replace(signo, "")

            # Obtener una lista de palabras a partir de la cadena
            contenido = contenido.split()

            # Inicializar diccionario
            diccionario = {}

            for palabra in palabras:
                diccionario[palabra] = 0
            
            # Recorrer el contenido del fichero
            for palabra_fichero in contenido:
                # Actualizar el contenido del diccionario cuando se encuentre una de sus palabras 
                if palabra_fichero in palabras:
                    diccionario[palabra_fichero] += 1
                    
            return diccionario

    except FileNotFoundError:
        print(f"Error | El fichero no se encontró en la ruta: {ruta}")
    return 

print(busqueda_palabras(lista, fichero))