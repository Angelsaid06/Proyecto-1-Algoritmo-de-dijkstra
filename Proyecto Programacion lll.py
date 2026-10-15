"""
nombre completo: Angel Said Vazquez Cisneros
Titulo: Proyecto del algoritmo de Dijkstra con programacion orientada a objetos
Fecha: 15/10/2026

Descripcion: El programa usa el algoritmo de Dijkstra para encontrar la ruta más corta entre dos lugares de un mapa.
Con POO, la clase Nodo guarda cada lugar y sus conexiones con su costo, y la clase Grafo junta todos los nodos y calcula la ruta. 
El algoritmo va eligiendo siempre el nodo con menor distancia acumulada y actualiza a sus vecinos, y al final reconstruye el camino hacia atrás desde el destino. 
El programa le pide al usuario el origen y el destino, y muestra la distancia total y la secuencia exacta de nodos del recorrido.

"""


class Nodo:
    # Cada nodo es un lugar del mapa (una estacion, una ciudad, etc.)
    def __init__(self, nombre):
        self.nombre = nombre
        self.vecinos = {}  # aqui guardo a que nodos esta conectado y cuanto cuesta ir

    def agregar_vecino(self, otro_nodo, peso):
        self.vecinos[otro_nodo] = peso


class Grafo:
    # El grafo guarda todos los nodos
    def __init__(self):
        self.nodos = {}  # diccionario: nombre -> objeto Nodo

    def agregar_nodo(self, nombre):
        if nombre not in self.nodos:
            self.nodos[nombre] = Nodo(nombre)

    def agregar_arista(self, nombre1, nombre2, peso):
        # Si el nodo no existe lo creo
        self.agregar_nodo(nombre1)
        self.agregar_nodo(nombre2)

        # Conecto en los dos sentidos (el camino va y viene)
        self.nodos[nombre1].agregar_vecino(nombre2, peso)
        self.nodos[nombre2].agregar_vecino(nombre1, peso)

    def dijkstra(self, origen, destino):
        # Revisar que los nodos existan
        if origen not in self.nodos or destino not in self.nodos:
            print("Error: el origen o el destino no existe en el grafo")
            return None, None

        # Al inicio todas las distancias son infinito, menos el origen que es 0
        distancias = {}
        anteriores = {}  # para saber por donde llegue a cada nodo
        for nombre in self.nodos:
            distancias[nombre] = float("inf")
            anteriores[nombre] = None
        distancias[origen] = 0

        # Lista de nodos que todavia no reviso
        no_visitados = list(self.nodos.keys())

        while len(no_visitados) > 0:
            # 1. Buscar el nodo no visitado con la menor distancia
            actual = None
            for nombre in no_visitados:
                if actual is None or distancias[nombre] < distancias[actual]:
                    actual = nombre

            # Si lo mas chico es infinito, ya no hay mas caminos posibles
            if distancias[actual] == float("inf"):
                break

           
            if actual == destino:
                break

            
            for vecino in self.nodos[actual].vecinos:
                peso = self.nodos[actual].vecinos[vecino]
                nueva_distancia = distancias[actual] + peso

               
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    anteriores[vecino] = actual

        
            no_visitados.remove(actual)

    
        if distancias[destino] == float("inf"):
            return None, None

        
        ruta = []
        nodo = destino
        while nodo is not None:
            ruta.append(nodo)
            nodo = anteriores[nodo]
        ruta.reverse()  

        return distancias[destino], ruta

mapa = Grafo()
mapa.agregar_arista("Casa", "Escuela", 7)
mapa.agregar_arista("Casa", "Parque", 9)
mapa.agregar_arista("Casa", "Mercado", 14)
mapa.agregar_arista("Escuela", "Parque", 10)
mapa.agregar_arista("Escuela", "Biblioteca", 15)
mapa.agregar_arista("Parque", "Biblioteca", 11)
mapa.agregar_arista("Parque", "Mercado", 2)
mapa.agregar_arista("Biblioteca", "Cine", 6)
mapa.agregar_arista("Mercado", "Cine", 9)

print("algoritmo de dijkstra")
print("Nodos disponibles:", ", ".join(mapa.nodos.keys()))
print()

origen = input("Escribe el nodo de origen: ")
destino = input("Escribe el nodo de destino: ")

distancia, ruta = mapa.dijkstra(origen, destino)

print()
if distancia is None:
    print("No hay una ruta entre", origen, "y", destino)
else:
    print("Distancia/costo total:", distancia)
    print("Ruta mas corta:", " -> ".join(ruta))