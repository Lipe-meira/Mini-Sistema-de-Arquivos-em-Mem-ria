# Mini Sistema de Arquivos em Memória

Este projeto é um simulador simples de sistema de arquivos feito em Python para a disciplina de Sistemas Operacionais.

A ideia é simular, em memória, alguns conceitos de um sistema de arquivos parecido com Linux, como diretórios em árvore, arquivos, metadados, inode, permissões RWX, comandos básicos e alocação de blocos.

O programa não mexe nos arquivos reais do computador. Tudo acontece dentro da execução do Python e é perdido quando o simulador é encerrado.

\---

## Objetivo do projeto

O objetivo principal é mostrar, de forma prática, como um sistema de arquivos pode organizar arquivos e diretórios internamente.

O simulador implementa conceitos como:

* árvore de diretórios;
* criação, leitura, escrita, cópia, movimentação e remoção de arquivos;
* metadados de arquivos e diretórios;
* FCB, com um inode simulado;
* permissões RWX usando valores octais, como `777`, `700`, `400`;
* verificação de permissões antes das operações;
* simulação de blocos de disco;
* tratamento de erros comuns.

\---

## Como executar

Como o projeto foi feito em Python, não precisa compilar.

Primeiro, tenha o Python 3 instalado.

Depois, no terminal, entre na pasta do projeto e execute:

```bash
python mini\_fs.py
```

Em alguns sistemas, pode ser necessário usar:

```bash
python3 mini\_fs.py
```

Ao executar, o simulador abre um terminal próprio, parecido com:

```bash
mini-fs:/$
```

Para sair do simulador, use:

```bash
exit
```

\---

## Comandos disponíveis

### `pwd`

Mostra o caminho atual dentro do sistema de arquivos simulado.

```bash
pwd
```

Exemplo de saída:

```text
/
```

\---

### `ls`

Lista os arquivos e diretórios do diretório atual.

```bash
ls
```

Exemplo:

```text
\[DIR] docs
\[ARQ] a.txt
```

O comando verifica se o diretório atual tem permissão de leitura (`r`).

\---

### `mkdir <nome>`

Cria um diretório no diretório atual.

```bash
mkdir docs
```

O comando verifica:

* se o nome é válido;
* se já existe arquivo ou diretório com o mesmo nome;
* se o diretório atual tem permissão de escrita (`w`).

\---

### `cd <diretorio>`

Entra em um diretório.

```bash
cd docs
```

Também aceita:

```bash
cd ..
cd /
```

O comando verifica se o destino é realmente um diretório e se ele tem permissão de entrada (`x`).

\---

### `touch <arquivo>`

Cria um arquivo vazio.

```bash
touch a.txt
```

O comando verifica se o diretório atual tem permissão de escrita (`w`).

\---

### `echo <texto> > <arquivo>`

Escreve conteúdo em um arquivo.

```bash
echo ola mundo > a.txt
```

Se o arquivo já existir, o conteúdo antigo é substituído.

Se o arquivo não existir, ele é criado.

O comando verifica:

* permissão de escrita (`w`) no arquivo, se ele já existir;
* permissão de escrita (`w`) no diretório atual, se for criar um arquivo novo.

\---

### `cat <arquivo>`

Mostra o conteúdo de um arquivo.

```bash
cat a.txt
```

O comando verifica se o arquivo tem permissão de leitura (`r`).

\---

### `rm <arquivo\_ou\_diretorio>`

Remove um arquivo ou diretório.

```bash
rm a.txt
rm docs
```

Regras implementadas:

* arquivos têm seus blocos liberados antes de serem removidos;
* diretórios só podem ser removidos se estiverem vazios;
* o item precisa ter permissão de escrita (`w`) para ser removido.

Observação: no Linux real, a remoção depende principalmente da permissão no diretório pai. Neste simulador, foi usada uma regra didática baseada na permissão do próprio item.

\---

### `cp <origem> <destino>`

Copia um arquivo.

```bash
cp a.txt b.txt
```

Regras implementadas:

