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
                if "x" in self.atual.filhos[nome].permissoes:
                    self.atual = self.atual.filhos[nome]
                else:
                    print("Erro: Sem permissão de entrada.")
            else:
                print("Erro: Não é um diretório.")
        else:
            print("Erro: Diretório não encontrado.")

    # cria o arquivo e add conteudo
    def echo(self, conteudo, nome):
        if nome in self.atual.filhos and self.atual.filhos[nome].tipo == "arquivo":
            if "w" in self.atual.filhos[nome].permissoes:
                self.atual.filhos[nome].conteudo = conteudo
            else:
                print("Erro: Sem permissão de escrita.")
        else:
            if nome in self.atual.filhos:
                print("[ERRO]: Já existe um arquivo ou diretório com esse nome.")
            else:
                self.atual.filhos[nome] = No(nome, "arquivo")
                self.atual.filhos[nome].pai = self.atual
                self.atual.filhos[nome].conteudo = conteudo

    # mostra o conteudo de um arquivo
    def cat(self, nome):
        if nome in self.atual.filhos and self.atual.filhos[nome].tipo == "arquivo":
            if "r" in self.atual.filhos[nome].permissoes:
                print(self.atual.filhos[nome].conteudo)
            else:
                print("Erro: Sem permissão de leitura.")
        else:
            print("Erro: Arquivo não encontrado.")

    # deleta um arquivo
    def rm(self, nome):
        if nome in self.atual.filhos:
            if self.atual.filhos[nome].tipo == "arquivo":
                del self.atual.filhos[nome]
                print("Arquivo removido com sucesso.")
            elif (
                self.atual.filhos[nome].tipo == "diretorio"
                and self.atual.filhos[nome].filhos == {}
            ):
                del self.atual.filhos[nome]
                print("Diretorio removido com sucesso.")
            else:
                print("[ERRO]: Diretório não está vazio.")
        else:
            print("[ERRO]: Arquivo ou diretório não encontrado.")

    def gerar_nome_copia(self, nome):
        # separa nome e extensão
        if "." in nome:
            base, extensao = nome.rsplit(".", 1)
            extensao = "." + extensao
        else:
            base = nome
            extensao = ""

        # se ainda não tem _copia, adiciona
        if base.endswith("_copia"):
            prefixo = base
        else:
            prefixo = base + "_copia"

        novo_nome = prefixo + extensao

        # se arquivo_copia.txt ainda não existe, usa ele
        if novo_nome not in self.atual.filhos:
            return novo_nome

        # se já existe, começa a tentar (1), (2), (3)...
        contador = 1

        while 1 == 1:
            novo_nome = prefixo + "(" + str(contador) + ")" + extensao

            if novo_nome not in self.atual.filhos:
                return novo_nome

            contador += 1

    # copiar, duplicar o arquivo alvo em outro lugar
    def cp(self, nomeArqOrigem, nomeArqDestino):
        if nomeArqOrigem in self.atual.filhos:
            if self.atual.filhos[nomeArqOrigem].tipo == "arquivo":
                if nomeArqOrigem == nomeArqDestino:
                    copia_nome = self.gerar_nome_copia(nomeArqOrigem)
                    self.atual.filhos[copia_nome] = No(copia_nome, "arquivo")
                    self.atual.filhos[copia_nome].pai = self.atual
                    self.atual.filhos[copia_nome].conteudo = self.atual.filhos[
                        nomeArqOrigem
                    ].conteudo
                else:
                    self.atual.filhos[nomeArqDestino] = No(nomeArqDestino, "arquivo")
                    self.atual.filhos[nomeArqDestino].pai = self.atual
                    self.atual.filhos[nomeArqDestino].conteudo = self.atual.filhos[
                        nomeArqOrigem
                    ].conteudo

                print("Arquivo copiado com sucesso.")
            else:
                print("[ERRO]: Não é um arquivo.")
        else:
            print("[ERRO]: Arquivo não encontrado.")

    # move o arquivo OU renomeia
    def mv(self, origem, destino):
        if origem not in self.atual.filhos:
            print("[ERRO]: Arquivo ou diretório de origem não encontrado.")
            return

        no_origem = self.atual.filhos[origem]

        # caso 1: destino existe
        if destino in self.atual.filhos:
            no_destino = self.atual.filhos[destino]

            # se destino for diretório, move origem para dentro dele
            if no_destino.tipo == "diretorio":
                if origem in no_destino.filhos:
                    print("[ERRO]: Já existe um item com esse nome no diretório de destino.")
                    return

                del self.atual.filhos[origem]

                no_origem.pai = no_destino
                no_destino.filhos[origem] = no_origem

                print("Movido com sucesso.")
                return

            # se destino existe mas não é diretório, não pode sobrescrever
            print("[ERRO]: Já existe um arquivo com esse nome.")
            return

        # caso 2: destino não existe, então renomeia
        del self.atual.filhos[origem]

        no_origem.nome = destino
        no_origem.pai = self.atual
        self.atual.filhos[destino] = no_origem

        print("Renomeado com sucesso.")

    # ordem do LINUX: chmod(novaPermissao, nome)
    def chmod(self, novaPermissao, nome):
        if nome in self.atual.filhos:
            if len(novaPermissao) == 3:
                if novaPermissao in ["rwx", "rw-", "r--", "r-x",
                                    "-wx", "-w-", "--x", "---"]:
                    self.atual.filhos[nome].permissoes = novaPermissao
                    print("Permissao alterada com sucesso.")
                else:
                    print("[ERRO]: Permissão inválida.")
            else:
                print("[ERRO]: Permissão inválida.")
        else:
            print("[ERRO]: Arquivo ou diretório não encontrado.")


def terminal():
    fs = SistemaArquivos()

    while True:
        entrada = input("mini-fs:/$ ").strip()

        if entrada == "":
            continue

        partes = entrada.split()
        comando = partes[0].lower()


        if comando == "exit":
            print("Encerrando o simulador.")
            break

        elif comando == "pwd":
            print(fs.pwd())

        elif comando == "ls":
            fs.ls()

        elif comando == "mkdir":
            if len(partes) < 2:
                print("Erro: use mkdir <nome>")
            elif len(partes) > 2:
                print("Erro: o nome do diretório não pode conter espaços.")
            else:
                fs.mkdir(partes[1])

        else:
            print("Comando não reconhecido.")

terminal()