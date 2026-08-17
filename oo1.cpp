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
#include <iostream>
#include <string>

// Classe Pessoa
class Pessoa {
public:
    // Atributos
    std::string nome = "";
    std::string cpf = "";
    int idade = 0;

    // Métodos
    void caminhar() {
        std::cout << "Pessoa caminhando" << std::endl;
    }

    void correr() {
        std::cout << "Pessoa correndo" << std::endl;
    }
};

int main() {
    // pessoa1 é um objeto
    Pessoa pessoa1;
    pessoa1.nome = "José da Silva";
    pessoa1.idade = 20;
    pessoa1.cpf = "123";

    // pessoa2 é outro objeto
    Pessoa pessoa2;
    pessoa2.nome = "Maria da Silva";
    pessoa2.idade = 25;
    pessoa2.cpf = "321";

    return 0;
}