* só copia arquivos, não diretórios;
* a origem precisa ter permissão de leitura (`r`);
* se o destino já existir e for arquivo, precisa ter permissão de escrita (`w`);
* se o destino não existir, o diretório atual precisa ter permissão de escrita (`w`);
* se origem e destino tiverem o mesmo nome, o sistema cria uma cópia automática.

Exemplo:

```bash
cp a.txt a.txt
```

Pode gerar:

```text
a\_copia.txt
```

Se já existir `a\_copia.txt`, ele tenta nomes como:

```text
a\_copia(1).txt
a\_copia(2).txt
```

\---

### `mv <origem> <destino>`

Move ou renomeia um arquivo/diretório.

```bash
mv a.txt b.txt
mv a.txt docs
```

Se o destino não existir, o comando funciona como renomear.

Se o destino existir e for diretório, o comando move a origem para dentro dele.

Regras implementadas:

* origem e destino não podem ser iguais;
* a origem precisa ter permissão de escrita (`w`);
* para mover para um diretório, o diretório de destino precisa ter permissão de escrita (`w`) e entrada (`x`);
* não sobrescreve arquivo ou diretório já existente no destino.

\---

### `chmod <permissao> <arquivo\_ou\_diretorio>`

Altera as permissões de um arquivo ou diretório.

```bash
chmod 700 a.txt
chmod 400 a.txt
chmod 777 docs
```

A permissão deve ter exatamente três dígitos octais, de `0` até `7`.

Exemplos:

* `777` = dono, grupo e outros podem ler, escrever e executar;
* `700` = apenas o dono pode ler, escrever e executar;
* `400` = apenas o dono pode ler;
* `200` = apenas o dono pode escrever;
* `500` = dono pode ler e entrar/executar, mas não escrever.

\---

### `stat <arquivo\_ou\_diretorio>`

Mostra os metadados de um arquivo ou diretório.

```bash
stat a.txt
```

Exemplo de informações mostradas:

```text
Nome: a.txt
Inode: 2
Tipo: arquivo
Tipo de dado: caractere
Tamanho: 10
Permissões numéricas: 777
Permissões RWX: rwxrwxrwx
Owner: felipe
Grupo: alunos
Blocos: \[0, 1]
Criado em: ...
Modificado em: ...
Acessado em: ...
```

\---

### `disco`

Mostra os blocos do disco simulado.

```bash
disco
```

Exemplo:

```text
Tamanho do bloco: 4
Bloco 0: ola 
Bloco 1: mund
Bloco 2: o
```

Neste projeto, cada bloco tem tamanho 4. Então um conteúdo maior é dividido em partes de 4 caracteres.

\---

## Estrutura principal do código

O código está organizado principalmente em duas classes:

* `No`
* `SistemaArquivos`

\---

## Classe `No`

A classe `No` representa tanto arquivos quanto diretórios.

Cada objeto possui informações como:

```python
self.nome
self.tipo
self.conteudo
self.filhos
self.pai
self.permissoes
self.owner
self.group
self.blocos
```

Se o nó for um arquivo, ele pode ter conteúdo e blocos associados.

Se o nó for um diretório, ele usa o dicionário `filhos` para guardar os arquivos e subdiretórios dentro dele.

O atributo `pai` aponta para o diretório anterior, permitindo navegar com `cd ..` e montar o caminho usado pelo `pwd`.

\---

## FCB e inode simulado

No trabalho, cada arquivo precisa ter um File Control Block, ou FCB.

No código, o próprio objeto da classe `No` funciona como esse FCB simplificado.

Ele guarda os principais metadados do arquivo ou diretório:

```python
self.id\_inode
self.tamanho
self.data\_criacao
self.data\_modificacao
self.data\_acesso
self.tipo\_dado
self.permissoes
self.blocos
```

O `id\_inode` é um número único gerado automaticamente:

```python
No.proximo\_inode = 1
```

Cada novo arquivo ou diretório recebe um inode diferente.

Isso simula a ideia de inode usada em sistemas Unix/Linux, onde o arquivo tem um identificador interno além do nome.

\---

## Classe `SistemaArquivos`

