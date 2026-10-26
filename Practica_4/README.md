# Modelo SIR con Python, SimPy y NetLogo

Práctica 04 de Simulación (UNL, Computación, ciclo 5): comparación de dos implementaciones de una simulación de propagación de infecciones mediante el modelo SIR.

## Estructura del proyecto

Los archivos están directamente en la carpeta raíz de la práctica:

| Archivo | Descripción |
|---------|-------------|
| `model.py` | Estados SIR, parámetros, población y simulación con SimPy. |
| `view.py` | Exporta resultados CSV, genera la gráfica PNG y el reporte HTML. |
| `controller.py` | Ejecuta el modelo y coordina las vistas. |
| `main.py` | Punto de entrada para correr la simulación de Python. |
| `requirements.txt` | Dependencias de Python: SimPy y Matplotlib. |
| `test_model.py`, `test_view.py` | Pruebas automatizadas del modelo y sus salidas. |
| `Codigo_netlogo.nlogox` | Modelo SIR de NetLogo 7.0.4, incluye la simulación y la carga del CSV de Python. |

Al ejecutar Python también se generan `resultados_python.csv`, `grafica_sir_python.png` y `reporte_python.html`.

## Parámetros del modelo

Ambas implementaciones usan población de 100 personas, 5 infectados iniciales, β = 0.30, γ = 0.10 y 100 pasos de tiempo. NetLogo inicia su generador aleatorio con semilla 42; Python usa su propio generador con semilla 42.

La semilla hace reproducible cada implementación, pero **no garantiza que Python y NetLogo produzcan las mismas curvas**: sus generadores aleatorios y el orden de las operaciones al azar son distintos.

En cada paso, las personas infectadas al inicio del paso eligen un contacto al azar. Si es susceptible, se contagia con probabilidad β. Cada infectado de ese inicio también puede recuperarse con probabilidad γ. En ambas implementaciones se usa una copia del estado inicial del paso, de modo que una persona recién infectada no contagia ni se recupera hasta un paso posterior.

## Ejecutar la simulación de Python

Desde la carpeta raíz de la práctica:

```bash
pip install -r requirements.txt
python main.py
```

El programa crea los tres archivos de salida en la carpeta desde la que se ejecuta y abre el reporte HTML en el navegador. Para evitar que se abra automáticamente:

```bash
python main.py --sin-navegador
```

También se puede usar `uv` sin instalar dependencias globalmente:

```bash
uv run --no-project --with simpy --with matplotlib python main.py
```

Con los parámetros predeterminados y la implementación actual, el CSV contiene 101 registros, desde t = 0 hasta t = 100. La primera fila de datos es 0,95,5,0.

## Ejecutar el modelo de NetLogo e importar los datos de Python

1. Ejecuta primero la simulación de Python desde la raíz de la práctica. Esto crea o actualiza `resultados_python.csv`.
2. Abre `Codigo_netlogo.nlogox` con NetLogo 7.0.4.
3. En la pestaña **Code**, revisa el procedimiento `cargar-python`. Actualmente usa esta ruta absoluta para leer el CSV:

   ```netlogo
   csv:from-file "/home/steevenpardo/Documentos/5-CICLO/Simulacion/Unidad_1/Practica_4/resultados_python.csv"
   ```

   Si la carpeta del proyecto está en otra ubicación o en otro equipo, cambia esa cadena por la ruta absoluta del `resultados_python.csv` que generaste. Usa `/` como separador de carpetas. El modelo no busca automáticamente el CSV junto al archivo `.nlogox`.
4. Pulsa **setup** para crear la población de NetLogo y preparar las gráficas.
5. Pulsa **cargar-python** para leer el CSV y dibujar sus 101 filas en la gráfica **Python**.
6. Pulsa **go** para ejecutar la simulación de NetLogo. El botón está configurado para repetir el procedimiento hasta alcanzar 100 ticks; al finalizar se imprime el resumen en el área de salida.

La gráfica **NetLogo** muestra la simulación de agentes en NetLogo; la gráfica **Python** muestra los valores importados desde el archivo CSV. Para comparar los resultados visualmente, ejecuta `setup`, carga Python y luego ejecuta `go`.

El CSV debe conservar esta cabecera y orden de columnas:

```text
tiempo,susceptibles,infectados,recuperados
```

No cambies los nombres ni el orden de las columnas: el procedimiento `cargar-python` toma las columnas por posición.

## Pruebas

Desde la raíz del proyecto:

```bash
python -m unittest -v
```

Las pruebas comprueban, entre otras cosas, que se generen los 101 registros, que la población total se conserve, que la semilla haga repetible el resultado de Python y que se creen correctamente el CSV, la gráfica y el reporte.
