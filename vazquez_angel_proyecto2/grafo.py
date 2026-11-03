"""Clases POO del proyecto: Nodo, Grafo y el algoritmo de Dijkstra.

Alumno: Angel Said Vazquez Cisneros
Codigo: 225361652
Proyecto 2  ProgramacionIII Unidad 2
"""
from typing import Dict, List, Optional, Tuple


class Nodo:
    """Representa un lugar del mapa y sus conexiones con su costo"""

    def __init__(self, nombre: str) -> None:
        """Crea un nodo con nombre y sin vecinos."""
        self.nombre: str = nombre
        self.vecinos: Dict[str, float] = {}

    def agregar_vecino(self, otro_nodo: str, peso: float) -> None:
        """Conecta este nodo con otro guardando el costo del camino"""
        self.vecinos[otro_nodo] = peso


class Grafo:
    """Conjunto de nodos conectados calcula rutas con Dijkstra"""

    def __init__(self) -> None:
        """Crea un grafo vacio."""
        self.nodos: Dict[str, Nodo] = {}

    def agregar_nodo(self, nombre: str) -> None:
        """Agrega un nodo al grafo si todavia no existe"""
        if nombre not in self.nodos:
            self.nodos[nombre] = Nodo(nombre)

    def agregar_arista(self, origen: str, destino: str, peso: float) -> None:
        """Conecta dos nodos en ambos sentidos, creandolos si hace falta"""
        self.agregar_nodo(origen)
        self.agregar_nodo(destino)
        self.nodos[origen].agregar_vecino(destino, peso)
        self.nodos[destino].agregar_vecino(origen, peso)

    def dijkstra(
        self, origen: str, destino: str
    ) -> Tuple[Optional[float], Optional[List[str]]]:
        """Calcula la ruta mas corta entre origen y destino.
        Regresa. Si alguno de los nodos no existe
        o no hay camino entre ellos, regresa.
        """
        if origen not in self.nodos or destino not in self.nodos:
            return None, None

        distancias: Dict[str, float] = {
            nombre: float("inf") for nombre in self.nodos
        }
        anteriores: Dict[str, Optional[str]] = {
            nombre: None for nombre in self.nodos
        }
        distancias[origen] = 0.0
        no_visitados: List[str] = list(self.nodos.keys())

        while no_visitados:
            actual = min(no_visitados, key=lambda n: distancias[n])

            # Si lo mas cercano es infinito, ya no hay mas caminos.
            if distancias[actual] == float("inf"):
                break
            if actual == destino:
                break

            for vecino, peso in self.nodos[actual].vecinos.items():
                nueva_distancia = distancias[actual] + peso
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    anteriores[vecino] = actual

            no_visitados.remove(actual)

        if distancias[destino] == float("inf"):
            return None, None

        return distancias[destino], self._reconstruir_ruta(
            anteriores, destino
        )

    @staticmethod
    def _reconstruir_ruta(
        anteriores: Dict[str, Optional[str]], destino: str
    ) -> List[str]:
        """Reconstruye la ruta hacia atras desde el destino"""
        ruta: List[str] = []
        nodo: Optional[str] = destino
        while nodo is not None:
            ruta.append(nodo)
            nodo = anteriores[nodo]
        ruta.reverse()
        return ruta
