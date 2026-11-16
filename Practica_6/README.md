# Generador y pruebas de uniformidad

Proyecto en Python y Java para generar secuencias con un generador
congruencial lineal (LCG), ejecutar pruebas de uniformidad y estimar pi por
simulacion. Las implementaciones comparten los mismos parametros para poder
comparar sus resultados.

## Tecnologias

- Python 3.9 o posterior
- SciPy y Matplotlib
- JDK 17 o posterior

## Instalacion y uso

### Python

Desde el directorio `python/`:

```bash
python -m pip install -r requirements.txt
python main.py
python -m unittest discover -s test
```

### Java

Desde el directorio `java/`:

```bash
javac --release 17 -d target/classes src/main/java/practica6/*.java
java -cp target/classes practica6.EstimacionPi
```

### Comparar las implementaciones

Despues de ejecutar Python y Java, desde `python/`:

```bash
python compare_results.py
```

El comparador comprueba las huellas SHA-256 de las secuencias usadas para
estimar pi y genera una tabla comparativa. Los tiempos dependen del equipo y
de las condiciones de ejecucion.

## Archivos generados

Los programas escriben sus resultados en `resultados/`:

- `resultados_python.csv`: frecuencias, estadisticos, valores p, decisiones y
  tiempos de las pruebas de uniformidad en Python.
- `resultados_uniformidad_java.csv`: los mismos resultados de las pruebas en
  Java.
- `resultados_pi_python.csv` y `resultados_pi_java.csv`: estimaciones de pi,
  errores, tiempos y huellas de las secuencias de cada lenguaje.
- `comparacion_pi.csv`: comparacion de las estimaciones de ambos lenguajes.
- `ecdf_ks_python.png` y `ecdf_ks_java.svg`: graficas de las distribuciones
  acumuladas usadas para visualizar la prueba KS.

## Estructura

```text
Practica_6/
├── java/
│   ├── pom.xml
│   └── src/main/java/practica6/
├── python/
│   ├── main.py
│   ├── compare_results.py
│   ├── requirements.txt
│   ├── src/
│   └── test/
└── resultados/
```

En Python, `src/generadores/` contiene el generador y `src/pruebas/` las
pruebas de uniformidad. En Java, `LCG` genera la secuencia y las clases que
implementan `UniformityTest` proporcionan las pruebas mediante el patron
Strategy.
