package practica6;

public final class LCG {
    private final long multiplicador;
    private final long incremento;
    private final long modulo;
    private long estado;

    public LCG(long semilla, long multiplicador, long incremento, long modulo) {
        if (modulo <= 0) {
            throw new IllegalArgumentException("El modulo debe ser mayor que cero");
        }
        if (semilla < 0 || semilla >= modulo) {
            throw new IllegalArgumentException("La semilla debe estar entre 0 y modulo - 1");
        }
        if (multiplicador < 0 || multiplicador >= modulo) {
            throw new IllegalArgumentException(
                    "El multiplicador debe estar entre 0 y modulo - 1");
        }
        if (incremento < 0 || incremento >= modulo) {
            throw new IllegalArgumentException(
                    "El incremento debe estar entre 0 y modulo - 1");
        }

        this.estado = semilla;
        this.multiplicador = multiplicador;
        this.incremento = incremento;
        this.modulo = modulo;
    }

    public long siguienteEntero() {
        estado = (multiplicador * estado + incremento) % modulo;
        return estado;
    }

    public double siguiente() {
        return (double) siguienteEntero() / modulo;
    }

    public long getModulo() {
        return modulo;
    }
}
