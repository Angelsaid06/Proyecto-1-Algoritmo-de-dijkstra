# Titulo: Proyecto 3 - Lectura y escritura de archivos
# Autor: Angel Said Vazquez Cisneros
# Fecha: 15/11/2026
# Descripcion: Guarda y lee las conexiones en nodos.csv y en grafo.json.

import csv
import json
import os

from grafo import Grafo

# Los archivos se buscan en la misma carpeta que este script,
# asi funciona aunque el programa se corra desde otra carpeta
CARPETA = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_CSV = os.path.join(CARPETA, "nodos.csv")
ARCHIVO_JSON = os.path.join(CARPETA, "grafo.json")
ENCABEZADOS = ["Origen", "Destino", "Peso"]


def guardar_arista(origen, destino, peso, ruta_archivo=ARCHIVO_CSV):
    # Agrega una conexion al final del CSV.
    # Si el archivo no existe o esta vacio primero pone los encabezados.
    # Si no se puede escribir, el error (ej. PermissionError) lo maneja
    # quien llama a esta funcion.
    poner_encabezados = False
    if not os.path.exists(ruta_archivo):
        poner_encabezados = True
    elif os.path.getsize(ruta_archivo) == 0:
        poner_encabezados = True

    with open(ruta_archivo, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        if poner_encabezados:
            escritor.writerow(ENCABEZADOS)
        escritor.writerow([origen, destino, peso])


def cargar_grafo(ruta_archivo=ARCHIVO_CSV):
    # Lee el CSV fila por fila y arma el grafo.
    # Regresa el grafo y una lista con los avisos de las filas danadas.
    # Si el archivo no existe se lanza FileNotFoundError.
    grafo = Grafo()
    avisos = []

    with open(ruta_archivo, "r", newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        numero = 1  # la fila 1 son los encabezados
        for fila in lector:
            numero = numero + 1
            try:
                origen = fila["Origen"].strip()
                destino = fila["Destino"].strip()
                peso = float(fila["Peso"])
                if origen == "" or destino == "" or peso <= 0:
                    raise ValueError("datos vacios o peso no positivo")
            except KeyError:
                avisos.append("Fila " + str(numero) + " omitida: "
                              "faltan columnas.")
                continue
            except (ValueError, TypeError, AttributeError):
                avisos.append("Fila " + str(numero) + " omitida: "
                              "datos invalidos.")
                continue
            grafo.agregar_arista(origen, destino, peso)

    return grafo, avisos


def exportar_json(grafo, ruta_archivo=ARCHIVO_JSON):
    # Guarda las conexiones del grafo en un JSON (cada una una sola vez)
    aristas = []
    for conexion in grafo.lista_conexiones():
        aristas.append({
            "origen": conexion[0],
            "destino": conexion[1],
            "peso": conexion[2],
        })
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        json.dump({"aristas": aristas}, archivo, indent=4,
                  ensure_ascii=False)
    return len(aristas)


def importar_json(ruta_archivo=ARCHIVO_JSON):
    # Lee las conexiones de un JSON y las regresa en una lista.
    # Los elementos danados se saltan con un aviso.
    aristas = []
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        numero = 0
        for item in datos["aristas"]:
            numero = numero + 1
            try:
                origen = str(item["origen"]).strip()
                destino = str(item["destino"]).strip()
                peso = float(item["peso"])
                if origen == "" or destino == "" or peso <= 0:
                    raise ValueError("datos vacios o peso no positivo")
            except (KeyError, ValueError, TypeError):
                print("Aviso: conexion", numero, "del JSON omitida.")
                continue
            aristas.append([origen, destino, peso])
    except FileNotFoundError:
        print("Aviso: no existe el archivo grafo.json")
    except json.JSONDecodeError:
        print("Aviso: grafo.json no es un JSON valido")
    except (KeyError, TypeError):
        print("Aviso: grafo.json no tiene la estructura esperada")
    return aristas
