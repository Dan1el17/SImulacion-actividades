from pathlib import Path

from controller.simulacion_controller import SimulacionController
from view.consola_view import ConsolaView
from view.grafica_view import GraficaView

RUTA_DATOS = Path(__file__).resolve().parent / "datos.csv"


def main():
    controlador = SimulacionController(RUTA_DATOS, ConsolaView(), GraficaView())
    controlador.ejecutar()


if __name__ == "__main__":
    main()