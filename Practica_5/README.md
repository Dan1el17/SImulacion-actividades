# Práctica 5: Generador Congruencial Lineal

## Descripción

Esta práctica implementa el Generador Congruencial Lineal (LCG) en Python y
Java. Ambos programas generan 10 000 valores usando la misma fórmula,
parámetros y semilla, e imprimen las primeras 20 observaciones para comparar
los resultados. La versión de Python también muestra una gráfica de valores
consecutivos.

La fórmula utilizada es:

```text
X(n+1) = (a * X(n) + c) mod m
```

Parámetros usados:

| Parámetro | Valor |
|---|---:|
| `a` | 1664525 |
| `c` | 1013904223 |
| `m` | 2³² |
| Semilla | 12345 |

## Tecnologías

- Python 3
- Matplotlib
- Java JDK 17 o posterior

## Instalación y ejecución

### Python

Desde la carpeta `Practica_5/Python`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

El programa imprime las primeras 20 observaciones y muestra una gráfica de
dispersión de `X(n)` frente a `X(n+1)`.

### Java

Desde la carpeta `Practica_5/Java`:

```bash
javac --release 17 -d out GeneradorCongruencial.java Main.java
java -cp out Main
```

El programa genera 10 000 valores e imprime las primeras 20 observaciones.

## Estructura del proyecto

```text
Practica_5/
├── README.md
├── Java/
│   ├── GeneradorCongruencial.java
│   └── Main.java
└── Python/
    ├── generador.py
    ├── grafica_lcg.png
    ├── main.py
    └── requirements.txt
```

- `GeneradorCongruencial.java` y `generador.py`: implementan el generador y
  sus operaciones.
- `Main.java` y `main.py`: ejecutan el generador y muestran las primeras
  observaciones.
- `grafica_lcg.png`: gráfica de la secuencia para incluir en el informe.
- `requirements.txt`: dependencia necesaria para Python.
