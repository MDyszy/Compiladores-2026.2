class Token:
    def __init__(self, classe, lexema, tipo):
        self.classe = classe
        self.lexema = lexema
        self.tipo = tipo

    # Formato da Figura 1 do enunciado. O PDF escreve "Nulo" onde o tipo não
    # se aplica; no Python esse campo é None.
    def __str__(self):
        if self.tipo is not None:
            tipo = self.tipo
        else:
            tipo = "Nulo"

        return f"Classe: {self.classe}, Lexema: {self.lexema}, Tipo: {tipo}"