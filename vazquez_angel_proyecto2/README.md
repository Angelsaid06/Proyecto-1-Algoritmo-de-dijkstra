# Proyecto 2: Persistencia, Archivos y Excepciones

**Alumno:** Angel Said Vazquez Cisneros
**Codigo:** 225361652
**Materia:** Programación III (Unidad 2)

Programa en Python que permite capturar conexiones de una red de transporte
(origen, destino y peso), guardarlas en `nodos.csv`, cargarlas para construir
un grafo y calcular la ruta más corta con el algoritmo de Dijkstra.

## Estructura

| Archivo | Descripción |
|---|---|
| `main.py` | Script principal interactivo (menú y validación de entradas) |
| `grafo.py` | Clases POO: `Nodo`, `Grafo` y Dijkstra |
| `io_handler.py` | Lectura/escritura de CSV y JSON con manejo de errores |
| `nodos.csv` | Datos de las conexiones |
| `requirements.txt` | Dependencias (flake8) |

## Cómo ejecutarlo

```bash
pip install -r requirements.txt
python main.py
```

1. Opción **1**: agrega una conexión (se valida el peso: no texto, no
   negativos, no vacío) y se guarda en `nodos.csv`.
2. Opción **2**: carga el CSV, pide nodo de inicio y destino, y muestra la
   ruta más corta con su peso total.
3. Opción **3**: exporta las conexiones del CSV a `grafo.json`.
4. Opción **4**: importa conexiones desde `grafo.json` y las agrega al CSV
   (omite elementos dañados sin detenerse).

## Validar estilo

```bash
flake8
```

