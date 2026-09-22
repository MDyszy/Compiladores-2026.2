from tokens import Token
import tabela_de_simbolos

# Estado da leitura do fonte. É este objeto que o SCANNER recebe como
# parâmetro de entrada, no lugar das variáveis globais que existiam antes:
# assim a função não depende de nada de fora e dois fontes podem ser
# analisados ao mesmo tempo, cada um com a sua Entrada.
class Entrada:
    def __init__(self, texto):
        self.fonte = texto                # Código mgol
        self.posicao_caracter = 0         # Índice do próximo caracter a ler
        self.linha = 1                    # Linha que está sendo lida
        self.coluna = 1                   # Coluna que está sendo lida

        # Onde o lexema atual começou, para as mensagens de erro
        self.linha_comeco_lexema = 1
        self.coluna_comeco_lexema = 1

# Lê o arquivo inteiro para a memória e devolve uma Entrada pronta para o
# scanner. Devolve None se não conseguir abrir, para o principal decidir.
def abrir_arquivo(caminho):
    # encoding explícito: sem ele o Windows usaria a codificação local.
    # "utf-8-sig" descarta o BOM que o Bloco de Notas põe no começo do arquivo,
    # e errors="replace" troca byte inválido (arquivo salvo em ANSI) por um
    # caracter de substituição, que o scanner acusa como ERRO1 na posição
    # certa. Assim a análise nunca morre no meio por causa da codificação.
    try:
        with open(caminho, "r", encoding="utf-8-sig", errors="replace") as arquivo:
            return Entrada(arquivo.read())
    except OSError as falha:
        print(f"Não foi possível abrir o arquivo fonte: {falha}")
        return None

# Avança o caracter para a leitura do arquivo fonte
def avancar_caracter(entrada):
    if entrada.posicao_caracter >= len(entrada.fonte): # Fim do arquivo
        return ""

    c = entrada.fonte[entrada.posicao_caracter]
    entrada.posicao_caracter += 1

    if c == "\n":
        entrada.linha += 1
        entrada.coluna = 1
    else:
        entrada.coluna += 1

    return c

# Avança sem consumir para reconhecimentos de, por exemplo, OPR e RCB
def avancar_sem_consumir(entrada):
    if entrada.posicao_caracter >= len(entrada.fonte):
        return ""

    return entrada.fonte[entrada.posicao_caracter]

# Reconhecedores de letras
def letra(c): # Letras
    return "A" <= c <= "Z" or "a" <= c <= "z"

def digito(c): # Números
    return "0" <= c <= "9"

def especial(c): # " ", "\t" e "\n"
    return c in (" ", "\t", "\n")

# Um caracter que pode estar DENTRO de um identificador: L, D ou _
def parte_de_identificador(c):
    return letra(c) or digito(c) or c == "_"

# Mensagem de cada erro léxico. A chave é a classe do token, no formato da
# Figura 1 do enunciado: "Classe: ERRO1, Lexema: @, Tipo: Nulo".
MENSAGENS_DE_ERRO = {
    "ERRO1": "Caractere inválido na linguagem",
    "ERRO2": "Constante literal não fechada, verifique as aspas de abertura e de fechamento",
    "ERRO3": "Identificador em formato inválido, deve começar por letra",
    "ERRO4": "Comentário sem abertura {",
    "ERRO5": "Comentário sem fechamento }",
    "ERRO6": "Número real em formato inválido, depois do ponto é preciso ao menos um dígito (ex.: 5.0)",
    "ERRO7": "Notação científica em formato inválido, o expoente precisa de dígitos (ex.: 5e3, 2.5e-3, 7E+2)",
    "ERRO8": "Número colado em identificador, separe os dois",
    "ERRO9": "Símbolo do alfabeto sem uso na linguagem",
    "ERRO10": "Ponto fora de número, todo número começa por dígito (ex.: 0.5)",
    "ERRO11": "Abertura de comentário dentro de comentário, o comentário fecha no primeiro }",
}

# Recebe o TOKEN ERRO e mostra na tela a mensagem, a linha e a coluna em que
# o lexema começou. Quem chama é o programa principal.
def erro(token, entrada):
    mensagem = MENSAGENS_DE_ERRO.get(token.classe, "Erro léxico desconhecido")
    print(f"{token.classe} – {mensagem}, "
          f"linha {entrada.linha_comeco_lexema}, "
          f"coluna {entrada.coluna_comeco_lexema}")

# Consome letras, dígitos e _ enquanto houver, acrescentando ao lexema. Os
# estados de erro usam isto para engolir o lexema inteiro: assim a mensagem
# mostra "123abc" em vez de acusar um caracter e deixar o resto virar tokens
# soltos (o erro em cascata).
def engolir_identificador(entrada, lexema):
    while parte_de_identificador(avancar_sem_consumir(entrada)):
        lexema += avancar_caracter(entrada)
    return lexema

