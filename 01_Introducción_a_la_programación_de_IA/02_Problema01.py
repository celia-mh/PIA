'''
    Crea una función que reciba una lista de enteros por parámetro y devuelva otra lista, 
    de acuerdo a las siguientes acciones:
        - Eliminar los números negativos de la lista.
        - Eliminar los valores que están repetidos, quedándonos con uno de ellos.
        - Ordenar los números resultantes de menor a mayor.
    Por ejemplo, si le pasara [4, -1, 2, 4, 3, -5, 2], debería retornar [2,3,4].
'''

listaIni = [8, 4, -1, 2, 4, 16, 3, 0, -5, 2, -15, -15, 16]


def formatear_lista (listaRec):
    # 1. Eliminar los números negativos
    listaRec = [numero for numero in listaRec if numero >= 0]

    # 2. Quitar los números repetidos haciendo una doble conversión
    listaRec = list(set(listaRec))
    
    # 3. Ordenar los números resultantes. La funcion sorted() 
    #   que nos garantiza el orden ascendente
    listaRec = sorted(listaRec)

    return listaRec

print(formatear_lista(listaIni))