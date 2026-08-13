/*
O que é importante em uma pessoa ?
Dados:
 - Nome
 - CPF
 - idade
 Ação:
  - caminhar
  - correr
*/

// Classe Pessoa
class Pessoa {
    // Atributos
    String nome = "";
    String cpf = "";
    int idade = 0;

    // Métodos
    void caminhar() {
        System.out.println("Pessoa caminhando");
    }

    void correr() {
        System.out.println("Pessoa correndo");
    }
}

public class oo1 {
    public static void main(String[] args) {
        // pessoa1 é um objeto
        Pessoa pessoa1 = new Pessoa();
        pessoa1.nome = "José da Silva";
        pessoa1.idade = 20;
        pessoa1.cpf = "123";

        // pessoa2 é outro objeto
        Pessoa pessoa2 = new Pessoa();
        pessoa2.nome = "Maria da Silva";
        pessoa2.idade = 25;
        pessoa2.cpf = "321";
    }
}