A classe `SistemaArquivos` controla o funcionamento geral do simulador.

Ela guarda:

```python
self.root
self.atual
self.tamanho\_bloco
self.disco
self.usuario\_atual
self.grupo\_atual
```

* `root` é o diretório raiz `/`;
* `atual` é o diretório onde o usuário está no momento;
* `tamanho\_bloco` define o tamanho dos blocos simulados;
* `disco` é uma lista que representa o disco em memória;
* `usuario\_atual` e `grupo\_atual` simulam o usuário e grupo que estão executando os comandos.

\---

## Árvore de diretórios

A estrutura de diretórios é feita como uma árvore.

O diretório raiz `/` fica no topo.

Cada diretório pode ter vários filhos dentro do dicionário `filhos`.

Exemplo conceitual:

```text
/
├── docs
│   └── texto.txt
└── a.txt
```

No código, isso fica parecido com:

```python
self.root.filhos\["docs"]
self.root.filhos\["a.txt"]
```

E o diretório `docs` também pode ter seus próprios filhos:

```python
docs.filhos\["texto.txt"]
```

Essa estrutura facilita a navegação, a organização e o agrupamento de arquivos.

\---

## Permissões RWX

O projeto usa permissões no estilo Linux:

* `r` = read = leitura;
* `w` = write = escrita;
* `x` = execute = execução/entrada em diretório.

As permissões são divididas em três grupos:

* proprietário;
* grupo;
* outros.

Exemplo:

```text
rwxr-x---
```

No código, as permissões são guardadas como número octal:

```python
self.permissoes = 0o777
```

Para verificar permissões, o projeto usa operações bit a bit.

Exemplo de função usada:

```python
def tem\_permissao(self, no, permissao):
```

Ela compara os bits de permissão do usuário atual com a permissão necessária para a operação.

\---

## Simulação de blocos

O projeto também simula a alocação de blocos de disco.

O disco é uma lista:

```python
self.disco = \[]
```

Cada bloco tem tamanho 4:

```python
self.tamanho\_bloco = 4
```

Quando um arquivo recebe conteúdo, o texto é dividido em blocos.

Exemplo:

```bash
echo abcd1234 > a.txt
```

O conteúdo pode ser separado assim:

```text
Bloco 0: abcd
Bloco 1: 1234
```

O arquivo guarda os índices desses blocos no atributo:

```python
self.blocos
```

Isso se parece com uma alocação indexada simplificada, porque o FCB/inode do arquivo guarda uma lista apontando para os blocos onde o conteúdo está.

Quando um arquivo é removido, seus blocos são liberados e podem ser reutilizados por outros arquivos.

\---

## Tratamento de erros

O simulador trata vários erros comuns, como:

* comando desconhecido;
* arquivo ou diretório não encontrado;
* tentar entrar em arquivo usando `cd`;
* tentar remover diretório não vazio;
* tentar criar item com nome inválido;
* tentar criar item com nome repetido;
* tentar ler arquivo sem permissão;
* tentar escrever em arquivo sem permissão;
* tentar listar diretório sem permissão de leitura;
* tentar entrar em diretório sem permissão de entrada;
* tentar mover arquivo para diretório sem permissão adequada;
* tentar usar `chmod` com permissão inválida.

Exemplo:

```bash
chmod 400 a.txt
echo novo > a.txt
```

Saída esperada:

```text
Erro: Sem permissão de escrita.
```

\---

## Exemplos de uso

Exemplo básico:

```bash
mkdir docs
cd docs
touch a.txt
echo ola mundo > a.txt
cat a.txt
stat a.txt
disco
exit
```

Exemplo com permissões:

```bash
touch secreto.txt
echo senha > secreto.txt
chmod 200 secreto.txt
cat secreto.txt
```

Saída esperada:

```text
Erro: Sem permissão de leitura.
```

Exemplo de blocos:

```bash
touch a.txt
echo abcd1234 > a.txt
disco
rm a.txt
disco
```

Primeiro o disco mostra os blocos ocupados. Depois do `rm`, os blocos aparecem como `LIVRE`.

\---

## Comparação com comandos Linux reais

