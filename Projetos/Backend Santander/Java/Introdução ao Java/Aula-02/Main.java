

public class Main {
    
    public static void main(String[] args) {

        boolean fimDeSemana = true;
        //boolean fazendoSol = true;
        //boolean vamosAPraia = fimDeSemana && fazendoSol;

        // Tabla verdade JAVA
        // Operador && (AND)
        // true  && true = true
        // true  && false = false
        // false && true = false
        // false && false = false

        // Operador || (OR)
        // true  || true = true
        // true  || false = true
        // false || true = true
        // false || false = false

        //System.out.println(vamosAPraia);

        String mensagem = fimDeSemana ? "É fim de semana e tem sol,  Bora?" : "Não é fim de semana.";
        System.out.println(mensagem);
    }
}
