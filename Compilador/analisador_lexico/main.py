import scanner
import tabela_de_simbolos

CAMINHO_DO_FONTE = "testes/ERRO_LITERAL.ALG"


# Programa principal: prepara a tabela, abre o fonte e pede um token por vez
# ao scanner até chegar no EOF.
def principal():
    tabela_de_simbolos.iniciar()          # reservadas antes de começar a análise

    entrada = scanner.abrir_arquivo(CAMINHO_DO_FONTE)
    if entrada is None:
        return                            # sem fonte não há o que analisar

    while True:
        token = scanner.scanner(entrada)
        print(token)

        if token.classe.startswith("ERRO"):
            scanner.erro(token, entrada)

        if token.classe == "EOF":
            break


if __name__ == "__main__":
    principal()
