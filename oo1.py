"""
O que é importante em uma pessoa ?
Dados:
 - Nome
 - CPF
 - idade
 Ação:
  - caminhar
  - correr
"""
# Classe Pessoa
class Pessoa:
    # Atributos 
    nome = ''
    cpf = ''
    idade = 0
    # Métodos
    def caminhar(self):
        print('Pessoa caminhando')
    
    def correr(self):
        print('Pessoa correndo')

# pessoa1 é um objeto
pessoa1 = Pessoa()
pessoa1.nome = "José da Silva"
pessoa1.idade = 20
pessoa1.cpf = '123'

# pessoa2 é outro objeto
pessoa2 = Pessoa()
pessoa2.nome = "Maria da Silva"
pessoa2.idade = 25
pessoa2.cpf = '321'