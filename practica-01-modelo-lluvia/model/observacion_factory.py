import csv
from model.observacion import Observacion


class ObservacionFactory:
    @staticmethod
    def crear(hora, humedad, nubosidad, temp) -> Observacion:
        return Observacion(hora, float(humedad) / 100, float(nubosidad) / 100, float(temp))

    @staticmethod
    def desde_csv(ruta) -> list[Observacion]:
        with open(ruta, newline="", encoding="utf-8") as f:
            return [ObservacionFactory.crear(**fila) for fila in csv.DictReader(f)]