# Igual à de cima, mas engole também o ponto: um número malformado como
# "5..3" sai num erro só, em vez de virar três eventos na tela.
def engolir_resto_do_numero(entrada, lexema):
    while (parte_de_identificador(avancar_sem_consumir(entrada))
           or avancar_sem_consumir(entrada) == "."):
        lexema += avancar_caracter(entrada)
    return lexema

# Scanner com a lógica de leitura. Recebe a Entrada e devolve UM token por
# chamada, como pede o enunciado: token SCANNER(parâmetros de entrada).
def scanner(entrada):
    estado = 0
    lexema = ""
    aninhado = False                      # viu um '{' dentro do comentário
    entrada.linha_comeco_lexema = entrada.linha
    entrada.coluna_comeco_lexema = entrada.coluna

    while True:
        c = avancar_sem_consumir(entrada)  # olha o caracter de agora, sem consumir

        if estado == 0:
            # o '$' do AFD denota o fim da entrada; aceito os dois, o caracter
            # e o fim físico do arquivo
            if c == "" or c == "$":           # estado 6: fim do arquivo (Problema 1)
                return Token("EOF", "EOF", None)

            if especial(c):                   # estado 28: branco, ignora
                avancar_caracter(entrada)
                # o lexema ainda não começou: tira a foto de novo
                entrada.linha_comeco_lexema = entrada.linha
                entrada.coluna_comeco_lexema = entrada.coluna
                continue

            if c == "{":                      # vai para o estado 4
                avancar_caracter(entrada)     # a chave não entra no lexema
                estado = 4
                continue

            if c == '"':                      # vai para o estado 1
                lexema += avancar_caracter(entrada)
                estado = 1
                continue

            if letra(c):                      # vai para o estado 3
                lexema += avancar_caracter(entrada)
                estado = 3
                continue

            if digito(c):                     # vai para o estado 22
                lexema += avancar_caracter(entrada)
                estado = 22
                continue

            if c == "<":                      # vai para o estado 7
                lexema += avancar_caracter(entrada)
                estado = 7
                continue

            if c == ">":                      # vai para o estado 9
                lexema += avancar_caracter(entrada)
                estado = 9
                continue

            if c == "=":                      # estado 8: final, um caracter só
                lexema += avancar_caracter(entrada)
                return Token("OPR", lexema, None)

            if c in ("+", "-", "*", "/"):     # estados 14 a 17
                lexema += avancar_caracter(entrada)
                return Token("OPM", lexema, None)

            if c == "(":                      # estado 18
                lexema += avancar_caracter(entrada)
                return Token("AB_P", lexema, None)

            if c == ")":                      # estado 19
                lexema += avancar_caracter(entrada)
                return Token("FC_P", lexema, None)

            if c == ";":                      # estado 20
                lexema += avancar_caracter(entrada)
                return Token("PT_V", lexema, None)

            if c == ",":                      # estado 21
                lexema += avancar_caracter(entrada)
                return Token("Vir", lexema, None)

            if c == "}":                      # fecha comentário sem abrir
                lexema += avancar_caracter(entrada)
                return Token("ERRO4", lexema, None)

            if c == "_":                      # id tem de começar por letra
                lexema += avancar_caracter(entrada)
                lexema = engolir_identificador(entrada, lexema)
                return Token("ERRO3", lexema, None)

            # do alfabeto do MGOL, mas não começam token nenhum
            if c in (":", "!", "?", "\\", "[", "]", "'"):
                lexema += avancar_caracter(entrada)
                return Token("ERRO9", lexema, None)

            if c == ".":                      # o ponto só existe dentro de Num
                lexema += avancar_caracter(entrada)
                return Token("ERRO10", lexema, None)

            # nenhuma seta sai do estado 0 com esse caracter
            lexema += avancar_caracter(entrada)   # consome para não travar
            return Token("ERRO1", lexema, None)

        # ---------- estado 1: dentro do literal ----------
        elif estado == 1:
            # o literal não atravessa linha: assim uma aspa esquecida engole
            # no máximo o resto da linha, e não o resto do programa
            if c == "" or c == "\n":          # acabou a linha ou o arquivo
                return Token("ERRO2", lexema, None)

            lexema += avancar_caracter(entrada)   # engole qualquer caracter

            if c == '"':                      # estado 2: final
                return Token("Lit", lexema, "literal")
            # se não era aspas, continua no estado 1

        # ---------- estado 3: identificador ----------
        elif estado == 3:
            if parte_de_identificador(c):
                lexema += avancar_caracter(entrada)
                continue

            # faca-ate: o AFD de id não forma o hífen, trata-se aqui
            proximos = entrada.fonte[entrada.posicao_caracter:
                                     entrada.posicao_caracter + 4]
            depois = entrada.fonte[entrada.posicao_caracter + 4:
                                   entrada.posicao_caracter + 5]
            if (lexema == "faca"
                    and proximos == "-ate"
                    and not parte_de_identificador(depois)):
                for _ in range(4):
                    lexema += avancar_caracter(entrada)

            # o identificador acabou: consulta a tabela de símbolos
            achado = tabela_de_simbolos.busca(lexema)
            if achado is not None:            # reservada ou id já visto
                return achado

            novo = Token("id", lexema, None)
            tabela_de_simbolos.inserir(novo)
            return novo

        # ---------- estado 4: dentro do comentário ----------
        elif estado == 4:
            if c == "":                       # acabou o arquivo sem fechar
                return Token("ERRO5", "{", None)

            if c == "{":                      # o AFD não conta níveis
                aninhado = True

            avancar_caracter(entrada)         # comentário não vira lexema

            if c == "}":                      # estado 5: reconhecido e ignorado
                if aninhado:                  # acusa só depois de fechar, para
                    return Token("ERRO11", "{", None)   # não espalhar lixo
                estado = 0                    # volta ao início e procura de novo
                lexema = ""
                entrada.linha_comeco_lexema = entrada.linha
                entrada.coluna_comeco_lexema = entrada.coluna
            # se não era }, continua no estado 4

        # ---------- estado 7: já leu '<' ----------
        elif estado == 7:
            if c == "=":                      # estado 11
                lexema += avancar_caracter(entrada)
                return Token("OPR", lexema, None)
            if c == ">":                      # estado 12
                lexema += avancar_caracter(entrada)
                return Token("OPR", lexema, None)
            if c == "-":                      # estado 13
                lexema += avancar_caracter(entrada)
                return Token("RCB", lexema, None)
            return Token("OPR", lexema, None) # o 7 também é final: '<' sozinho

        # ---------- estado 9: já leu '>' ----------
        elif estado == 9:
            if c == "=":                      # estado 10
                lexema += avancar_caracter(entrada)
            return Token("OPR", lexema, None)

        # ---------- estado 22: parte inteira do número ----------
        elif estado == 22:
            if digito(c):
                lexema += avancar_caracter(entrada)
                continue
            if c == ".":
                lexema += avancar_caracter(entrada)
                estado = 23
                continue
            if c in ("e", "E"):
                lexema += avancar_caracter(entrada)
                estado = 25
                continue
            if letra(c) or c == "_":                 # 123abc: lexemas colados
                lexema = engolir_identificador(entrada, lexema)
                return Token("ERRO8", lexema, None)
            return Token("Num", lexema, "inteiro")   # 22 é final

        # ---------- estado 23: leu o ponto, precisa de dígito ----------
        elif estado == 23:
            if digito(c):
                lexema += avancar_caracter(entrada)
                estado = 24
                continue
            lexema = engolir_resto_do_numero(entrada, lexema)
            return Token("ERRO6", lexema, None)      # 23 NÃO é final

        # ---------- estado 24: parte decimal ----------
        elif estado == 24:
            if digito(c):
                lexema += avancar_caracter(entrada)
                continue
            if c in ("e", "E"):
                lexema += avancar_caracter(entrada)
                estado = 25
                continue
            if letra(c) or c == "_":                 # 1.5abc: lexemas colados
                lexema = engolir_identificador(entrada, lexema)
                return Token("ERRO8", lexema, None)
            return Token("Num", lexema, "real")      # 24 é final

        # ---------- estado 25: leu o 'e' do expoente ----------
        elif estado == 25:
            if c in ("+", "-"):
                lexema += avancar_caracter(entrada)
                estado = 26
                continue
            if digito(c):
                lexema += avancar_caracter(entrada)
                estado = 27
                continue
            lexema = engolir_resto_do_numero(entrada, lexema)
            return Token("ERRO7", lexema, None)      # 25 NÃO é final

        # ---------- estado 26: leu o sinal do expoente ----------
        elif estado == 26:
            if digito(c):
                lexema += avancar_caracter(entrada)
                estado = 27
                continue
            lexema = engolir_resto_do_numero(entrada, lexema)
            return Token("ERRO7", lexema, None)      # 26 NÃO é final

        # ---------- estado 27: dígitos do expoente ----------
        elif estado == 27:
            if digito(c):
                lexema += avancar_caracter(entrada)
                continue
            if letra(c) or c == "_":                 # 5e3abc: lexemas colados
                lexema = engolir_identificador(entrada, lexema)
                return Token("ERRO8", lexema, None)
            return Token("Num", lexema, "real")      # 27 é final
