public class GeneradorCongruencial {
    private static final long A = 1664525L;
    private static final long C = 1013904223L;
    private static final long M = 1L << 32;

    private final long semilla;
    private long estado;

    public GeneradorCongruencial(long semilla) {
        this.semilla = semilla;
        this.estado = semilla;
    }

    public long siguiente() {
        estado = (A * estado + C) % M;
        return estado;
    }

    public long[] generar(int cantidad) {
        long[] valores = new long[cantidad];
        for (int i = 0; i < cantidad; i++) {
            valores[i] = siguiente();
        }
        return valores;
    }

    public double normalizar(long valor) {
        return (double) valor / M;
    }

    public long getSemilla() {
        return semilla;
    }
}
