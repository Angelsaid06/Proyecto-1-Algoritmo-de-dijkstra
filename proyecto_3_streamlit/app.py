# Titulo: Proyecto 3  Interfaz web con Streamlit
# Alumno: Angel Said Vazquez Cisneros
# Maestro: Diego Alberto Ayala Vazquez
# Fecha: 15/11/2026
# Descripcion: Pagina web para registrar conexiones y calcular rutas.

import pandas as pd
import streamlit as st
from grafo import Grafo
from io_handler import cargar_grafo, guardar_arista

st.set_page_config(page_title="Rutas con Dijkstra")

# Un poco de estilo para que se vea mas chilo
st.markdown("""
<style>
div[data-testid="stHeading"] h1 { color: #8A6BBE; }
div[data-testid="stHeading"] h2,
div[data-testid="stHeading"] h3 { color: #6F8FC9; }
div[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 2px solid #F6D6E6;
    border-radius: 12px;
    padding: 8px 14px;
}
div[data-testid="stForm"] {
    background-color: #FFF1E6;
    border: 2px solid #FFD9BF;
    border-radius: 12px;
}
.stButton button, div[data-testid="stFormSubmitButton"] button {
    background-color: #F6D6E6;
    border: none;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("Red de transporte con Dijkstra")
st.write("Registra conexiones entre lugares y calcula la ruta mas corta.")

# cargar el grafo una sola vez
# Solo se lee nodos.csv si el grafo todavia no esta en session_state,
# asi no se vuelve a leer el archivo cada vez que se presiona un boton
if "grafo" not in st.session_state:
    try:
        grafo_leido, avisos = cargar_grafo()
        st.session_state["grafo"] = grafo_leido
        st.session_state["avisos"] = avisos
    except FileNotFoundError:
        st.session_state["grafo"] = Grafo()
        st.session_state["avisos"] = [
            "No se encontro nodos.csv, se empieza con una red vacia."]
    except PermissionError:
        st.session_state["grafo"] = Grafo()
        st.session_state["avisos"] = [
            "No hay permiso para leer nodos.csv, se empieza vacia."]

grafo = st.session_state["grafo"]

# pestanas
tab_ruta, tab_registro, tab_red = st.tabs(
    ["Calcular ruta", "Registrar conexion", "Ver red"])

# Pestana 1= calcular la ruta mas corta
with tab_ruta:
    st.subheader("Ruta mas corta")
    if len(grafo.nodos) > 0:
        st.caption("Nodos disponibles: " + ", ".join(grafo.nodos.keys()))

    col1, col2 = st.columns(2)
    with col1:
        origen = st.text_input("Nodo de origen")
    with col2:
        destino = st.text_input("Nodo de destino")

    if st.button("Calcular ruta"):
        origen = origen.strip()
        destino = destino.strip()

        if origen == "" or destino == "":
            st.warning("Escribe el nodo de origen y el de destino.")
        else:
            try:
                distancia, ruta = grafo.dijkstra(origen, destino)
                if distancia is None:
                    st.error("No existe una ruta entre " + origen +
                             " y " + destino + ".")
                else:
                    st.success("Ruta encontrada")
                    st.metric("Costo total", distancia)
                    st.info(" -> ".join(ruta))
                    st.write("Paradas en el recorrido:", len(ruta))
            except KeyError as error:
                st.error("El nodo '" + str(error.args[0]) +
                         "' no existe en la red. Revisa como lo escribiste.")

# Pestana 2= registrar una conexion nueva
with tab_registro:
    st.subheader("Nueva conexion")

    with st.form("form_conexion", clear_on_submit=True):
        nuevo_origen = st.text_input("Origen")
        nuevo_destino = st.text_input("Destino")
        texto_peso = st.text_input("Peso (ej. 4 o 2.5)")
        guardar = st.form_submit_button("Guardar conexion")

    if guardar:
        nuevo_origen = nuevo_origen.strip()
        nuevo_destino = nuevo_destino.strip()

        if nuevo_origen == "" or nuevo_destino == "":
            st.warning("El origen y el destino no pueden quedar vacios.")
        elif nuevo_origen == nuevo_destino:
            st.warning("El origen y el destino deben ser diferentes.")
        else:
            try:
                peso = float(texto_peso)
                if peso <= 0:
                    raise ValueError("el peso debe ser mayor que 0")

                # primero se guarda en el disco y luego en la memoria
                guardar_arista(nuevo_origen, nuevo_destino, peso)
                grafo.agregar_arista(nuevo_origen, nuevo_destino, peso)
                st.success("Conexion guardada: " + nuevo_origen + " <-> " +
                           nuevo_destino + " (" + str(peso) + ")")
            except ValueError:
                st.error("El peso debe ser un numero mayor que 0 "
                         "(ej. 4 o 2.5).")
            except PermissionError:
                st.error("No se pudo guardar: nodos.csv esta abierto en "
                         "otro programa o no hay permiso.")

# Pestana 3= ver la red en tabla
with tab_red:
    st.subheader("Conexiones registradas")
    conexiones = grafo.lista_conexiones()

    if len(conexiones) == 0:
        st.info("La red esta vacia. Registra una conexion primero.")
    else:
        tabla = pd.DataFrame(conexiones,
                             columns=["Origen", "Destino", "Peso"])
        st.dataframe(tabla, hide_index=True)

        # tabla de nodos dentro de un expander
        with st.expander("Ver nodos y sus vecinos"):
            filas = []
            for nombre in grafo.nodos:
                vecinos = grafo.nodos[nombre].vecinos
                filas.append([nombre, len(vecinos),
                              ", ".join(vecinos.keys())])
            tabla_nodos = pd.DataFrame(
                filas, columns=["Nodo", "Num. de vecinos", "Vecinos"])
            st.dataframe(tabla_nodos, hide_index=True)

# barra lateral
# Va al final para que los numeros ya incluyan lo recien guardado
with st.sidebar:
    st.header("Resumen de la red")
    st.metric("Nodos", len(grafo.nodos))
    st.metric("Conexiones", len(grafo.lista_conexiones()))
    st.caption("Datos guardados en nodos.csv")

    # avisos de filas danadas del CSV
    for aviso in st.session_state["avisos"]:
        st.warning(aviso)
