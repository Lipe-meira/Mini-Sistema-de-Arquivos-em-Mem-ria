from datetime import datetime


class No:
    proximo_inode = 1

    def __init__(self, nome, tipo):
        self.nome = nome
        self.tipo = tipo  # "arquivo" ou "diretorio"
        self.conteudo = ""
        self.filhos = {}
        self.pai = None
        self.permissoes = 0o777
        self.owner = "felipe"
        self.group = "alunos"
        self.blocos = []

        # FCB
        agora = datetime.now()
        self.id_inode = No.proximo_inode
        No.proximo_inode += 1
        self.tamanho = 0
        self.data_criacao = agora
        self.data_modificacao = agora
        self.data_acesso = agora
        if tipo == "arquivo":
            self.tipo_dado = "caractere"
        else:
            self.tipo_dado = "diretorio"

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
        self.tamanho_bloco = 4
        self.disco = []
        self.usuario_atual = "felipe"
        self.grupo_atual = "alunos"

    def obter_permissao_usuario(self, no):
        if self.usuario_atual == no.owner:
            deslocamento = 6
        elif self.grupo_atual == no.group:
            deslocamento = 3
        else:
            deslocamento = 0

        return (no.permissoes >> deslocamento) & 0b111

    def tem_permissao(self, no, permissao):
        valores_permissao = {"r": 4, "w": 2, "x": 1}

        if permissao not in valores_permissao:
            return False

        bits_usuario = self.obter_permissao_usuario(no)
        valor_necessario = valores_permissao[permissao]
        return (bits_usuario & valor_necessario) != 0

    def permissoes_numericas(self, no):
        return format(no.permissoes, "03o")

    def permissoes_rwx(self, no):
        texto = ""

        for deslocamento in [6, 3, 0]:
            bits = (no.permissoes >> deslocamento) & 0b111
            texto += "r" if bits & 4 else "-"
            texto += "w" if bits & 2 else "-"
            texto += "x" if bits & 1 else "-"

        return texto

    def permissao_numerica_valida(self, permissao):
        if len(permissao) != 3:
            return False

        if not permissao.isdigit():
            return False

        for digito in permissao:
            if digito < "0" or digito > "7":
                return False

        return True
    
    def nome_valido(self, nome):
        nomes_invalidos = ["/", ".", "..", ">", ">>"]

        if nome in nomes_invalidos:
            return False

        if "/" in nome:
            return False

        return True

    def alocar_bloco(self, dados):
        for indice in range(len(self.disco)):
            if self.disco[indice] is None:
                self.disco[indice] = dados
                return indice

        self.disco.append(dados)
        return len(self.disco) - 1

    def liberar_blocos(self, no):
        for indice in no.blocos:
            if 0 <= indice < len(self.disco):
                self.disco[indice] = None

        no.blocos = []

    def gravar_conteudo(self, no, conteudo):
        self.liberar_blocos(no)
        no.conteudo = conteudo

        for inicio in range(0, len(conteudo), self.tamanho_bloco):
            # inicio : ate onde vai alocar
            parte = conteudo[inicio:inicio + self.tamanho_bloco]
            indice = self.alocar_bloco(parte)
            no.blocos.append(indice)

        no.atualizar_tamanho()
        no.atualizar_modificacao()

    def ler_conteudo(self, no):
        partes = []

        for indice in no.blocos:
            if 0 <= indice < len(self.disco) and self.disco[indice] is not None:
                partes.append(self.disco[indice])

        no.conteudo = "".join(partes)
        return no.conteudo

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
        if not self.nome_valido(nome):
            print("Erro: nome inválido.")
            return

        if not self.tem_permissao(self.atual, "w"):
            print("Erro: Sem permissão de escrita no diretório atual.")
            return

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
        if not self.nome_valido(nome):
            print("Erro: nome inválido.")
            return

        if not self.tem_permissao(self.atual, "w"):
            print("Erro: Sem permissão de escrita no diretório atual.")
            return

        if nome in self.atual.filhos:
            print("Erro: Já existe um arquivo ou diretório com esse nome.")
        else:
            self.atual.filhos[nome] = No(nome, "arquivo")
            self.atual.filhos[nome].pai = self.atual
            self.atual.atualizar_tamanho()
            self.atual.atualizar_modificacao()

    # mudar de diretorio/pasta.
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
                if self.tem_permissao(self.atual.filhos[nome], "x"):
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
        if not self.nome_valido(nome):
            print("Erro: nome inválido.")
            return

        if nome in self.atual.filhos and self.atual.filhos[nome].tipo == "arquivo":
            if self.tem_permissao(self.atual.filhos[nome], "w"):
                self.gravar_conteudo(self.atual.filhos[nome], conteudo)
            else:
                print("Erro: Sem permissão de escrita.")
        else:
            if nome in self.atual.filhos:
                print("Erro: Já existe um arquivo ou diretório com esse nome.")
            else:
                if not self.tem_permissao(self.atual, "w"):
                    print("Erro: Sem permissão de escrita no diretório atual.")
                    return

                self.atual.filhos[nome] = No(nome, "arquivo")
                self.atual.filhos[nome].pai = self.atual
                self.gravar_conteudo(self.atual.filhos[nome], conteudo)
                self.atual.atualizar_tamanho()
                self.atual.atualizar_modificacao()

    # mostra o conteudo de um arquivo
    def cat(self, nome):
        if nome in self.atual.filhos and self.atual.filhos[nome].tipo == "arquivo":
            if self.tem_permissao(self.atual.filhos[nome], "r"):
                print(self.ler_conteudo(self.atual.filhos[nome]))
                self.atual.filhos[nome].atualizar_acesso()
            else:
                print("Erro: Sem permissão de leitura.")
        else:
            print("Erro: Arquivo não encontrado.")

    # deleta um arquivo
    def rm(self, nome):
        if nome in self.atual.filhos:
            no = self.atual.filhos[nome]

            if not self.tem_permissao(no, "w"):
                print("Erro: Sem permissão para remover.")
                return

            if no.tipo == "arquivo":
                self.liberar_blocos(no)
                del self.atual.filhos[nome]
                self.atual.atualizar_tamanho()
                self.atual.atualizar_modificacao()
                print("Arquivo removido com sucesso.")
            elif (
                no.tipo == "diretorio"
                and no.filhos == {}
            ):
                del self.atual.filhos[nome]
                self.atual.atualizar_tamanho()
                self.atual.atualizar_modificacao()
                print("Diretorio removido com sucesso.")
            else:
                print("Erro: Diretório não está vazio.")
        else:
            print("Erro: Arquivo ou diretório não encontrado.")

    def gerar_nome_copia(self, nome):
        # separa nome e extensao
        if "." in nome:
            base, extensao = nome.rsplit(".", 1)
            extensao = "." + extensao
        else:
            base = nome
            extensao = ""

        # se ainda nao tem _copia, adiciona
        if base.endswith("_copia"):
            prefixo = base
        else:
            prefixo = base + "_copia"

        novo_nome = prefixo + extensao

        # se arquivo_copia.txt ainda nao existe, usa ele
        if novo_nome not in self.atual.filhos:
            return novo_nome

        # se ja existe, começa a tentar (1), (2), (3)...
        contador = 1

        while True:
            novo_nome = prefixo + "(" + str(contador) + ")" + extensao

            if novo_nome not in self.atual.filhos:
                return novo_nome

            contador += 1

    # copiar, duplicar o arquivo alvo em outro lugar
    def cp(self, nomeArqOrigem, nomeArqDestino):
        if not self.nome_valido(nomeArqDestino):
            print("Erro: nome inválido.")
            return

        if nomeArqOrigem in self.atual.filhos:
            if self.atual.filhos[nomeArqOrigem].tipo == "arquivo":
                arquivo_origem = self.atual.filhos[nomeArqOrigem]

                if not self.tem_permissao(arquivo_origem, "r"):
                    print("Erro: Sem permissão de leitura.")
                    return

                if nomeArqOrigem == nomeArqDestino:
                    nome_final = self.gerar_nome_copia(nomeArqOrigem)
                else:
                    nome_final = nomeArqDestino

                if nome_final in self.atual.filhos:
                    if self.atual.filhos[nome_final].tipo == "arquivo":
                        if not self.tem_permissao(self.atual.filhos[nome_final], "w"):
                            print("Erro: Sem permissão de escrita no arquivo de destino.")
                            return

                        self.liberar_blocos(self.atual.filhos[nome_final])
                    else:
                        print("Erro: Já existe um diretório com esse nome.")
                        return
                else:
                    if not self.tem_permissao(self.atual, "w"):
                        print("Erro: Sem permissão de escrita no diretório atual.")
                        return

                self.atual.filhos[nome_final] = No(nome_final, "arquivo")
                self.atual.filhos[nome_final].pai = self.atual
                self.atual.filhos[nome_final].permissoes = arquivo_origem.permissoes
                self.atual.filhos[nome_final].tipo_dado = arquivo_origem.tipo_dado
                self.gravar_conteudo(
                    self.atual.filhos[nome_final], self.ler_conteudo(arquivo_origem)
                )
                arquivo_origem.atualizar_acesso()
                self.atual.atualizar_tamanho()
                self.atual.atualizar_modificacao()

                print("Arquivo copiado com sucesso.")
            else:
                print("Erro: Não é um arquivo.")
        else:
            print("Erro: Arquivo não encontrado.")

    # move o arquivo OU renomeia
    def mv(self, origem, destino):
        if origem == destino:
            print("Erro: origem e destino sao iguais.")
            return

        if not self.nome_valido(destino):
            print("Erro: nome inválido.")
            return

        if origem not in self.atual.filhos:
            print("Erro: Arquivo ou diretório de origem não encontrado.")
            return

        no_origem = self.atual.filhos[origem]

        if not self.tem_permissao(no_origem, "w"):
            print("Erro: Sem permissão para mover ou renomear.")
            return

        # caso 1: destino existe
        if destino in self.atual.filhos:
            no_destino = self.atual.filhos[destino]

            # se destino for diretorio, move origem para dentro dele
            if no_destino.tipo == "diretorio":
                if not self.tem_permissao(no_destino, "w"):
                    print("Erro: Sem permissão de escrita no diretório de destino.")
                    return

                if origem in no_destino.filhos:
                    print("Erro: Já existe um item com esse nome no diretório de destino.")
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
            print("Erro: Já existe um arquivo com esse nome.")
            return

        # caso 2: destino não existe, então renomeia
        if not self.tem_permissao(self.atual, "w"):
            print("Erro: Sem permissão de escrita no diretório atual.")
            return

        del self.atual.filhos[origem]

        no_origem.nome = destino
        no_origem.pai = self.atual
        self.atual.filhos[destino] = no_origem
        no_origem.atualizar_modificacao()
        self.atual.atualizar_modificacao()

        print("Renomeado com sucesso.")

    # ordem do LINUX: chmod(novaPermissao, nome)
    def chmod(self, novaPermissao, nome):
        if nome not in self.atual.filhos:
            print("Erro: Arquivo ou diretorio nao encontrado.")
            return

        if not self.permissao_numerica_valida(novaPermissao):
            print("Erro: Permissao invalida.")
            return

        self.atual.filhos[nome].permissoes = int(novaPermissao, 8)
        self.atual.filhos[nome].atualizar_modificacao()
        print("Permissao alterada com sucesso.")

    def formatar_data(self, data):
        return data.strftime("%Y-%m-%d %H:%M:%S")

    def stat(self, nome):
        if nome not in self.atual.filhos:
            print("[ERRO]: Arquivo ou diretorio nao encontrado.")
            return

        no = self.atual.filhos[nome]
        no.atualizar_acesso()

        print("Nome: " + no.nome)
        print("Inode: " + str(no.id_inode))
        print("Tipo: " + no.tipo)
        print("Tipo de dado: " + no.tipo_dado)
        print("Tamanho: " + str(no.tamanho))
        print("Permissões numéricas: " + self.permissoes_numericas(no))
        print("Permissões RWX: " + self.permissoes_rwx(no))
        print("Owner: " + no.owner)
        print("Grupo: " + no.group)
        print("Blocos: " + str(no.blocos))
        print("Criado em: " + self.formatar_data(no.data_criacao))
        print("Modificado em: " + self.formatar_data(no.data_modificacao))
        print("Acessado em: " + self.formatar_data(no.data_acesso))

    def mostrar_disco(self):
        print("Tamanho do bloco: " + str(self.tamanho_bloco))

        if len(self.disco) == 0:
            print("Disco vazio.")
            return

        for indice in range(len(self.disco)):
            if self.disco[indice] is None:
                print("Bloco " + str(indice) + ": LIVRE")
            else:
                print("Bloco " + str(indice) + ": " + self.disco[indice])


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

        elif comando == "disco":
            if len(partes) > 1:
                print("Erro: use apenas disco")
            else:
                fs.mostrar_disco()

        elif comando == "mkdir":
            if len(partes) < 2:
                print("Erro: use mkdir <nome>")
            elif len(partes) > 2:
                print("Erro: o nome do diretorio nao pode conter espacos.")
            else:
                fs.mkdir(partes[1])

        elif comando == "cd":
            if len(partes) < 2:
                print("Erro: use cd <diretorio>")
            elif len(partes) > 2:
                print("Erro: o nome do diretorio nao pode conter espacos.")
            else:
                fs.cd(partes[1])

        elif comando == "touch":
            if len(partes) < 2:
                print("Erro: use touch <arquivo>")
            elif len (partes) > 2:
                print("Erros: o nome do arquivo nao pode conter espacos.")
            else:
                fs.touch(partes[1])

        elif comando == "cat":
            if len(partes) < 2:
                print("Erro: use cat <arquivo>")
            elif len(partes) > 2:
                print("Erro: o nome do arquivo nao pode conter espacos.")
            else:
                fs.cat(partes[1])

        elif comando == "stat":
            if len(partes) < 2:
                print("Erro: use stat <arquivo_ou_diretorio>")
            elif len(partes) > 2:
                print("Erro: o nome do arquivo ou diretorio nao pode conter espacos.")
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
                print("Erro: o nome do arquivo nao pode conter espacos.")
                
            else:
                texto = " ".join(partes[1:indice])
                arquivo = partes[indice + 1]
                fs.echo(texto, arquivo)

        elif comando == "rm":
            if len(partes) < 2:
                print("Erro: use rm <arquivo_ou_diretorio>")

            elif len(partes) > 2:
                print("Erro: o nome do arquivo ou diretorio nao pode conter espacos.")
            else:
                fs.rm(partes[1])

        elif comando == "cp":
            if len(partes) < 3:
                print("Erro: use cp <origem> <destino>")
            elif len(partes) > 3:
                print("Erro: o nome do arquivo nao pode conter espacos.")
            else:
                fs.cp(partes[1], partes[2])

        elif comando == "mv":
            if len(partes) < 3:
                print("Erro: use mv <origem> <destino>")
            elif len(partes) > 3:
                print("Erro: o nome do arquivo nao pode conter espacos.")
            else:
                fs.mv(partes[1], partes[2])

        elif comando == "chmod":
            if len(partes) < 3:
                print("Erro: use chmod <permissao> <arquivo_ou_diretorio>")
            elif len(partes) > 3:
                print("Erro: o nome do arquivo ou diretorio nao pode conter espacos.")
            else:
                fs.chmod(partes[1], partes[2])

        else:
            print("Comando nao reconhecido.")

if __name__ == "__main__":
    terminal()
