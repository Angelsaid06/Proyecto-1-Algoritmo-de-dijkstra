# Proyecto 3: Interfaz web con Streamlit

**Alumno:** Angel Said Vazquez Cisneros
**Codigo:** 225361652
**Materia:** Programación III (Unidad 3)

Página web hecha con Streamlit para la red de transporte de los proyectos
anteriores. Permite registrar conexiones (origen, destino y peso), verlas en
una tabla y calcular la ruta más corta con el algoritmo de Dijkstra.

## Archivos

| Archivo | Para qué sirve |
|---|---|
| `app.py` | Interfaz web con Streamlit |
| `main.py` | Menú en consola del Proyecto 2 |
| `grafo.py` | Clases `Nodo` y `Grafo` con Dijkstra |
| `io_handler.py` | Lectura y escritura de `nodos.csv` y `grafo.json` |
| `nodos.csv` | Conexiones de prueba |
| `requirements.txt` | Librerías que se necesitan |

## Cómo correrlo

```bash
pip install -r requirements.txt
streamlit run app.py
```

La página tiene tres pestañas:

1. **Calcular ruta:** se escribe el nodo de origen y el de destino y muestra
   el costo total y el recorrido.
2. **Registrar conexion:** guarda una conexión nueva en `nodos.csv` y en el
   grafo que está en memoria.
3. **Ver red:** muestra las conexiones en una tabla y, en un desplegable, los
   nodos con sus vecinos.

El archivo `nodos.csv` se lee una sola vez y el grafo se guarda en
`st.session_state`. Los errores (peso que no es número, nodo que no existe,
archivo que no se encuentra o sin permiso) se muestran con `st.error` o
`st.warning`.

Para probar que no hay ruta se puede usar `Casa` y `Zoologico`, porque
`Zoologico` y `Linea 2` no están conectados con el resto de la red.

## Validar estilo

```bash
flake8 .
```
