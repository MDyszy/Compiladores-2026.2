# Teste end-to-end do analisador léxico do MGOL.
#
# Roda o scanner sobre todos os fontes de testes/ e confere, para cada um:
#   - a análise termina, ou seja, nenhum caminho de erro entrou em laço;
#   - os códigos de erro que aparecem são exatamente os esperados;
#   - nos fontes sem erro, colar todos os lexemas reproduz o fonte sem
#     brancos e sem comentários (nada foi perdido nem inventado).
#
# No fim, confere a cobertura: as classes da Tabela 1, as 14 reservadas da
# Tabela 2 e os 11 códigos de erro precisam ter sido todos exercitados.
#
# Uso: python teste_end_to_end.py

import scanner
import tabela_de_simbolos

LIMITE_DE_TOKENS = 1000          # passou disso, o scanner está em laço

ERROS_ESPERADOS = {
    "testes/COMPLETO.ALG": set(),
    "testes/FONTE.ALG": {"ERRO1"},          # o á da linha 35
    "testes/ERROS.ALG": {"ERRO1", "ERRO3", "ERRO4", "ERRO6",
                         "ERRO7", "ERRO8", "ERRO9", "ERRO10", "ERRO11"},
    "testes/ERRO_LITERAL.ALG": {"ERRO2"},
    "testes/ERRO_COMENTARIO.ALG": {"ERRO5"},
}

CLASSES_DA_TABELA_1 = ["Num", "Lit", "id", "EOF", "OPR", "RCB",
                       "OPM", "AB_P", "FC_P", "PT_V", "Vir"]

RESERVADAS = ["inicio", "varinicio", "varfim", "escreva", "leia", "se",
              "entao", "fimse", "faca-ate", "fimfaca", "fim", "inteiro",
              "literal", "real"]


# Roda o scanner do começo ao fim e devolve a lista de tokens. O limite existe
# para o teste acusar um laço em vez de travar junto com o scanner.
def analisar(caminho):
    tabela_de_simbolos.tabela.clear()
    tabela_de_simbolos.iniciar()

    entrada = scanner.abrir_arquivo(caminho)
    if entrada is None:
        return None

    tokens = []
    while len(tokens) < LIMITE_DE_TOKENS:
        token = scanner.scanner(entrada)
        tokens.append(token)
        if token.classe == "EOF":
            return tokens
    return None                  # estourou o limite: laço


# Devolve o fonte sem comentários e sem os brancos que ficam FORA de literais.
# É com isto que a concatenação dos lexemas tem de bater.
def limpar(texto):
    limpo = []
    dentro_de_literal = False
    dentro_de_comentario = False

    for c in texto:
        if dentro_de_comentario:
            if c == "}":
                dentro_de_comentario = False
        elif dentro_de_literal:
            limpo.append(c)
            if c == '"':
                dentro_de_literal = False
        elif c == "{":
            dentro_de_comentario = True
        elif c == '"':
            dentro_de_literal = True
            limpo.append(c)
        elif c not in (" ", "\t", "\n"):
            limpo.append(c)

    return "".join(limpo)


def principal():
    falhas = []
    classes_vistas = set()
    reservadas_vistas = set()
    erros_vistos = set()

    for caminho, esperados in ERROS_ESPERADOS.items():
        tokens = analisar(caminho)

        if tokens is None:
            print(f"FALHOU  {caminho}: não terminou (laço) ou não abriu")
            falhas.append(caminho)
            continue

        obtidos = {t.classe for t in tokens if t.classe.startswith("ERRO")}
        classes_vistas.update(t.classe for t in tokens)
        reservadas_vistas.update(t.lexema for t in tokens
                                 if t.lexema in RESERVADAS)
        erros_vistos.update(obtidos)

        if obtidos != esperados:
            print(f"FALHOU  {caminho}")
            print(f"        esperava {sorted(esperados)}")
            print(f"        obteve   {sorted(obtidos)}")
            falhas.append(caminho)
            continue

        # nos fontes sem erro, nenhum caracter pode ter sido perdido ou criado
        detalhe = ""
        if not esperados:
            with open(caminho, encoding="utf-8-sig") as arquivo:
                limpo = limpar(arquivo.read())
            colado = "".join(t.lexema for t in tokens if t.classe != "EOF")
            if limpo != colado:
                print(f"FALHOU  {caminho}: os lexemas não reproduzem o fonte")
                falhas.append(caminho)
                continue
            detalhe = f", {len(colado)} caracteres reconstruídos"

        print(f"ok      {caminho}: {len(tokens)} tokens, "
              f"erros {sorted(obtidos) if obtidos else '(nenhum)'}{detalhe}")

    # ---------- cobertura ----------
    print()
    faltando_classes = [c for c in CLASSES_DA_TABELA_1 if c not in classes_vistas]
    faltando_reservadas = [r for r in RESERVADAS if r not in reservadas_vistas]
    faltando_erros = [e for e in scanner.MENSAGENS_DE_ERRO if e not in erros_vistos]

    for nome, faltando in (("classes da Tabela 1", faltando_classes),
                           ("reservadas da Tabela 2", faltando_reservadas),
                           ("códigos de erro", faltando_erros)):
        if faltando:
            print(f"FALHOU  {nome} nunca exercitadas: {faltando}")
            falhas.append(nome)
        else:
            print(f"ok      {nome}: todas exercitadas")

    print()
    if falhas:
        print(f"{len(falhas)} FALHA(S)")
    else:
        print("TODOS OS TESTES PASSARAM")


if __name__ == "__main__":
    principal()
