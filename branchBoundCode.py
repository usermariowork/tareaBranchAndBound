import math                     #importamos la librería de math para poder utilizar ciertas funciones
limite_superior = float('inf')  #definimos el maximo tamaño como infinito como variable auxiliar para hacer comparaciones

def crearFinal(camino_actual):                              #funcion auxiliar para guardar la solucion temporal
    camino_final[:numero_nodos + 1] = camino_actual[:]      #añadimos valores al camino final provenientes del camino actual
    camino_final[numero_nodos] = camino_actual[0]           #igualamos a la primera posición del camino actual

def primerMinimo(adj, i):                                   #funcion utilizada para encontrar el costo mínimo en las aristas de un nodo
    min = limite_superior                                   #a esta variable le damos el valor de nuestra auxiliar inicial para que sea infinita
    for k in range(numero_nodos):                           #iteramos el numero de veces necesarias para llegar al numero de nodos del grafo
        if adj[i][k] < min and i != k:                      #si el adyacente actual tiene un costo menor a infinito y es diferente de k
            min = adj[i][k]                                 #se actualiza el valor mínimo
    return min                                              #se retorna el mínimo

def segundoMinimo(adj, i):                                      #funcion que se usa para encontrar la segunda arista menos costosa
    primero, segundo = limite_superior, limite_superior         #inicializamos variables auxiliares para comparar y encontrar la arista en cuestión
    for j in range(numero_nodos):                               #iteramos el numero de veces necesarias para llegar al numero de nodos del grafo
        if i == j:                                              #si se llega al path actual
            continue                                            #continua
        if adj[i][j] <= primero:                                # si el adyacente es menor o igual al primero
            segundo = primero                                   #el segundo se actualiza para que sea igual al primero
            primero = adj[i][j]                                 #el primero se actualiza y ahora es el adyacente encontrado

        elif (adj[i][j] <= segundo and adj[i][j] != primero):   #si el adyacente actual es menor o igual al segundo y es diferente al primero
            segundo = adj[i][j]                                 #el segundo se actualiza al adyacente actual
    return segundo                                              #retornamos e segundo camino menos costoso

def rec(adj, bound_actual, peso_actual, profundidad, camino_actual, visitado):                                      #funcion recursiva
    global costo                                                                                                    #tenemos un costo declarado globalmente

    if profundidad == numero_nodos:                                                                                 #si la profundidad llega al numero de nodos
        if adj[camino_actual[profundidad - 1]][camino_actual[0]] != 0:                                              #si el adyacente del camino actual es diferente de 0
            curr_res = peso_actual + adj[camino_actual[profundidad - 1]] \
                [camino_actual[0]]                                                                                  #calculamos el resultado actual
            if curr_res < costo:                                                                                    #si el resultado actual es menor que el costo
                crearFinal(camino_actual)                                                                           #creamos el final a partir del camino actual
                costo = curr_res                                                                                    #actualizamos el costo para que obtenga el valor del resultado actual
        return                                                                                                      #retornamos

    for i in range(numero_nodos):                                                                                   #iteramos en los nodos

        if (adj[camino_actual[profundidad - 1]][i] != 0 and visitado[i] == False):                                  #si adyacente del camino actual es diferente de 0 y no hay visitados
            temp = bound_actual                                                                                     #la variable temp va a tener el valor del bound actual
            peso_actual += adj[camino_actual[profundidad - 1]][i]                                                   #el peso actual va a actualizarse

            if profundidad == 1:                                                                                    #si la profundidad es 1
                bound_actual -= ((primerMinimo(adj, camino_actual[profundidad - 1]) + primerMinimo(adj, i)) / 2)    #recalculamos el bound actual con eel primer minimo
            else:
                bound_actual -= ((segundoMinimo(adj, camino_actual[profundidad - 1]) + primerMinimo(adj, i)) / 2)   #recalculamos el bound actual con el segundo minimo

            if bound_actual + peso_actual < costo:                                                                  #si la suma de bpund actual y el peso actual es menor al costo
                camino_actual[profundidad] = i                                                                      #el camino actual de la profundidad se iguala a i
                visitado[i] = True                                                                                  #la posición del visitado de i se cambia a true porque ya lo visitamos

                rec(adj, bound_actual, peso_actual, profundidad + 1, camino_actual, visitado)                       #se realiza la funcion recurrente

            peso_actual -= adj[camino_actual[profundidad - 1]][i]                                                   #se alcutaliza el peso actual
            bound_actual = temp                                                                                     #usamos la variable temporal para actualizar al bound actual

            visitado = [False] * len(visitado)                                                                      #el arreglo de visitados se actualiza con falsos dependiendo de los visitados
            for j in range(profundidad):                                                                            #recorremos la profundidad
                if camino_actual[j] != -1:                                                                          #si el camino actual es diferente de -1
                    visitado[camino_actual[j]] = True                                                               #cambiamos a true la posicion del arreglo de visitados a True

def BranchBound(adj):                                                   #el algoritmo recibe la matriz de adyacencia
    bound_actual = 0                                                    #el bound actual se inicializa en 0
    camino_actual = [-1] * (numero_nodos + 1)                           #el camino actual es un array con -1 en cada posición sabiendo que es del tamaño del nimero de nodos +1
    visitados = [False] * numero_nodos                                  #el array de visitados se inicializa como falsos en cada posicion sabiendo que es del tamaño del nimero de nodos

    for i in range(numero_nodos):                                       #se realiza un ciclo para saber el bound actual
        bound_actual += (primerMinimo(adj, i) + segundoMinimo(adj, i))

    bound_actual = math.ceil(bound_actual / 2)                          #se calcula el bound actual según la teoría del algoritmo

    visitados[0] = True                                                 #el primer elemento del array de visitados se cambia a true porque ya se visitó
    camino_actual[0] = 0                                                #hacemos lo mismo con el camino actual

    rec(adj, bound_actual, 0, 1, camino_actual, visitados)              #usamos la funcion recursiva


adj_matrix = [[0, 5, 50, 15], #añadimos la matriz de adyacencia
              [5, 0, 30, 25],
              [50, 30, 0, 10],
              [15, 25, 10, 0]]

#adj_matrix = [[0, 10, 15],
#              [10, 0, 35],
#              [15, 35, 0]]

#adj_matrix = [[0, 10, 20, 20, 40],
#              [10, 0, 25, 35, 25],
#              [20, 25, 0, 30, 45],
#              [20, 35, 30, 0, 15],
#              [40, 25, 45, 15, 0]]


numero_nodos = 4                            #damos el numero de nodos
camino_final = [None] * (numero_nodos + 1)  #el camino final es un array con campos vacios del tamaño del numero de nodos +1
visitados = [False] * numero_nodos          #el arreglo de visitados es un array de falsos del tamaño del numero de nodos
costo = limite_superior                     #al costo lo definimos como el limite superior definido anteriormente
BranchBound(adj_matrix)                     #el algoritmo recibe a la matriz de adyacencia para poder funcionar

print("Minimum cost :", costo)      #imprimirmos el costo
print("Path Taken : ", end=' ')     #imprimimos el camino tomado con ayuda del siguiente ciclo:
for i in range(numero_nodos + 1):
    print(camino_final[i], end=' ') #se imprime cada elemento de camino_final
