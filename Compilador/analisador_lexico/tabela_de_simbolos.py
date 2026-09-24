from tokens import Token

tabela_de_simbolos = ["inicio", "varinicio", "varfim",
                    "escreva", "leia", "se", "entao",
                    "fimse", "faca-ate", "fimfaca",
                    "fim", "inteiro", "literal", "real"]

tabela = {}

def iniciar():
    for palavra in tabela_de_simbolos:
        inserir(Token(palavra, palavra, palavra))

def inserir(token):
    tabela[token.lexema] = token

def busca(lexema):
    return tabela.get(lexema)

def atualiza(token):
    if token.lexema in tabela:
        tabela[token.lexema] = token
        return True
    return False

def imprimir():
    print()
    print("Tabela de símbolos")
    for token in tabela.values():
        tipo = token.tipo if token.tipo is not None else "Nulo"
        print(f"{token.classe}, {token.lexema}, {tipo}")
