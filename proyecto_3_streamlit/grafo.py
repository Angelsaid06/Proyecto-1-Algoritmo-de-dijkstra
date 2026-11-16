# Titulo: Proyecto 3 - Clases del grafo y algoritmo de Dijkstra
# Autor: Angel Said Vazquez Cisneros
# Fecha: 15/11/2026
# Descripcion: Clases Nodo y Grafo con Dijkstra para la ruta mas corta.


class Nodo:
    # Cada nodo es un lugar del mapa (una estacion, una casa, etc.)
    def __init__(self, nombre):
        self.nombre = nombre
        self.vecinos = {}  # nombre del vecino -> peso del camino

    def agregar_vecino(self, otro_nodo, peso):
        self.vecinos[otro_nodo] = peso


class Grafo:
    # El grafo guarda todos los nodos en un diccionario
    def __init__(self):
        self.nodos = {}  # nombre -> objeto Nodo

    def agregar_nodo(self, nombre):
        if nombre not in self.nodos:
            self.nodos[nombre] = Nodo(nombre)

    def agregar_arista(self, nombre1, nombre2, peso):
        # Si los nodos no existen se crean
        self.agregar_nodo(nombre1)
        self.agregar_nodo(nombre2)

        # Se conecta en los dos sentidos (el camino va y viene)
        self.nodos[nombre1].agregar_vecino(nombre2, peso)
        self.nodos[nombre2].agregar_vecino(nombre1, peso)

    def lista_conexiones(self):
        # Regresa cada conexion una sola vez: [origen, destino, peso]
        conexiones = []
        ya_vistas = []
        for nombre in self.nodos:
            for vecino in self.nodos[nombre].vecinos:
                # si ya puse B -> A no vuelvo a poner A -> B
                if (vecino, nombre) in ya_vistas:
                    continue
                ya_vistas.append((nombre, vecino))
                peso = self.nodos[nombre].vecinos[vecino]
                conexiones.append([nombre, vecino, peso])
        return conexiones

    def dijkstra(self, origen, destino):
        # Si algun nodo no existe se lanza KeyError con su nombre
        if origen not in self.nodos:
            raise KeyError(origen)
        if destino not in self.nodos:
            raise KeyError(destino)

        # Al inicio todas las distancias son infinito, menos el origen
        distancias = {}
        anteriores = {}  # para saber por donde llegue a cada nodo
        for nombre in self.nodos:
            distancias[nombre] = float("inf")
            anteriores[nombre] = None
        distancias[origen] = 0

        no_visitados = list(self.nodos.keys())

        while len(no_visitados) > 0:
            # 1. Buscar el nodo no visitado con la menor distancia
            actual = None
            for nombre in no_visitados:
                if actual is None or distancias[nombre] < distancias[actual]:
                    actual = nombre

            # Si lo mas chico es infinito ya no hay mas caminos
            if distancias[actual] == float("inf"):
                break

            if actual == destino:
                break

            # 2. Actualizar la distancia de los vecinos
            for vecino in self.nodos[actual].vecinos:
                peso = self.nodos[actual].vecinos[vecino]
                nueva_distancia = distancias[actual] + peso
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    anteriores[vecino] = actual

            no_visitados.remove(actual)

        # Si el destino sigue en infinito no hay ruta
        if distancias[destino] == float("inf"):
            return None, None

        # 3. Reconstruir el camino hacia atras desde el destino
        ruta = []
        nodo = destino
        while nodo is not None:
            ruta.append(nodo)
            nodo = anteriores[nodo]
        ruta.reverse()

        return distancias[destino], ruta
