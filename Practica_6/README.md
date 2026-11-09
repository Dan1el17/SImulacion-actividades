# Practica de simulacion: validacion de numeros pseudoaleatorios

La implementacion de Python genera numeros con un LCG y evalua su uniformidad
con las pruebas Chi-cuadrado y Kolmogorov-Smirnov. Las pruebas se intercambian
mediante el patron Strategy.

## Ejecutar Python

Desde la carpeta `python`:

```bash
python -m pip install -r requirements.txt
python main.py
```

El programa procesa 1 000, 10 000, 100 000 y 1 000 000 numeros. Guarda los
estadisticos, valores p, decisiones y tiempos en
`resultados/resultados_python.csv`.

Para ejecutar las pruebas automaticas, desde la carpeta `python`:

```bash
python -m unittest discover -s test
```

Los parametros iniciales del LCG estan definidos al inicio de `python/main.py`.
Conviene confirmar con el docente que estos parametros y los tamanos de muestra
son los solicitados. La guia menciona tambien una tabla de estimacion de pi,
aunque el objetivo descrito corresponde a las pruebas de uniformidad.