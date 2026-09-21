{ Programa de teste do analisador lexico do MGOL.
  Cobre todos os tokens da Tabela 1 e as 14 reservadas da Tabela 2.
  Este comentario tem varias linhas de proposito. }
inicio
    varinicio
        A literal;
        B inteiro;
        C real;
        D_1, Valor_Total3 inteiro;
        E2 real;
    varfim;

    { constantes: inteiro, real com ponto e real com expoente }
    B <- 10;
    C <- 3.14;
    C <- 1e5;
    C <- 2.5e-3;
    C <- 7E+2;
    A <- "constante literal";

    { operadores aritmeticos e parenteses }
    B <- B + 1;
    B <- B - 2;
    B <- B * 3;
    B <- B / 4;
    B <- (B + 1) * (B - 1);

    { os seis operadores relacionais }
    se (B > 5) entao
        escreva "maior";
    fimse
    se (B < 5) entao
        escreva "menor";
    fimse
    se (B >= 5) entao
        escreva "maior ou igual";
    fimse
    se (B <= 5) entao
        escreva "menor ou igual";
    fimse
    se (B = 5) entao
        escreva "igual";
    fimse
    se (B <> 5) entao
        escreva "diferente";
    fimse

    { repeticao }
    faca-ate (B > 100)
        B <- B + 10;
    fimfaca

    leia A;
    leia D_1;
    escreva C;
    escreva E2;
    escreva Valor_Total3;
fim
