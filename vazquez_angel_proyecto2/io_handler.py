"""Funciones de lectura y escritura de nodos.csv y grafo.json.
Alumno: Angel Said Vazquez Cisneros
Codigo: 225361652
Proyecto 2  ProgramacionIII Unidad 2
"""

import csv
import json
import os
from typing import Any, Dict, List, Set, Tuple
from grafo import Grafo

ARCHIVO_CSV: str = "nodos.csv"
ARCHIVO_JSON: str = "grafo.json"
ENCABEZADOS: List[str] = ["Origen", "Destino", "Peso"]


def guardar_arista(
    origen: str, destino: str, peso: float, ruta_archivo: str = ARCHIVO_CSV
) -> None:
    """Agrega una conexion al final del CSV.
    Si el archivo no existe o esta vacio, escribe primero los encabezados.
    """
    escribir_encabezados = (
        not os.path.exists(ruta_archivo)
        or os.path.getsize(ruta_archivo) == 0
    )
    with open(ruta_archivo, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        if escribir_encabezados:
            escritor.writerow(ENCABEZADOS)
        escritor.writerow([origen, destino, peso])


def cargar_grafo(ruta_archivo: str = ARCHIVO_CSV) -> Grafo:
    """Lee el CSV fila por fila y construye el grafo en memoria.

    Las filas danadas se omiten con un aviso, sin detener el programa.
    """
    grafo = Grafo()
    try:
        with open(ruta_archivo, "r", newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for numero, fila in enumerate(lector, start=2):
                try:
                    origen = fila["Origen"].strip()
                    destino = fila["Destino"].strip()
                    peso = float(fila["Peso"])
                    if not origen or not destino or peso < 0:
                        raise ValueError("datos vacios o peso negativo")
                except KeyError:
                    print(f"Aviso: fila {numero} omitida (faltan columnas).")
                    continue
                except (ValueError, AttributeError, TypeError):
                    print(f"Aviso: fila {numero} omitida (datos invalidos).")
                    continue
                grafo.agregar_arista(origen, destino, peso)
    except FileNotFoundError:
        print(f"Aviso: no existe '{ruta_archivo}'. Se inicia un grafo vacio.")
    return grafo


def exportar_json(grafo: Grafo, ruta_archivo: str = ARCHIVO_JSON) -> int:
    """Guarda las conexiones del grafo en un archivo JSON
    Cada conexion se escribe una sola vez.
    Regresa cuantas conexiones se exportaron.
    """
    aristas: List[Dict[str, Any]] = []
    vistas: Set[frozenset] = set()
    for nombre, nodo in grafo.nodos.items():
        for vecino, peso in nodo.vecinos.items():
            par = frozenset((nombre, vecino))
            if par in vistas:
                continue
            vistas.add(par)
            aristas.append(
                {"origen": nombre, "destino": vecino, "peso": peso}
            )
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        json.dump({"aristas": aristas}, archivo, indent=4,
                  ensure_ascii=False)
    return len(aristas)


def importar_json(
    ruta_archivo: str = ARCHIVO_JSON,
) -> List[Tuple[str, str, float]]:
    """Lee las conexiones de un JSON y las regresa como tuplas
    Los elementos danados se omiten con un aviso. Si el archivo no existe
    o esta mal formado, regresa una lista vacia
    """
    aristas: List[Tuple[str, str, float]] = []
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        for numero, item in enumerate(datos["aristas"], start=1):
            try:
                origen = str(item["origen"]).strip()
                destino = str(item["destino"]).strip()
                peso = float(item["peso"])
                if not origen or not destino or peso <= 0:
                    raise ValueError("datos vacios o peso no positivo")
            except (KeyError, ValueError, TypeError):
                print(f"Aviso: conexion {numero} del JSON omitida.")
                continue
            aristas.append((origen, destino, peso))
    except FileNotFoundError:
        print(f"Aviso: no existe '{ruta_archivo}'.")
    except json.JSONDecodeError:
        print(f"Aviso: '{ruta_archivo}' no es un JSON valido.")
    except (KeyError, TypeError):
        print(f"Aviso: '{ruta_archivo}' no tiene la estructura esperada.")
    return aristas
