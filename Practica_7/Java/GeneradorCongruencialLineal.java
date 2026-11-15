public final class GeneradorCongruencialLineal implements GeneradorAleatorio {
    public static final long MODULO = 2_147_483_647L;
    private static final long MULTIPLICADOR = 16_807L;
    private static final long INCREMENTO = 0L;

    private long estado;

    GeneradorCongruencialLineal(long semilla) {
        if (semilla < 1 || semilla >= MODULO) {
            throw new IllegalArgumentException("La semilla debe estar entre 1 y " + (MODULO - 1) + ".");
        }
        estado = semilla;
    }

    @Override
    public long siguienteEntero() {
        estado = (MULTIPLICADOR * estado + INCREMENTO) % MODULO;
        return estado;
    }

    @Override
    public double siguienteReal() {
        return (double) siguienteEntero() / MODULO;
    }
}
