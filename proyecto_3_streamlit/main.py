# Titulo: Proyecto 3 - Menu en consola (version del Proyecto 2)
# Autor: Angel Said Vazquez Cisneros
# Fecha: 15/11/2026
# Descripcion: Menu en consola para agregar conexiones y calcular rutas.

from grafo import Grafo
from io_handler import (cargar_grafo, exportar_json, guardar_arista,
                        importar_json)


def leer_grafo():
    # Lee el CSV y avisa si hay filas malas o si no existe
    try:
        grafo, avisos = cargar_grafo()
    except FileNotFoundError:
        print("Aviso: no existe nodos.csv, se empieza con un grafo vacio.")
        return Grafo()
    for aviso in avisos:
        print("Aviso:", aviso)
    return grafo


def pedir_texto(mensaje):
    # Pide un texto que no este vacio
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto
        print("Error: este campo no puede quedar vacio.")


def pedir_peso(mensaje):
    # Pide un numero mayor que 0
    while True:
        try:
            peso = float(input(mensaje))
            if peso <= 0:
                raise ValueError("el peso debe ser positivo")
            return peso
        except ValueError:
            print("Error: escribe un numero mayor que 0 (ej. 4 o 2.5).")


def agregar_conexion():
    origen = pedir_texto("Nodo origen: ")
    destino = pedir_texto("Nodo destino: ")
    peso = pedir_peso("Peso de la arista: ")
    try:
        guardar_arista(origen, destino, peso)
    except PermissionError:
        print("Error: no hay permiso para escribir nodos.csv "
              "(revisa que no este abierto en Excel).")
        return
    print("Conexion guardada:", origen, "<->", destino, "(" + str(peso) + ")")


def calcular_ruta(grafo):
    if len(grafo.nodos) == 0:
        print("El grafo esta vacio. Agrega conexiones primero.")
        return
    print("Nodos disponibles:", ", ".join(grafo.nodos.keys()))
    origen = pedir_texto("Nodo de inicio: ")
    destino = pedir_texto("Nodo de destino: ")
    try:
        distancia, ruta = grafo.dijkstra(origen, destino)
    except KeyError as error:
        print("Error: el nodo", error.args[0], "no existe.")
        return
    if distancia is None:
        print("No hay ruta entre", origen, "y", destino)
        return
    print("Peso total:", distancia)
    print("Ruta mas corta:", " -> ".join(ruta))


def exportar_a_json():
    grafo = leer_grafo()
    try:
        total = exportar_json(grafo)
    except PermissionError:
        print("Error: no hay permiso para escribir grafo.json")
        return
    print("Se exportaron", total, "conexiones a grafo.json")


def importar_desde_json():
    aristas = importar_json()
    if len(aristas) == 0:
        print("No se importo ninguna conexion.")
        return
    try:
        for arista in aristas:
            guardar_arista(arista[0], arista[1], arista[2])
    except PermissionError:
        print("Error: no hay permiso para escribir nodos.csv")
        return
    print("Se importaron", len(aristas), "conexiones al CSV.")


def mostrar_menu():
    print("\n Red de transporte Dijkstra")
    print("1. Agregar conexion")
    print("2. Calcular ruta mas corta")
    print("3. Exportar conexiones a JSON")
    print("4. Importar conexiones desde JSON")
    print("5. Salir")


def main():
    while True:
        mostrar_menu()
        opcion = input("Elige una opcion: ").strip()
        if opcion == "1":
            agregar_conexion()
        elif opcion == "2":
            # se vuelve a leer el CSV para incluir lo recien guardado
            calcular_ruta(leer_grafo())
        elif opcion == "3":
            exportar_a_json()
        elif opcion == "4":
            importar_desde_json()
        elif opcion == "5":
            print("Hasta luego.")
            break
        else:
            print("Opcion invalida, elige del 1 al 5.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma terminado por el usuario.")
