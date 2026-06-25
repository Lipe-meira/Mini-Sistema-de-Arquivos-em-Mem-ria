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

    # pwd mostra o caminho completo da pasta atual
    def pwd(self):
        self.caminho = []
        no = self.atual
        while no is not None:
            self.caminho.append(no.nome)
            no = no.pai
        self.caminho.reverse()

        # join junta os itens de um array em um string
        return "/" + "/".join(self.caminho[1:])

    # ls lista os arquivos e diretorios da pasta atual
    def ls(self):
        for nome in self.atual.filhos:
            if self.atual.filhos[nome].tipo == "diretorio":
                print("[DIR] " + nome)
            else:
                print("[ARQ] " + nome)

    # cria pasta
    def mkdir(self, nome):
        # no linux nao da pra criar uma pasta com msm nome de um arquivo ou de outro DIR.
        if nome in self.atual.filhos:
            print("Erro: Já existe um arquivo ou diretório com esse nome.")
        else:
            self.atual.filhos[nome] = No(nome, "diretorio")
            self.atual.filhos[nome].pai = self.atual

    # cria arquuivo
    def touch(self, nome):
        if nome in self.atual.filhos:
            print("[ERRO]: Já existe um arquivo ou diretório com esse nome.")
        else:
            self.atual.filhos[nome] = No(nome, "arquivo")
            self.atual.filhos[nome].pai = self.atual
    
    # mudar de diretório/pasta.
    def cd(self, nome):
        if nome == "..":
            if self.atual == self.root:
                print("Erro: Já está no diretório raiz.")
            else:
                self.atual = self.atual.pai
        # nome da raiz
        elif nome == "/":
            self.atual = self.root
        elif nome in self.atual.filhos:
            if self.atual.filhos[nome].tipo == "diretorio":
                self.atual = self.atual.filhos[nome]
            else:
                print("Erro: Não é um diretório.")
        else:
            print("Erro: Diretório não encontrado.")

    def echo(self, conteudo, nome):
        if nome in self.atual.filhos and self.atual.filhos[nome].tipo == "arquivo":
            self.atual.filhos[nome].conteudo = conteudo
        
        # cria o arquivo e add conteudo
        else:
            if nome in self.atual.filhos:
                print("[ERRO]: Já existe um arquivo ou diretório com esse nome.")
            else:
                self.atual.filhos[nome] = No(nome, "arquivo")
                self.atual.filhos[nome].pai = self.atual
                self.atual.filhos[nome].conteudo = conteudo

    def cat(self, nome):
        if nome in self.atual.filhos and self.atual.filhos[nome].tipo == "arquivo":
            print(self.atual.filhos[nome].conteudo)
        else:
            print("Erro: Arquivo não encontrado.")

fs = SistemaArquivos()