O simulador usa comandos parecidos com Linux:

|Simulador|Linux real|Função|
|-|-|-|
|`pwd`|`pwd`|Mostra o diretório atual|
|`ls`|`ls`|Lista arquivos e diretórios|
|`mkdir`|`mkdir`|Cria diretório|
|`cd`|`cd`|Navega entre diretórios|
|`touch`|`touch`|Cria arquivo vazio|
|`cat`|`cat`|Lê arquivo|
|`echo >`|`echo >`|Escreve em arquivo|
|`rm`|`rm`|Remove arquivo ou diretório|
|`cp`|`cp`|Copia arquivo|
|`mv`|`mv`|Move ou renomeia|
|`chmod`|`chmod`|Altera permissões|
|`stat`|`stat`|Mostra metadados|

A diferença é que no projeto tudo acontece dentro da memória do programa, e não no sistema de arquivos real do computador.

\---

## Limitações conhecidas

Como o objetivo é didático, o simulador não implementa tudo que um sistema de arquivos real teria.

Algumas limitações:

* os dados não são persistidos após fechar o programa;
* não há vários usuários reais, apenas usuário e grupo simulados;
* não aceita caminhos completos como `docs/a.txt`, apenas nomes no diretório atual;
* não implementa links simbólicos ou hard links;
* não implementa append com `>>`;
* o `echo` sobrescreve o conteúdo inteiro do arquivo;
* o `rm` usa permissão do próprio item, e não exatamente a regra do Linux real baseada no diretório pai;
* ao sobrescrever com `cp`, o arquivo de destino é recriado internamente;
* o tamanho dos blocos é fixo em 4 caracteres apenas para facilitar a visualização.

Essas limitações foram mantidas para deixar o projeto mais simples, explicável e focado nos conceitos principais da disciplina.

\---

## Relação com os conceitos de Sistemas Operacionais

O projeto demonstra os principais conceitos pedidos no trabalho:

### Conceito de arquivo

Um arquivo é tratado como uma unidade lógica de armazenamento, com nome, conteúdo e atributos.

No código, ele é representado por um objeto da classe `No` com `tipo = "arquivo"`.

### Atributos do arquivo

O arquivo possui metadados como tamanho, datas, tipo, permissões e inode.

Esses dados ficam dentro do objeto `No`, funcionando como um FCB.

### Operações com arquivos

O simulador implementa operações como criar, ler, escrever, copiar, mover, renomear e excluir.

Essas operações são parecidas com comandos Linux, mas executadas apenas na estrutura simulada.

### FCB e inode

O FCB é representado pela classe `No`, que guarda as informações necessárias para controlar o arquivo.

O inode é simulado pelo atributo `id\_inode`, que recebe um valor único para cada novo nó criado.

### Estrutura de diretórios

Os diretórios são organizados em árvore a partir da raiz `/`.

Cada diretório guarda seus filhos em um dicionário, permitindo criar uma hierarquia de pastas e arquivos.

### Proteção de acesso

As permissões RWX controlam o que o usuário atual pode fazer.

Antes de ler, escrever, listar ou entrar em diretórios, o sistema verifica se a permissão necessária existe.

### Alocação de blocos

O conteúdo dos arquivos é dividido em blocos de tamanho fixo.

Cada arquivo guarda a lista dos blocos que pertencem a ele, simulando uma alocação indexada simplificada.

\---

## Teste rápido sugerido

Um teste geral para validar o funcionamento básico:

```bash
pwd
mkdir docs
touch a.txt
echo ola mundo teste > a.txt
cat a.txt
stat a.txt
disco
cp a.txt b.txt
cat b.txt
mv b.txt docs
cd docs
ls
cat b.txt
cd ..
chmod 400 a.txt
echo novo > a.txt
cp docs a.txt
ls
rm a.txt
chmod 700 a.txt
rm a.txt
disco
exit
```

Esse teste verifica navegação, criação, escrita, leitura, cópia, movimentação, permissões, remoção e blocos.

\---

## Integrantes

* Felipe Meira
* Arthur Costa de Avelar Ferreira

