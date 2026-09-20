from tokens import Token
import tabela_de_simbolos

fonte = "" # Código mgol
posicao_caracter = 0 # Índice, dentro de fonte, do próximo caracter a ser lido
linha = 1 # Linha que está sendo lida
coluna = 1 # Coluna que está sendo lida

# Variáveis para erros no terminal
linha_comeco_lexema = 1
coluna_comeco_lexema = 1

# Lê o arquivo inteiro para a memória e deixa o scanner pronto para começar.
def abrir_arquivo(caminho):
    global fonte, posicao_caracter, linha, coluna

    # encoding explícito: sem ele o Windows usaria a codificação local
    with open(caminho, "r", encoding="utf-8") as arquivo:
        fonte = arquivo.read()
    posicao_caracter = 0
    linha = 1
    coluna = 1


# Avança o caracter para a leitura do arquivo fonte 
def avancar_caracter():
    global posicao_caracter, linha, coluna

    if posicao_caracter >= len(fonte): # Fim do arquivo
        return ""

    c = fonte[posicao_caracter]
    posicao_caracter += 1

    if c == "\n":
        linha += 1
        coluna = 1
    else:
        coluna += 1

    return c


# Avança sem consumir para reconhecimentos de, por exemplo, OPR e RCB
def avancar_sem_consumir():
    global posicao_caracter, linha, coluna

    if posicao_caracter >= len(fonte):
        return ""

    c = fonte[posicao_caracter]

    return c


# Reconhecedores de letras 
def letra(c): # Letras
    pass


def digito(c): # Números
    pass

def especial(c): # " ", "\t" e "\n"
    pass


# Um caracter que pode estar DENTRO de um identificador: L, D ou _
def parte_de_identificador(c):
    return letra(c) or digito(c) or c == "_"


# Scanner com a lógica de leitura
def scanner():
    global linha_comeco_lexema, coluna_comeco_lexema

    estado = 0
    lexema = ""
    linha_comeco_lexema = linha
    coluna_comeco_lexema = coluna

    while True:
        c = avancar_sem_consumir()   # olha o caracter de agora, sem consumir
        
        if estado == 0:
            if c == "":                       # estado 6: fim do arquivo (Problema 1)
                return Token("EOF", "EOF", None)

            if especial(c):                   # estado 28: branco, ignora
                avancar_caracter()
                linha_comeco_lexema = linha   # o lexema ainda não começou:
                coluna_comeco_lexema = coluna # tira a foto de novo
                continue

            if c == "{":                      # vai para o estado 4
                avancar_caracter()            # a chave não entra no lexema
                estado = 4
                continue

            if c == '"':                      # vai para o estado 1
                lexema += avancar_caracter()
                estado = 1
                continue

            if letra(c):                      # vai para o estado 3
                lexema += avancar_caracter()
                estado = 3
                continue

            if digito(c):                     # vai para o estado 22
                lexema += avancar_caracter()
                estado = 22
                continue

            if c == "<":                      # vai para o estado 7
                lexema += avancar_caracter()
                estado = 7
                continue

            if c == ">":                      # vai para o estado 9
                lexema += avancar_caracter()
                estado = 9
                continue

            if c == "=":                      # estado 8: final, um caracter só
                lexema += avancar_caracter()
                return Token("OPR", lexema, None)

            if c in ("+", "-", "*", "/"):     # estados 14 a 17
                lexema += avancar_caracter()
                return Token("OPM", lexema, None)

            if c == "(":                      # estado 18
                lexema += avancar_caracter()
                return Token("AB_P", lexema, None)

            if c == ")":                      # estado 19
                lexema += avancar_caracter()
                return Token("FC_P", lexema, None)

            if c == ";":                      # estado 20
                lexema += avancar_caracter()
                return Token("PT_V", lexema, None)

            if c == ",":                      # estado 21
                lexema += avancar_caracter()
                return Token("Vir", lexema, None)

            # nenhuma seta sai do estado 0 com esse caracter
            avancar_caracter()                # consome para não travar
            return Token("ERRO", "1", None)

        # ---------- estado 1: dentro do literal ----------
        elif estado == 1:
            if c == "":                       # acabou o arquivo sem fechar
                return Token("ERRO", "2", None)

            lexema += avancar_caracter()      # engole qualquer caracter

            if c == '"':                      # estado 2: final
                return Token("Lit", lexema, "literal")
            # se não era aspas, continua no estado 1

        # ---------- estado 3: identificador ----------
        elif estado == 3:
            if parte_de_identificador(c):
                lexema += avancar_caracter()
                continue

            # faca-ate: o AFD de id não forma o hífen, trata-se aqui
            if (lexema == "faca"
                    and fonte[posicao_caracter:posicao_caracter + 4] == "-ate"
                    and not parte_de_identificador(
                        fonte[posicao_caracter + 4:posicao_caracter + 5])):
                for _ in range(4):
                    lexema += avancar_caracter()

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
                return Token("ERRO", "3", None)

            avancar_caracter()                # comentário não vira lexema

            if c == "}":                      # estado 5: reconhecido e ignorado
                estado = 0                    # volta ao início e procura de novo
                lexema = ""
                linha_comeco_lexema = linha
                coluna_comeco_lexema = coluna
            # se não era }, continua no estado 4

        # ---------- estado 7: já leu '<' ----------
        elif estado == 7:
            if c == "=":                      # estado 11
                lexema += avancar_caracter()
                return Token("OPR", lexema, None)
            if c == ">":                      # estado 12
                lexema += avancar_caracter()
                return Token("OPR", lexema, None)
            if c == "-":                      # estado 13
                lexema += avancar_caracter()
                return Token("RCB", lexema, None)
            return Token("OPR", lexema, None) # o 7 também é final: '<' sozinho

        # ---------- estado 9: já leu '>' ----------
        elif estado == 9:
            if c == "=":                      # estado 10
                lexema += avancar_caracter()
            return Token("OPR", lexema, None)

        # ---------- estado 22: parte inteira do número ----------
        elif estado == 22:
            if digito(c):
                lexema += avancar_caracter()
                continue
            if c == ".":
                lexema += avancar_caracter()
                estado = 23
                continue
            if c in ("e", "E"):
                lexema += avancar_caracter()
                estado = 25
                continue
            return Token("Num", lexema, "inteiro")   # 22 é final

        # ---------- estado 23: leu o ponto, precisa de dígito ----------
        elif estado == 23:
            if digito(c):
                lexema += avancar_caracter()
                estado = 24
                continue
            return Token("ERRO", "4", None)          # 23 NÃO é final

        # ---------- estado 24: parte decimal ----------
        elif estado == 24:
            if digito(c):
                lexema += avancar_caracter()
                continue
            if c in ("e", "E"):
                lexema += avancar_caracter()
                estado = 25
                continue
            return Token("Num", lexema, "real")      # 24 é final

        # ---------- estado 25: leu o 'e' do expoente ----------
        elif estado == 25:
            if c in ("+", "-"):
                lexema += avancar_caracter()
                estado = 26
                continue
            if digito(c):
                lexema += avancar_caracter()
                estado = 27
                continue
            return Token("ERRO", "5", None)          # 25 NÃO é final

        # ---------- estado 26: leu o sinal do expoente ----------
        elif estado == 26:
            if digito(c):
                lexema += avancar_caracter()
                estado = 27
                continue
            return Token("ERRO", "5", None)          # 26 NÃO é final

        # ---------- estado 27: dígitos do expoente ----------
        elif estado == 27:
            if digito(c):
                lexema += avancar_caracter()
                continue
            return Token("Num", lexema, "real")      # 27 é final