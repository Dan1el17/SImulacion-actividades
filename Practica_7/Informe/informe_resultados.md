# Practica 7: estimacion de resultados mediante Monte Carlo

## Objetivo

Aplicar el metodo de Monte Carlo para aproximar numericamente el valor de pi, estudiar el efecto del tamano de muestra y comparar los tiempos de ejecucion de Python y Java. Como analisis complementario indicado por el docente, se aplico una prueba chi-cuadrado a la distribucion de puntos en una cuadricula.

## Modelo matematico

Se considera un cuadrado de lado 2, representado por la region `[-1, 1] x [-1, 1]`, que contiene un circulo unitario centrado en el origen. Un punto `(x, y)` esta dentro del circulo cuando:

`x^2 + y^2 <= 1`

El area del circulo es `pi` y la del cuadrado es `4`. Por tanto, la proporcion de puntos del cuadrado que caen dentro del circulo aproxima `pi / 4`. Si `N` es el numero total de puntos generados y `Nc` el numero de puntos dentro del circulo, se estima:

`pi_estimado = 4 * (Nc / N)`

El error absoluto se calcula con:

`error = abs(pi_estimado - 3.141592653589793)`

## Metodologia

1. Se genero cada coordenada pseudoaleatoria dentro del cuadrado y se verifico si el punto satisfacia `x^2 + y^2 <= 1`.
2. Se ejecuto el experimento para `N = 1 000`, `10 000`, `100 000` y `1 000 000`.
3. Se implemento el mismo generador congruencial lineal MINSTD (`a = 16807`, `c = 0`, `m = 2 147 483 647`) en Python y Java, con la misma semilla (`2026`). El programa valida la secuencia mediante un hash y compara los resultados numericos.
4. El tiempo mide la generacion de puntos, el conteo dentro del circulo y la asignacion de puntos a las celdas. Se excluyen compilacion, inicio del proceso y escritura de archivos. Se realizaron cinco ejecuciones por muestra y se reporta la mediana.
5. Para chi-cuadrado, se dividio el cuadrado en 16 celdas iguales (4 x 4). Para cada celda se espero `N / 16` puntos y se calculo `suma((observado - esperado)^2 / esperado)`. Con 15 grados de libertad y `alfa = 0.05`, se comparo el estadistico con el valor critico `24.99579`.

## Resultados de Monte Carlo

Resultados generados en el entorno de ejecucion del proyecto: Python 3.14.8 y OpenJDK 25.0.4.1. Los tiempos dependen del computador y pueden cambiar al ejecutar de nuevo.

