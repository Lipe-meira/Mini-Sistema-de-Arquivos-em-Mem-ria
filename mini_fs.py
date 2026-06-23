class No:
    def __init__(self, nome, tipo):
        self.nome = nome
        self.tipo = tipo  # "arquivo" ou "diretorio"
        self.conteudo = ""
        self.filhos = {}
        self.pai = None
        self.permissoes = "rwx"

class SistemaArquivos:
    def __init__(self):
        self.root = No("/", "diretorio")
        self.atual = self.root


fs = SistemaArquivos()
print(fs.root.nome)      
print(fs.root.tipo)       
print(fs.root.filhos)   
print(fs.atual == fs.root) 