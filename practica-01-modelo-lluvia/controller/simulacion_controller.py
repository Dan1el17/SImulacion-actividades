from model.factor_temperatura import FactorLineal
from model.modelo_lluvia import ModeloLluvia
from model.observacion_factory import ObservacionFactory


class SimulacionController:
    def __init__(self, ruta_datos, vista_consola, vista_grafica):
        self.ruta_datos = ruta_datos
        self.consola = vista_consola
        self.grafica = vista_grafica

    def ejecutar(self):
        observaciones = ObservacionFactory.desde_csv(self.ruta_datos)

        modelos = [
            ModeloLluvia("Modelo original", FactorLineal(), pesos=(0.5, 0.3, 0.2)),
            ModeloLluvia("Modelo ajustado", FactorLineal(), pesos=(0.4, 0.4, 0.2)),
        ]

        for m in modelos:
            resultados = m.simular(observaciones)
            titulo = f"{m.nombre} ({m.wh}H + {m.wn}N + {m.wt}Tf)"
            archivo = m.nombre.lower().replace(" ", "_") + ".png"

            self.consola.mostrar_tabla(m.nombre, resultados)
            self.grafica.mostrar_indice(resultados, titulo, guardar=archivo)