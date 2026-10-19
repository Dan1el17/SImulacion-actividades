import math

import pytest

from modelos import (
    ModeloContinuoEuler,
    ModeloDeterministico,
    ModeloDiscreto,
    ModeloEstocastico,
    NOMBRES_MODELOS,
    crear_modelo,
    ejecutar_todos,
)


def test_crear_modelo_devuelve_clase_correcta():
    assert isinstance(crear_modelo("deterministico", 1000, 0.1, 5), ModeloDeterministico)
    assert isinstance(crear_modelo("discreto", 1000, 0.1, 5), ModeloDiscreto)
    assert isinstance(crear_modelo("estocastico", 1000, 0.1, 5, sigma=0.05), ModeloEstocastico)
    assert isinstance(crear_modelo("continuo_euler", 1000, 0.1, 5), ModeloContinuoEuler)


def test_crear_modelo_nombre_invalido():
    with pytest.raises(ValueError):
        crear_modelo("inexistente", 1000, 0.1, 5)


def test_deterministico_crecimiento():
    modelo = ModeloDeterministico(1000, 0.1, 5)
    tiempos, poblaciones = modelo.ejecutar()
    assert len(tiempos) == len(poblaciones)
    assert tiempos[0] == 0
    assert poblaciones[0] == 1000
    assert poblaciones[-1] > poblaciones[0]
    assert poblaciones[-1] == pytest.approx(1000 * math.exp(0.1 * 5))


def test_deterministico_decrecimiento():
    modelo = ModeloDeterministico(1000, -0.1, 5)
    _, poblaciones = modelo.ejecutar()
    assert poblaciones[-1] < poblaciones[0]


def test_discreto():
    modelo = ModeloDiscreto(1000, 0.1, 3)
    tiempos, poblaciones = modelo.ejecutar()
    assert tiempos == [0, 1, 2, 3]
    esperado = [1000]
    p = 1000
    for _ in range(3):
        p = p + 0.1 * p
        esperado.append(p)
    assert poblaciones == pytest.approx(esperado)


def test_estocastico_no_baja_de_cero_y_es_reproducible():
    a = ModeloEstocastico(1000, -0.5, 10, sigma=0.3, semilla=42)
    b = ModeloEstocastico(1000, -0.5, 10, sigma=0.3, semilla=42)
    ta, pa = a.ejecutar()
    tb, pb = b.ejecutar()
    assert pa == pb  # misma semilla -> mismo resultado
    assert all(p >= 0 for p in pa)


def test_estocastico_cero_sigma_igual_a_discreto():
    estoc = ModeloEstocastico(1000, 0.1, 5, sigma=0.0, semilla=1)
    disc = ModeloDiscreto(1000, 0.1, 5)
    _, p_estoc = estoc.ejecutar()
    _, p_disc = disc.ejecutar()
    assert p_estoc == pytest.approx(p_disc)


def test_continuo_euler():
    modelo = ModeloContinuoEuler(1000, 0.1, 5, dt=0.1)
    tiempos, poblaciones = modelo.ejecutar()
    assert len(tiempos) == len(poblaciones)
    assert tiempos[0] == 0
    assert poblaciones[0] == 1000
    assert poblaciones[-1] > poblaciones[0]
    assert tiempos[-1] == pytest.approx(5, abs=1e-9)


def test_ejecutar_todos_devuelve_cuatro_series():
    series = ejecutar_todos(1000, 0.1, 5, sigma=0.05, dt=0.1)
    assert len(series) == len(NOMBRES_MODELOS)
    for nombre, tiempos, poblaciones in series:
        assert isinstance(nombre, str)
        assert len(tiempos) == len(poblaciones)
