from datetime import datetime


class No:
    proximo_inode = 1

    def __init__(self, nome, tipo):
        self.nome = nome
        self.tipo = tipo  # "arquivo" ou "diretorio"
        self.conteudo = ""
        self.filhos = {}
        self.pai = None
        self.permissoes = "rwx"

        # FCB
        agora = datetime.now()
        self.id_inode = No.proximo_inode
        No.proximo_inode += 1
        self.tamanho = 0
        self.data_criacao = agora
        self.data_modificacao = agora
        self.data_acesso = agora
        self.tipo_dado = "caractere"

    def atualizar_acesso(self):
        self.data_acesso = datetime.now()

    def atualizar_modificacao(self):
        self.data_modificacao = datetime.now()

    def atualizar_tamanho(self):
        if self.tipo == "arquivo":
            self.tamanho = len(self.conteudo)
        else:
            self.tamanho = len(self.filhos)


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
            self.atual.atualizar_tamanho()
            self.atual.atualizar_modificacao()

    # cria arquuivo
    def touch(self, nome):
        if nome in self.atual.filhos:
            print("[ERRO]: Já existe um arquivo ou diretório com esse nome.")
        else:
            self.atual.filhos[nome] = No(nome, "arquivo")
            self.atual.filhos[nome].pai = self.atual
            self.atual.atualizar_tamanho()
            self.atual.atualizar_modificacao()

    # mudar de diretório/pasta.
    def cd(self, nome):
        if nome == "..":
            if self.atual == self.root:
                print("Erro: Já está no diretório raiz.")
            else:
                self.atual = self.atual.pai
                self.atual.atualizar_acesso()

        # nome da raiz
        elif nome == "/":
            self.atual = self.root
            self.atual.atualizar_acesso()
        elif nome in self.atual.filhos:
            if self.atual.filhos[nome].tipo == "diretorio":
                if "x" in self.atual.filhos[nome].permissoes:
                    self.atual = self.atual.filhos[nome]
                    self.atual.atualizar_acesso()
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
                self.atual.filhos[nome].atualizar_tamanho()
                self.atual.filhos[nome].atualizar_modificacao()
            else:
                print("Erro: Sem permissão de escrita.")
        else:
            if nome in self.atual.filhos:
                print("[ERRO]: Já existe um arquivo ou diretório com esse nome.")
            else:
                self.atual.filhos[nome] = No(nome, "arquivo")
                self.atual.filhos[nome].pai = self.atual
                self.atual.filhos[nome].conteudo = conteudo
                self.atual.filhos[nome].atualizar_tamanho()
                self.atual.filhos[nome].atualizar_modificacao()
                self.atual.atualizar_tamanho()
                self.atual.atualizar_modificacao()

    # mostra o conteudo de um arquivo
    def cat(self, nome):
        if nome in self.atual.filhos and self.atual.filhos[nome].tipo == "arquivo":
            if "r" in self.atual.filhos[nome].permissoes:
                print(self.atual.filhos[nome].conteudo)
                self.atual.filhos[nome].atualizar_acesso()
            else:
                print("Erro: Sem permissão de leitura.")
        else:
            print("Erro: Arquivo não encontrado.")

    # deleta um arquivo
    def rm(self, nome):
        if nome in self.atual.filhos:
            if self.atual.filhos[nome].tipo == "arquivo":
                del self.atual.filhos[nome]
                self.atual.atualizar_tamanho()
                self.atual.atualizar_modificacao()
                print("Arquivo removido com sucesso.")
            elif (
                self.atual.filhos[nome].tipo == "diretorio"
                and self.atual.filhos[nome].filhos == {}
            ):
                del self.atual.filhos[nome]
                self.atual.atualizar_tamanho()
                self.atual.atualizar_modificacao()
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
                arquivo_origem = self.atual.filhos[nomeArqOrigem]

                if nomeArqOrigem == nomeArqDestino:
                    nome_final = self.gerar_nome_copia(nomeArqOrigem)
                else:
                    nome_final = nomeArqDestino

                self.atual.filhos[nome_final] = No(nome_final, "arquivo")
                self.atual.filhos[nome_final].pai = self.atual
                self.atual.filhos[nome_final].conteudo = arquivo_origem.conteudo
                self.atual.filhos[nome_final].permissoes = arquivo_origem.permissoes
                self.atual.filhos[nome_final].tipo_dado = arquivo_origem.tipo_dado
                self.atual.filhos[nome_final].atualizar_tamanho()
                self.atual.filhos[nome_final].atualizar_modificacao()
                arquivo_origem.atualizar_acesso()
                self.atual.atualizar_tamanho()
                self.atual.atualizar_modificacao()

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
                no_origem.atualizar_modificacao()
                no_destino.atualizar_tamanho()
                no_destino.atualizar_modificacao()
                self.atual.atualizar_tamanho()
                self.atual.atualizar_modificacao()

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
        no_origem.atualizar_modificacao()
        self.atual.atualizar_modificacao()

        print("Renomeado com sucesso.")

    # ordem do LINUX: chmod(novaPermissao, nome)
    def chmod(self, novaPermissao, nome):
        if nome in self.atual.filhos:
            if len(novaPermissao) == 3:
                if novaPermissao in ["rwx", "rw-", "r--", "r-x",
                                    "-wx", "-w-", "--x", "---"]:
                    self.atual.filhos[nome].permissoes = novaPermissao
                    self.atual.filhos[nome].atualizar_modificacao()
                    print("Permissao alterada com sucesso.")
                else:
                    print("[ERRO]: Permissão inválida.")
            else:
                print("[ERRO]: Permissão inválida.")
        else:
            print("[ERRO]: Arquivo ou diretório não encontrado.")

    def formatar_data(self, data):
        return data.strftime("%Y-%m-%d %H:%M:%S")

    def stat(self, nome):
        if nome not in self.atual.filhos:
            print("[ERRO]: Arquivo ou diretório não encontrado.")
            return

        no = self.atual.filhos[nome]
        no.atualizar_acesso()

        print("Nome: " + no.nome)
        print("Inode: " + str(no.id_inode))
        print("Tipo: " + no.tipo)
        print("Tipo de dado: " + no.tipo_dado)
        print("Tamanho: " + str(no.tamanho))
        print("Permissoes: " + no.permissoes)
        print("Criado em: " + self.formatar_data(no.data_criacao))
        print("Modificado em: " + self.formatar_data(no.data_modificacao))
        print("Acessado em: " + self.formatar_data(no.data_acesso))


