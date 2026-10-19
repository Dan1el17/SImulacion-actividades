# Práctica 02: Comparación de modelos determinísticos, estocásticos, discretos y continuos

**Asignatura:** Simulación (ciclo 5, Computación)
**Universidad Nacional de Loja**
**Docente:** José O. Guamán Q.
**Sistema de estudio:** crecimiento poblacional
**Tecnología:** Python + NumPy + Matplotlib + SciPy

---

## 1. ¿Qué hace la práctica y cuál es su objetivo?

Se comparan **cuatro formas** de modelar el crecimiento poblacional usando el
mismo conjunto de datos.

**Objetivo:** ver en qué se parecen y en qué se diferencian los modelos
determinístico, discreto, estocástico y continuo, cómo influye la tasa `r` y
observar tanto el **crecimiento** como el **decrecimiento**.

| Modelo | Fórmula | ¿Usa azar? |
|---|---|---|
| Determinístico | `P(t) = P0 * e^(r*t)` | No |
| Discreto | `P(t+1) = P(t) + r * P(t)` | No |
| Estocástico | `P(t+1) = P(t) + r * P(t) + ε`, con `ε ~ N(0, σ²)` | Sí |
| Continuo (Euler) | `P(t + Δt) = P(t) + Δt * (r * P(t))` | No |

> Regla del modelo estocástico: si la población queda por debajo de 0, se deja en **0**.

**Parámetros:** `P0`, `r`, `sigma`, `dt` y `tiempo`.

**¿Cómo se obtiene `r`?** La guía no indica cómo calcularla, así que se obtiene
del propio arreglo de datos con una regresión lineal de `ln(P)` contra `t`
(la pendiente es `r`), explicado en `parametros.py`. `sigma` se estima con la
desviación estándar de los residuos de esa regresión.

**Datos de entrada por defecto:**

```text
1000, 1100, 1250, 1400, 1600, 1850, 2100
```

**Escenarios que se grafican:**

1. **Crecimiento** (`r > 0`): compara los 4 modelos con la `r` calculada.
2. **Decrecimiento** (`r < 0`): usa una `r` negativa a propósito.
3. **Influencia de `r`**: determinístico con `r*0.5`, `r` y `r*1.5`.

Todas las gráficas llevan título, eje X "Tiempo", eje Y "Poblacion", leyenda y
cuadrícula.

---

## 2. Tecnologías

- Python 3.11+
- NumPy – ruido gaussiano
- Matplotlib – gráficas
- SciPy – regresión lineal para calcular `r`
- pytest – pruebas

---

## 3. Estructura del proyecto

```text
Practica_2/
├── modelos.py            # clase base + los 4 modelos (Strategy) + fábrica (Factory)
├── parametros.py         # cálculo de r y sigma desde los datos
├── grafica.py            # gráficas con matplotlib
├── main.py               # punto de entrada
├── tests/
│   ├── __init__.py
│   ├── test_modelos.py
│   └── test_parametros.py
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 4. Patrones de diseño aplicados

Todos en `modelos.py`, pequeños y fáciles de leer:

- **Clase base:** `ModeloPoblacion` guarda los datos comunes (`P0`, `r`,
  `tiempo`, `nombre`) y define `calcular()`.
- **Strategy:** cada modelo (`ModeloDeterministico`, `ModeloDiscreto`,
  `ModeloEstocastico`, `ModeloContinuoEuler`) implementa su propio `calcular()`;
  el resto del programa usa siempre `modelo.ejecutar()`.
- **Factory:** `crear_modelo(nombre, ...)` devuelve el modelo correcto sin que
  el programa principal conozca las clases.

---

## 5. Instalación (Fedora Linux)

```bash
sudo dnf install python3 python3-pip git
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 6. Cómo ejecutar y probar

```bash
python main.py     # calcula r y sigma, ejecuta los 4 modelos y muestra las gráficas
pytest -v          # ejecuta las pruebas
```

---


