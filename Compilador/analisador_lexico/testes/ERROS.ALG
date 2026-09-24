{ Teste dos erros lexicos do MGOL.
  Cada trecho provoca um erro de proposito e o comentario diz qual.
  O ERRO2 (literal sem fechar) e o ERRO4 sem fechamento NAO estao aqui:
  os dois so disparam no fim do arquivo, entao tem arquivo proprio. }
inicio
    varinicio
        A literal;
        B inteiro;
        C real;
    varfim;

    { ERRO1 - caracteres fora do alfabeto }
    B <- 1 @ 2;
    B <- 1 # 2;

    { ERRO3 - identificador comecando por _ }
    _total <- 10;

    { ERRO4 - fecha comentario sem abrir }
    }

    { ERRO5 - real sem digito depois do ponto }
    C <- 5.;

    { ERRO6 - notacao cientifica incompleta }
    C <- 5e;
    C <- 7E+;

    { ERRO7 - numero colado em identificador }
    B <- 123abc;
    C <- 1.5xy;
    C <- 5e3zz;

    { ERRO8 - simbolos do alfabeto que nao iniciam nenhum token }
    B <- 1 ! 2;
    B <- 1 ? 2;
    B <- 1 : 2;
    B <- 1 \ 2;
    B <- [ 1 ];
    A <- 'x';

    { ERRO9 - ponto fora de numero }
    C <- .5;
fim
