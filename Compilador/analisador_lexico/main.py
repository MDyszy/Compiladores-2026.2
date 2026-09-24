import scanner
import tabela_de_simbolos

CAMINHO_DO_FONTE = "testes/FONTE.ALG"

def principal():
    tabela_de_simbolos.iniciar()          
    entrada = scanner.abrir_arquivo(CAMINHO_DO_FONTE)
    if entrada is None:
        return                            

    while True:
        token = scanner.scanner(entrada)
        print(token)                      

        if token.classe.startswith("ERRO"):
            scanner.erro(token, entrada)

        if token.classe == "EOF":
            break

    tabela_de_simbolos.imprimir()


if __name__ == "__main__":
    principal()
