import OrientadaObjetos.Aula02.Cachorro;

public class main {

    public static void main(String[] args) {
        
        Cachorro cachorro1 = new Cachorro();

    cachorro1.nome = "Jolie";
    cachorro1.cor = "Branca";
    cachorro1.altura = 25;
    cachorro1.peso = 5.5;
    cachorro1.tamanhoDoRabo = 5;

    cachorro1.latir();
    
    System.out.println("O cachorro pegou a "+cachorro1.pegar()+".");

    }
}