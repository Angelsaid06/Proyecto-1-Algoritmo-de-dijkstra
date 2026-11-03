"""Script principal del Proyecto 2
Alumno: Angel Said Vazquez Cisneros
Codigo: 225361652
Proyecto 2  ProgramacionIII Unidad 2
"""
from grafo import Grafo
from io_handler import (
    ARCHIVO_JSON,
    cargar_grafo,
    exportar_json,
    guardar_arista,
    importar_json,
)


def pedir_texto(mensaje: str) -> str:
    """Pide un texto no vacio al usuario hasta que sea valido"""
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("Error: este campo no puede quedar vacio.")


def pedir_peso(mensaje: str) -> float:
    """Pide un peso numerico mayor que cero hasta que sea valido"""
    while True:
        try:
            peso = float(input(mensaje))
            if peso <= 0:
                raise ValueError("el peso debe ser positivo")
            return peso
        except ValueError:
            print("Error: escribe un numero mayor que 0 (ej. 4 o 2.5).")


def agregar_conexion() -> None:
    """Pide una conexion al usuario y la guarda en el CSV"""
    origen = pedir_texto("Nodo origen: ")
    destino = pedir_texto("Nodo destino: ")
    peso = pedir_peso("Peso de la arista: ")
    try:
        guardar_arista(origen, destino, peso)
    except OSError as error:
        print(f"Error al guardar en el archivo: {error}")
        return
    print(f"Conexion guardada: {origen} <-> {destino} ({peso})")


def calcular_ruta(grafo: Grafo) -> None:
    """Pide origen y destino y muestra la ruta mas corta."""
    if not grafo.nodos:
        print("El grafo esta vacio. Agrega conexiones primero.")
        return
    print("Nodos disponibles:", ", ".join(grafo.nodos.keys()))
    origen = pedir_texto("Nodo de inicio: ")
    destino = pedir_texto("Nodo de destino: ")
    distancia, ruta = grafo.dijkstra(origen, destino)
    if distancia is None or ruta is None:
        print(f"No hay ruta entre {origen} y {destino} (o no existen).")
        return
    print(f"Peso total: {distancia}")
    print("Ruta mas corta: " + " -> ".join(ruta))


def exportar_a_json() -> None:
    """Exporta las conexiones del CSV a un archivo JSON"""
    grafo = cargar_grafo()
    try:
        total = exportar_json(grafo)
    except OSError as error:
        print(f"Error al escribir el JSON: {error}")
        return
    print(f"Se exportaron {total} conexiones a {ARCHIVO_JSON}")


def importar_desde_json() -> None:
    """Lee conexiones de un JSON y las agrega al CSV."""
    aristas = importar_json()
    if not aristas:
        print("No se importo ninguna conexion.")
        return
    try:
        for origen, destino, peso in aristas:
            guardar_arista(origen, destino, peso)
    except OSError as error:
        print(f"Error al guardar en el archivo: {error}")
        return
    print(f"Se importaron {len(aristas)} conexiones al CSV.")


def mostrar_menu() -> None:
    """Imprime las opciones del menu."""
    print("\n Red de transporte Dijkstra")
    print("1. Agregar conexion")
    print("2. Calcular ruta mas corta")
    print("3. Exportar conexiones a JSON")
    print("4. Importar conexiones desde JSON")
    print("5. Salir")


def main() -> None:
    """Ciclo principal del programa"""
    while True:
        mostrar_menu()
        opcion = input("Elige una opcion: ").strip()
        if opcion == "1":
            agregar_conexion()
        elif opcion == "2":
            # Se recarga el CSV para incluir las conexiones recien guardadas
            calcular_ruta(cargar_grafo())
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
