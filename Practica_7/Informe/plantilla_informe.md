# Practica 7: estimacion de resultados mediante Monte Carlo

## Objetivo

Aplicar el metodo de Monte Carlo para estimar pi y comparar las implementaciones realizadas en Python y Java.

## Modelo matematico

Se considera un cuadrado de lado 2, representado por `[-1, 1] x [-1, 1]`, y un circulo unitario inscrito. Un punto `(x, y)` pertenece al circulo cuando `x^2 + y^2 <= 1`.

Si `N` es el numero total de puntos y `Nc` es el numero de puntos dentro del circulo, la estimacion es:

`pi_estimado = 4 * (Nc / N)`

El error absoluto es:

`error = abs(pi_estimado - 3.141592653589793)`

## Metodologia

1. Se genero una secuencia pseudoaleatoria con un generador congruencial lineal MINSTD (`a = 16807`, `c = 0`, `m = 2 147 483 647`) y una semilla fija.
2. Se genero cada punto dentro del cuadrado `[-1, 1] x [-1, 1]` y se conto si cumplia `x^2 + y^2 <= 1`.
3. Se repitio el experimento para 1 000, 10 000, 100 000 y 1 000 000 de puntos.
4. Se implemento el mismo algoritmo y la misma secuencia pseudoaleatoria en Python y Java.
5. Se midio el tiempo de generacion y conteo en cinco ejecuciones por muestra; se reporto la mediana.
6. Como analisis complementario, se dividio el cuadrado en 16 celdas iguales y se compararon las frecuencias observadas con las esperadas mediante chi-cuadrado.

## Resultados

Inserta aqui la tabla generada en `Resultados/tabla_comparativa.csv` y las graficas `estimacion_pi.png`, `error_absoluto.png` y `tiempo_ejecucion.png`.

| N | Pi estimado Python | Error Python | Tiempo Python (ms) | Pi estimado Java | Error Java | Tiempo Java (ms) |
|---:|---:|---:|---:|---:|---:|---:|
| 1 000 | | | | | | |
| 10 000 | | | | | | |
| 100 000 | | | | | | |
| 1 000 000 | | | | | | |

Inserta tambien los resultados de `Resultados/chi_cuadrado.csv` y la grafica `Resultados/chi_cuadrado.png`.

## Analisis de resultados

Responde con los valores obtenidos:

1. Como cambia la estimacion de pi al aumentar el numero de puntos?
2. Como se relaciona el tamano de muestra con el error absoluto?
3. Para que tamano de muestra se obtuvo la aproximacion mas cercana?
4. Que lenguaje tuvo menor tiempo mediano en este equipo?
5. Por que podrian diferir Python y Java si usan generadores o semillas distintos? En esta implementacion, por que coinciden sus estimaciones?
6. Que papel cumplen los numeros pseudoaleatorios en Monte Carlo?
7. El aumento de N garantiza que cada ejecucion tenga menor error? Explica la diferencia entre tendencia y garantia.
8. Que aplicaciones del metodo Monte Carlo se pueden encontrar en ingenieria, economia, informatica y ciencias?
9. En la prueba chi-cuadrado, cual fue el estadistico de cada muestra y que decision se obtuvo frente al valor critico? Explica por que no rechazar uniformidad no demuestra uniformidad perfecta.

## Preguntas de control

1. Que es el metodo Monte Carlo?
2. Por que suele disminuir el error al aumentar las muestras?
3. Que relacion existe entre precision y costo computacional?
4. Que diferencias se observaron entre Python y Java?
5. En que otros problemas se puede utilizar Monte Carlo?

## Conclusiones

Escribe conclusiones relacionadas con el objetivo, la tendencia del error, los tiempos medidos y el analisis de uniformidad. No afirmes que una muestra grande garantiza una estimacion mas cercana en cada ejecucion.

## Observacion

La rubrica de la guia menciona M/M/1, aunque el objetivo, el procedimiento y los resultados esperados describen la estimacion de pi. Confirma con el docente si esa mencion aplica a esta practica.
