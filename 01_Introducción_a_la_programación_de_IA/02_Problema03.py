'''
    Escribe una función que reciba dos listas de enteros y devuelva 
    un diccionario con la siguiente información 
    (ES OBLIGATORIO USAR CONJUNTOS PARA CALCULARLOS)

        - La intersección de ambos conjuntos (elementos comunes).
        - La unión de ambos conjuntos (todos los elementos sin 
            duplicados).
        - La diferencia simétrica (elementos que están en uno u 
            otro conjunto, pero no en ambos).
'''

def calculos_conjuntos (lista1, lista2):
    # Pasar listas a conjuntos
    lista1 = set(lista1)
    lista2 = set(lista2)

    # Intersección
    interseccion = lista1.intersection(lista2)
    # interseccion = lista1 & lista2

    # Unión
    union = lista1.union(list2)
    # union = lista1 | list2

    # Diferencia Simétrica
    dif_sim = lista1.symmetric_difference(lista2)
    # dif_sim = lista1 ^ lista2

    # Construir el diccionario a devolver
    resultados = {
        "interseccion": list(interseccion),
        "union": list(union),
        "diferencia_simetrica": list(dif_sim)
    }

    return resultados



list1 = [7,4,5,15,16,20]
list2 = [20,15,16,10,5,35]

resultado = calculos_conjuntos(list1, list2)

print("-" * 40)
print("Lista 1:", list1)
print("Lista 2:", list2)
print("-" * 40)

print("Resultados de Operaciones con Conjuntos:")
for clave, valor in resultado.items():
    print(f"- {clave.replace('_', ' ').capitalize()}: {valor}")