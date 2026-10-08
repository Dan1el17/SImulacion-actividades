from model.observacion import Observacion, Resultado
from model.factor_temperatura import FactorTemperatura


class ModeloLluvia:
    def __init__(self, nombre: str, factor: FactorTemperatura, pesos=(0.5, 0.3, 0.2)):
        self.nombre = nombre
        self.factor = factor
        self.wh, self.wn, self.wt = pesos

    def _clasificar(self, i: float) -> str:
        if i < 0.40:
            return "Sin lluvia"
        if i < 0.60:
            return "Baja posibilidad"
        if i < 0.75:
            return "Lluvia probable"
        return "Lluvia"

    def evaluar(self, obs: Observacion) -> Resultado:
        tf = self.factor.calcular(obs.temp)
        indice = round(self.wh * obs.h + self.wn * obs.n + self.wt * tf, 4)
        return Resultado(obs, tf, indice, self._clasificar(indice))

    def simular(self, observaciones: list[Observacion]) -> list[Resultado]:
        return [self.evaluar(o) for o in observaciones]