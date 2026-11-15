# Practica 7: estimacion de pi mediante Monte Carlo

Este proyecto estima pi mediante puntos pseudoaleatorios y compara una implementacion en Python con otra en Java. Tambien genera una tabla de resultados, un analisis complementario de chi-cuadrado y graficas.

## Requisitos

- Linux.
- Python 3.9 o posterior.
- JDK 11 o posterior, con los comandos `java` y `javac`.
- Matplotlib, que se instala desde `requirements.txt`.

El calculo no requiere NumPy ni Pandas.

### Instalar los programas necesarios

En Ubuntu o Debian, si aun no estan instalados:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip default-jdk
```

Comprueba que esten disponibles:

```bash
python3 --version
java -version
javac -version
```

En otras distribuciones de Linux, instala Python 3, el modulo `venv`, `pip` y un JDK con el gestor de paquetes correspondiente.

## Preparar el entorno de Python

Abre una terminal en la carpeta principal del proyecto y ejecuta:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

El entorno virtual `.venv` mantiene las dependencias de este proyecto separadas de las del sistema. No se sube a Git porque esta excluido en `.gitignore`.

## Ejecutar la practica

Con el entorno virtual activado, desde la carpeta principal:

```bash
python ejecutar_practica.py
```

El programa compila Java en una carpeta temporal, ejecuta Python y Java para `N = 1 000`, `10 000`, `100 000` y `1 000 000`, verifica que generen la misma secuencia y crea los archivos de resultados dentro de `Resultados/`.

Opcionalmente, se puede indicar otra semilla:

```bash
python ejecutar_practica.py 12345
```

Al terminar, se puede salir del entorno virtual con:

```bash
deactivate
```

## Archivos generados

- `Resultados/tabla_comparativa.csv`: estimacion, error y tiempo de ambos lenguajes.
- `Resultados/chi_cuadrado.csv`: resultados de la prueba complementaria.
- `Resultados/estimacion_pi.png`: estimacion de pi para cada cantidad de puntos.
- `Resultados/error_absoluto.png`: diferencia entre la estimacion y el valor de referencia.
- `Resultados/tiempo_ejecucion.png`: comparacion de tiempos.
- `Resultados/chi_cuadrado.png`: estadistico chi-cuadrado y valor de referencia.

Los tiempos se calculan como la mediana de cinco ejecuciones. Miden la generacion y el procesamiento de puntos; excluyen la compilacion, el inicio del programa y la escritura de archivos. Pueden variar segun el equipo.

## Modelo matematico

Los puntos se generan dentro del cuadrado `[-1, 1] x [-1, 1]`. Un punto `(x, y)` se considera dentro del circulo unitario si cumple:

```text
x^2 + y^2 <= 1
```

Si `N` es el numero total de puntos y `Nc` es la cantidad de puntos dentro del circulo:

```text
pi estimado = 4 * (Nc / N)
error absoluto = abs(pi estimado - 3.141592653589793)
```

## Generador pseudoaleatorio: LCG MINSTD

De acuerdo con el generador congruencial lineal presentado en las diapositivas, ambas implementaciones usan la variante multiplicativa MINSTD con `a = 16807`, `c = 0` y `m = 2 147 483 647`. La sucesion se calcula como `X siguiente = (a * X actual + c) mod m`, y se transforma a un numero entre 0 y 1 dividiendo `X` para `m`.

Python y Java usan la misma semilla (por defecto, `2026`) y la misma conversion a coordenadas, por lo que procesan la misma secuencia. Se valida que la semilla este entre 1 y `m - 1`; una semilla cero no se permite porque el LCG multiplicativo quedaria atascado en cero. El programa verifica la secuencia y los resultados antes de guardar la comparacion.

## Patron de diseno

Se aplica el patron Factory (fabrica simple) para crear el generador LCG MINSTD. Python usa `crear_generador` y Java usa `GeneradorAleatorioFactory`. La fabrica crea el generador elegido sin mezclar esa responsabilidad con el experimento. El generador se crea antes de iniciar el cronometro.

## Organizacion del codigo

- `Python/generador_aleatorio.py`: generador congruencial lineal y fabrica.
- `Python/experimento_montecarlo.py`: conteo de puntos, estimacion, error y chi-cuadrado.
- `Python/configuracion.py`: cantidades de puntos, referencia de pi y parametros.
- `Python/estimacion_pi.py`: ejecucion de la implementacion Python y salida CSV.
- `Python/comparacion.py`: ejecucion cruzada, validacion de la secuencia y guardado de tablas.
- `Python/graficas.py`: creacion de las graficas.
- `ejecutar_practica.py`: coordinador que inicia los componentes.
- `Java/GeneradorAleatorio.java`, `Java/GeneradorCongruencialLineal.java` y `Java/GeneradorAleatorioFactory.java`: contrato, generador congruencial lineal y fabrica.
- `Java/ExperimentoMonteCarlo.java` y `Java/ResultadoExperimento.java`: ejecucion del modelo y sus resultados.
- `Java/EstimacionPi.java`: punto de entrada y presentacion de resultados.

La separacion organiza las responsabilidades sin cambiar el modelo matematico ni los datos del informe. El programa principal coordina las partes; no contiene toda la implementacion del experimento.

## Analisis complementario de chi-cuadrado

El cuadrado se divide en 16 celdas iguales (4 x 4). Para cada celda se espera `N / 16` puntos y se calcula:

```text
chi-cuadrado = suma((observado - esperado)^2 / esperado)
```

Se usan 15 grados de libertad y un nivel de significancia de `0.05`; el valor de referencia es aproximadamente `24.996`. Si el estadistico supera ese valor, se rechaza la hipotesis de distribucion uniforme para esta prueba. Si no lo supera, no se rechaza la hipotesis, pero eso no demuestra que la distribucion sea perfectamente uniforme.

