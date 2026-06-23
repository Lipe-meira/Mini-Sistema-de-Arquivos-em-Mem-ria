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

    #pwd mostra o caminho completo da pasta atual
    def pwd(self):
        self.caminho = []
        no = self.atual
        while no is not None:
            self.caminho.append(no.nome)
            no = no.pai
        self.caminho.reverse()
        # junta os itens de um array em um string
        return("/".join(self.caminho)) 

    #ls lista os arquivos e diretorios da pasta atual
    def ls(self):
        for nome in self.atual.filhos:
            if self.atual.filhos[nome].tipo == "diretorio":
                print("[DIR] " + nome)
            else:
                print("[ARQ] " + nome)    

fs = SistemaArquivos()

# cria um diretório filho manualmente
pasta = No("documentos", "diretorio")
pasta.pai = fs.root
fs.root.filhos["documentos"] = pasta

# cria um arquivo filho manualmente
arq = No("notas.txt", "arquivo")
arq.pai = fs.root
fs.root.filhos["notas.txt"] = arq

fs.ls()  # deve mostrar algo como:
         # [DIR] documentos
         # [ARQ] notas.txt
