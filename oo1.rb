# O que é importante em uma pessoa ?
# Dados:
#  - Nome
#  - CPF
#  - idade
#  Ação:
#   - caminhar
#   - correr

# Classe Pessoa
class Pessoa
  # Atributos
  attr_accessor :nome, :cpf, :idade

  def initialize
    @nome = ''
    @cpf = ''
    @idade = 0
  end

  # Métodos
  def caminhar
    puts 'Pessoa caminhando'
  end

  def correr
    puts 'Pessoa correndo'
  end
end

# pessoa1 é um objeto
pessoa1 = Pessoa.new
pessoa1.nome = 'José da Silva'
pessoa1.idade = 20
pessoa1.cpf = '123'

# pessoa2 é outro objeto
pessoa2 = Pessoa.new
pessoa2.nome = 'Maria da Silva'
pessoa2.idade = 25
pessoa2.cpf = '321'
