import pytest

from parametros import calcular_r, calcular_sigma

DATOS = [1000, 1100, 1250, 1400, 1600, 1850, 2100]


def test_calcular_r_positivo_con_datos_crecientes():
    r = calcular_r(DATOS)
    assert r > 0


def test_calcular_r_negativo_con_datos_decrecientes():
    r = calcular_r([2100, 1850, 1600, 1400, 1250, 1100, 1000])
    assert r < 0


def test_calcular_r_exponencial_exacta():
    # Datos generados con r = 0.2 exacto -> la regresion debe recuperarlo
    P0 = 1000.0
    datos = [P0 * (2.718281828459045 ** (0.2 * t)) for t in range(6)]
    r = calcular_r(datos)
    assert r == pytest.approx(0.2, abs=1e-3)


def test_calcular_r_requiere_al_menos_dos_datos():
    with pytest.raises(ValueError):
        calcular_r([1000])


def test_calcular_r_rechaza_cero_o_negativos():
    with pytest.raises(ValueError):
        calcular_r([1000, 0, 1200])


def test_calcular_sigma_positivo():
    r = calcular_r(DATOS)
    sigma = calcular_sigma(DATOS, r)
    assert sigma > 0
