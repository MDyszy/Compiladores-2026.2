import scanner
import tabela_de_simbolos

CAMINHO_DO_FONTE = "testes/COMPLETO.ALG"


# Programa principal: prepara a tabela, abre o fonte e pede um token por vez
# ao scanner até chegar no EOF.
def principal():
    tabela_de_simbolos.iniciar()          # reservadas antes de começar a análise
    scanner.abrir_arquivo(CAMINHO_DO_FONTE)

    while True:
        token = scanner.scanner()
        print(token)

        if token.classe == "EOF":
            break


if __name__ == "__main__":
    principal()
