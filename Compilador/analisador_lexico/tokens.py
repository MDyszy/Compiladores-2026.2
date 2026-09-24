class Token:
    def __init__(self, classe, lexema, tipo):
        self.classe = classe
        self.lexema = lexema
        self.tipo = tipo

    def __str__(self):
        if self.tipo is not None:
            tipo = self.tipo
        else:
            tipo = "Nulo"

        return f"Classe: {self.classe}, Lexema: {self.lexema}, Tipo: {tipo}"