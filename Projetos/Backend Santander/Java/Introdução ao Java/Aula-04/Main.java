
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.TextStyle;
import java.util.Locale;


public class Main {
    

    public static void main(String[] args) {

        String nome = "Rui";
        LocalDate hoje = LocalDate.now();
        @SuppressWarnings("deprecation")
        Locale brasil = new Locale("pt", "BR");
        String diaSemana = hoje.getDayOfWeek().getDisplayName(TextStyle.FULL, brasil);
        String saudacao;
        LocalDateTime agora = LocalDateTime.now();

        if (agora.getHour() >= 0 && agora.getHour() < 12) {
            saudacao = "Bom dia!";
        }
        else if (agora.getHour() >= 12 && agora.getHour() < 18) {
            saudacao = "Boa tarde!";
        }
        if (agora.getHour() >= 18 && agora.getHour() < 24) {
            saudacao = "Boa noite!";
        }
        else{
            saudacao = " ";
        }

        System.out.printf("Olá, %s.%nHoje é %s, %s.%n" ,nome, diaSemana, saudacao);
    System.out.println(agora);
        // System.out.println(nome.toUpperCase());
        // System.out.println(nome.toLowerCase());
        // System.out.println(nome.length());

        // String nomeOutro = "rui";

        // System.out.println(nome.equals(nomeOutro));
        // System.out.println(nome.equalsIgnoreCase(nomeOutro));


    }
}