| N | Puntos dentro (Nc) | Pi estimado Python | Error absoluto Python | Tiempo Python (ms) | Pi estimado Java | Error absoluto Java | Tiempo Java (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 000 | 787 | 3.148000 | 0.00640735 | 1.135422 | 3.148000 | 0.00640735 | 0.303108 |
| 10 000 | 7 870 | 3.148000 | 0.00640735 | 9.891268 | 3.148000 | 0.00640735 | 2.061223 |
| 100 000 | 78 468 | 3.138720 | 0.00287265 | 96.155710 | 3.138720 | 0.00287265 | 5.023168 |
| 1 000 000 | 785 193 | 3.140772 | 0.00082065 | 950.780621 | 3.140772 | 0.00082065 | 12.906603 |

Las dos implementaciones usaron la misma secuencia pseudoaleatoria y obtuvieron el mismo conteo y estimacion para cada `N`. Los tiempos son mediciones de este entorno, no una propiedad universal de los lenguajes.

## Resultados de chi-cuadrado

| N | Esperado por celda | Estadistico chi-cuadrado | gl | Valor critico (alfa = 0.05) | Decision |
|---:|---:|---:|---:|---:|---|
| 1 000 | 62.5 | 13.3120 | 15 | 24.9958 | No se rechaza uniformidad |
| 10 000 | 625 | 13.1296 | 15 | 24.9958 | No se rechaza uniformidad |
| 100 000 | 6 250 | 16.3107 | 15 | 24.9958 | No se rechaza uniformidad |
| 1 000 000 | 62 500 | 10.8332 | 15 | 24.9958 | No se rechaza uniformidad |

Los valores de Python y Java coinciden salvo diferencias de redondeo numerico insignificantes, porque se evaluo la misma secuencia. En los cuatro tamanos de muestra, el estadistico chi-cuadrado quedo por debajo del valor critico. Por ello, en esta prueba no se rechazo la hipotesis de uniformidad; esto no demuestra que la distribucion sea perfectamente uniforme.

## Graficas

- [Estimacion de pi](../Resultados/estimacion_pi.png)
- [Error absoluto](../Resultados/error_absoluto.png)
- [Tiempo de ejecucion](../Resultados/tiempo_ejecucion.png)
- [Estadistico chi-cuadrado](../Resultados/chi_cuadrado.png)

## Analisis de resultados

1. **Cambio de la estimacion al aumentar N:** las estimaciones fueron 3.148, 3.148, 3.13872 y 3.140772. Los resultados fluctuan alrededor del valor de pi y no cambian necesariamente en una sola direccion.
2. **Tamano de muestra y error:** el error fue 0.00640735, 0.00640735, 0.00287265 y 0.00082065, respectivamente. En esta ejecucion, las muestras mayores terminaron con errores menores, aunque esto no esta garantizado para cada ejecucion.
3. **Mejor aproximacion:** `N = 1 000 000`, con un error absoluto aproximado de `0.00082065`.
4. **Menor tiempo:** Java fue mas rapido en estas mediciones. La comparacion depende del equipo, de la version de cada lenguaje y de los detalles de implementacion.
5. **Diferencias entre lenguajes:** cuando cada lenguaje usa un generador o semilla distinta, puede producir puntos diferentes y, por ello, estimaciones diferentes. Aqui se implemento el mismo generador, la misma semilla y la misma conversion a coordenadas; por eso coinciden las muestras y las estimaciones.
6. **Importancia de los numeros pseudoaleatorios:** representan las muestras del experimento. La calidad y distribucion de esos valores influyen en la confiabilidad de las aproximaciones.
7. **Garantia de acercarse a pi:** no. Aumentar el numero de puntos mejora la precision esperada, pero no garantiza que cada ejecucion sea mas cercana que la anterior.
8. **Aplicaciones:** estimacion de integrales y riesgos en ingenieria; simulacion de escenarios financieros en economia; pruebas probabilisticas y estimacion de rendimiento en informatica; y modelos de fenomenos en fisica, biologia y otras ciencias.
9. **Chi-cuadrado:** ninguna muestra supero el valor critico en esta ejecucion. La prueba solo examina la distribucion en una cuadricula de 4 x 4 para esta secuencia; no es una prueba definitiva de calidad del generador ni una medida del error de pi.

## Preguntas de control

1. **Que es Monte Carlo?** Es una familia de metodos que utiliza muestreo aleatorio para estimar resultados numericos o estudiar sistemas.
2. **Por que suele disminuir el error al aumentar las muestras?** Una muestra mayor reduce la influencia relativa de las fluctuaciones aleatorias; aun asi, el error de una ejecucion no tiene que disminuir siempre.
3. **Relacion entre precision y costo computacional:** normalmente, mas muestras mejoran la precision esperada, pero requieren mas operaciones y tiempo.
4. **Diferencias entre Python y Java:** con el mismo flujo de puntos, los resultados numericos coincidieron. Java tuvo menor tiempo en esta medicion; la conclusion de rendimiento se limita al equipo y al codigo usados.
5. **Otros usos de Monte Carlo:** integracion numerica, evaluacion de riesgos, simulacion de colas, modelado de inventarios y estimacion de probabilidades complejas.

## Conclusiones

El experimento permitio estimar pi con cuatro tamanos de muestra e implementar el mismo procedimiento en Python y Java con un generador congruencial lineal MINSTD. El error mas pequeno se obtuvo con un millon de puntos. Java fue mas rapido en el entorno medido, pero esa diferencia debe interpretarse considerando el hardware y las condiciones de ejecucion. La prueba chi-cuadrado no rechazo la uniformidad en los cuatro tamanos de muestra; esto es evidencia limitada a la cuadrilla y secuencia examinadas, no una certificacion general del generador.

## Nota sobre el alcance

El procedimiento y los resultados esperados de la guia tratan de estimar pi con Monte Carlo, mientras una linea de la rubrica menciona un modelo M/M/1. Este informe sigue el objetivo y el procedimiento detallados. Se debe consultar al docente si tambien espera una simulacion M/M/1 como parte de esta practica.
