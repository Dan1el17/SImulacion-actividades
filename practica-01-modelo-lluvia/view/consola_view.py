class ConsolaView:
    def mostrar_tabla(self, titulo, resultados):
        print(f"\n=== {titulo} ===")
        print(f"{'Hora':<6}{'Hum':>5}{'Nub':>5}{'Temp':>6}{'H':>7}{'N':>7}{'Tf':>7}{'Índice':>9}  Estado")
        for r in resultados:
            o = r.observacion
            print(f"{o.hora:<6}{o.h*100:>5.0f}{o.n*100:>5.0f}{o.temp:>6.0f}"
                  f"{o.h:>7.2f}{o.n:>7.2f}{r.tf:>7.2f}{r.indice:>9.3f}  {r.estado}")