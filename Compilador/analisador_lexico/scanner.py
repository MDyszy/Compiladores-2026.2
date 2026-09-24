from tokens import Token
import tabela_de_simbolos

class Entrada:
    def __init__(self, texto):
        self.fonte = texto                
        self.posicao_caracter = 0         
        self.linha = 1                    
        self.coluna = 1                   

        self.linha_comeco_lexema = 1
        self.coluna_comeco_lexema = 1

def abrir_arquivo(caminho):
    try:
        with open(caminho, "r", encoding="utf-8-sig", errors="replace") as arquivo:
            return Entrada(arquivo.read())
    except OSError as falha:
        print(f"Não foi possível abrir o arquivo fonte: {falha}")
        return None

def avancar_caracter(entrada):
    if entrada.posicao_caracter >= len(entrada.fonte):
        return ""

    c = entrada.fonte[entrada.posicao_caracter]
    entrada.posicao_caracter += 1

    if c == "\n":
        entrada.linha += 1
        entrada.coluna = 1
    else:
        entrada.coluna += 1

    return c

def avancar_sem_consumir(entrada):
    if entrada.posicao_caracter >= len(entrada.fonte):
        return ""

    return entrada.fonte[entrada.posicao_caracter]

def letra(c): 
    return "A" <= c <= "Z" or "a" <= c <= "z"

def digito(c): 
    return "0" <= c <= "9"

def parte_de_identificador(c):
    return letra(c) or digito(c) or c == "_"

TRANSICOES = {
    0:  {"LETRA": 3, "DIGITO": 22, '"': 1, "{": 4,
         "<": 7, ">": 9, "=": 8,
         "+": 14, "-": 15, "*": 16, "/": 17,
         "(": 18, ")": 19, ";": 20, ",": 21,
         " ": 28, "\t": 29, "\n": 30,
         "}": 35, "_": 32, ".": 34,
         ":": 33, "!": 33, "?": 33, "\\": 33, "[": 33, "]": 33, "'": 33},

    1:  {'"': 2, "QUALQUER": 1},              
    3:  {"LETRA": 3, "DIGITO": 3, "_": 3},      
    4:  {"}": 5, "QUALQUER": 4},             

    7:  {"=": 11, ">": 12, "-": 13},   
    9:  {"=": 10},                     

    22: {"DIGITO": 22, ".": 23, "e": 25, "E": 25, "LETRA": 31, "_": 31},
    23: {"DIGITO": 24},
    24: {"DIGITO": 24, "e": 25, "E": 25, "LETRA": 31, "_": 31},
    25: {"DIGITO": 27, "+": 26, "-": 26},
    26: {"DIGITO": 27},
    27: {"DIGITO": 27, "LETRA": 31, "_": 31},
}

FINAIS = {
    2: "Lit", 3: "id",
    7: "OPR", 8: "OPR", 9: "OPR", 10: "OPR", 11: "OPR", 12: "OPR",
    13: "RCB",
    14: "OPM", 15: "OPM", 16: "OPM", 17: "OPM",
    18: "AB_P", 19: "FC_P", 20: "PT_V", 21: "Vir",
    22: "Num", 24: "Num", 27: "Num",
}

TIPOS = {2: "literal", 22: "inteiro", 24: "real", 27: "real"}

ERROS_DE_ESTADO = {
    1: "ERRO2",     
    4: "ERRO4",     
    23: "ERRO5",    
    25: "ERRO6",    
    26: "ERRO6",    
    31: "ERRO7",    
    32: "ERRO3",    
    33: "ERRO8",    
    34: "ERRO9",    
    35: "ERRO4",    
}

ESTADOS_QUE_ENGOLEM = {23, 25, 26, 31, 32}

ESTADOS_SEM_LEXEMA = {4, 5, 28, 29, 30}

ESTADOS_QUE_REINICIAM = {5, 28, 29, 30}

MENSAGENS_DE_ERRO = {
    "ERRO1": "Caractere inválido na linguagem",
    "ERRO2": "Constante literal não fechada, verifique as aspas de abertura e de fechamento",
    "ERRO3": "Identificador em formato inválido, deve começar por letra",
    "ERRO4": "Comentário mal formado, verifique a abertura { e o fechamento }",
    "ERRO5": "Número real em formato inválido, depois do ponto é preciso ao menos um dígito (ex.: 5.0)",
    "ERRO6": "Notação científica em formato inválido, o expoente precisa de dígitos (ex.: 5e3, 2.5e-3, 7E+2)",
    "ERRO7": "Número colado em identificador, separe os dois",
    "ERRO8": "Símbolo do alfabeto que não inicia nenhum token",
    "ERRO9": "Ponto fora de número, todo número começa por dígito (ex.: 0.5)",
}

def erro(token, entrada):
    mensagem = MENSAGENS_DE_ERRO.get(token.classe, "Erro léxico desconhecido")

    print(f"{token.classe} - {mensagem}, "
          f"linha {entrada.linha_comeco_lexema}, "
          f"coluna {entrada.coluna_comeco_lexema}: {token.lexema}")

def engolir_identificador(entrada, lexema):
    while parte_de_identificador(avancar_sem_consumir(entrada)):
        lexema += avancar_caracter(entrada)
    return lexema

def transicao(estado, c):
    linha = TRANSICOES.get(estado, {})

    if c in linha:                        
        return linha[c]

    if letra(c) and "LETRA" in linha:         
        return linha["LETRA"]

    if digito(c) and "DIGITO" in linha:        
        return linha["DIGITO"]

    return linha.get("QUALQUER")                 

def scanner(entrada):
    estado = 0
    lexema = ""
    entrada.linha_comeco_lexema = entrada.linha
    entrada.coluna_comeco_lexema = entrada.coluna

    while True:
        c = avancar_sem_consumir(entrada)  

        if estado == 0 and c == "":
            return Token("EOF", "EOF", None)

        proximo = None if c == "" else transicao(estado, c)

        if proximo is not None:
            if proximo in ESTADOS_SEM_LEXEMA:
                avancar_caracter(entrada)        
            else:
                lexema += avancar_caracter(entrada)

            if proximo in ESTADOS_QUE_REINICIAM:   
                estado = 0
                lexema = ""
                entrada.linha_comeco_lexema = entrada.linha
                entrada.coluna_comeco_lexema = entrada.coluna
            else:
                estado = proximo
            continue

        if estado in FINAIS:
            classe = FINAIS[estado]

            if classe == "id":
                proximos = entrada.fonte[entrada.posicao_caracter:
                                         entrada.posicao_caracter + 4]
                depois = entrada.fonte[entrada.posicao_caracter + 4:
                                       entrada.posicao_caracter + 5]
                if (lexema == "faca"
                        and proximos == "-ate"
                        and not parte_de_identificador(depois)):
                    for _ in range(4):
                        lexema += avancar_caracter(entrada)

                achado = tabela_de_simbolos.busca(lexema)
                if achado is not None:      
                    return achado

                novo = Token("id", lexema, None)
                tabela_de_simbolos.inserir(novo)
                return novo

            return Token(classe, lexema, TIPOS.get(estado))

        if estado == 0:                     
            lexema += avancar_caracter(entrada)   
            return Token("ERRO1", lexema, None)

        if estado in ESTADOS_QUE_ENGOLEM:
            lexema = engolir_identificador(entrada, lexema)

        if estado == 4:                     
            lexema = "{"

        return Token(ERROS_DE_ESTADO[estado], lexema, None)