def terminal():
    fs = SistemaArquivos()

    while True:
        entrada = input(f"mini-fs:{fs.pwd()}$ ").strip()

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

        elif comando == "cd":
            if len(partes) < 2:
                print("Erro: use cd <diretorio>")
            elif len(partes) > 2:
                print("Erro: o nome do diretório não pode conter espaços.")
            else:
                fs.cd(partes[1])

        elif comando == "touch":
            if len(partes) < 2:
                print("Erro: use touch <arquivo>")
            elif len (partes) > 2:
                print("Erros: o nome do arquivo não pode conter espaços.")
            else:
                fs.touch(partes[1])

        elif comando == "cat":
            if len(partes) < 2:
                print("Erro: use cat <arquivo>")
            elif len(partes) > 2:
                print("Erro: o nome do arquivo não pode conter espaços.")
            else:
                fs.cat(partes[1])

        elif comando == "stat":
            if len(partes) < 2:
                print("Erro: use stat <arquivo_ou_diretorio>")
            elif len(partes) > 2:
                print("Erro: o nome do arquivo ou diretório não pode conter espaços.")
            else:
                fs.stat(partes[1])

        elif comando == "echo":
            if ">" not in partes:
                print("Erro: use echo <texto> > <arquivo>")
                continue

            if partes.count(">") != 1:
                print("Erro: use apenas um > no formato echo <texto> > <arquivo>")
                continue

            else:
                indice = partes.index(">")

            if indice == 1:
                print("Erro: informe o texto antes do >")

            elif indice + 1 >= len(partes):
                print("Erro: informe o nome do arquivo depois do >")

            elif indice + 2 < len(partes):
                print("Erro: o nome do arquivo não pode conter espaços.")
                
            else:
                texto = " ".join(partes[1:indice])
                arquivo = partes[indice + 1]
                fs.echo(texto, arquivo)

        elif comando == "rm":
            if len(partes) < 2:
                print("Erro: use rm <arquivo_ou_diretorio>")

            elif len(partes) > 2:
                print("Erro: o nome do arquivo ou diretório não pode conter espaços.")
            else:
                fs.rm(partes[1])

        elif comando == "cp":
            if len(partes) < 3:
                print("Erro: use cp <origem> <destino>")
            elif len(partes) > 3:
                print("Erro: o nome do arquivo não pode conter espaços.")
            else:
                fs.cp(partes[1], partes[2])

        elif comando == "mv":
            if len(partes) < 3:
                print("Erro: use mv <origem> <destino>")
            elif len(partes) > 3:
                print("Erro: o nome do arquivo não pode conter espaços.")
            else:
                fs.mv(partes[1], partes[2])

        elif comando == "chmod":
            if len(partes) < 3:
                print("Erro: use chmod <permissao> <arquivo_ou_diretorio>")
            elif len(partes) > 3:
                print("Erro: o nome do arquivo ou diretório não pode conter espaços.")
            else:
                fs.chmod(partes[1], partes[2])

        else:
            print("Comando não reconhecido.")

if __name__ == "__main__":
    terminal()
