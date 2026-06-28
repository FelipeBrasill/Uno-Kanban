class Usuario:
    def __init__(self, id_usuario: int, nome: str, email: str, senha_hash: str):
        self.id = id_usuario
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash  
        self.pontuacao_total = 0     
        