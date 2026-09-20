from tokens import Token

tabela_de_simbolos = ["inicio", "varinicio", "varfim",
                    "escreva", "leia", "se", "entao",
                    "fimse", "faca-ate", "fimfaca",
                    "fim", "inteiro", "literal", "real"]

tabela = {}


# Guarda as palavras reservadas na classe token 
def iniciar():
    for palavra in tabela_de_simbolos:
        inserir(Token(palavra, palavra, palavra))


# Guarda o token na tabela usando o lexema como chave.
# Quem verifica se já existe é quem chama (o scanner, com busca()).
# Se a chave já existisse, esta linha substituiria o valor antigo.
def inserir(token):
    tabela[token.lexema] = token


# Procura pelo lexema e devolve o Token guardado, ou None se não achar.
# O .get() calcula o hash do lexema e vai direto na posição: não percorre
# a tabela. É o que o scanner usa para decidir se uma palavra é reservada
# (já está aqui desde o iniciar) ou um id novo (não está).
def busca(lexema):
    return tabela.get(lexema)


# Troca o Token de um lexema que já está na tabela. Devolve True se achou
# e False se não achou, para quem chama saber o que aconteceu.
# Não é usada no analisador léxico: serve para as etapas seguintes, quando
# a declaração "B inteiro;" for preencher o tipo do id B.
def atualiza(token):
    if token.lexema in tabela:
        tabela[token.lexema] = token
        return True
    return False
