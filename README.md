<h1>Diary CLI</h1>

Gerenciador criptográfico de arquivos de texto de interface shell.

---

<h2>Índice</h2>

- [Descrição](#descrição)
- [Dependências](#dependências)
- [Instalação](#instalação)
  - [Instalação com Make](#instalação-com-make)
  - [Instalação manual](#instalação-manual)
- [Como usar](#como-usar)
- [Criptografia](#criptografia)
- [Como contribuir](#como-contribuir)


---

## Descrição

O Diary-CLI é um programa com interface em shell que permite o gerenciamento de arquivos de texto em um diretório rastreado configurável pelo usuário e seus subdiretórios. Sua principal finalidade é proporcionar a criptografia e descriptografia dos arquivos rastreados.

Com o Diary-CLI, você pode organizar seus arquivos de texto de forma segura, criptografando-os com senhas escolhidas por você. O programa utiliza um algoritmo de criptografia de chave simétrica, onde você pode fornecer uma ou mais senhas (separadas por espaços) para cada arquivo. Esse processo pode ser repetido várias vezes para o mesmo arquivo, mas a descriptografia deve seguir a mesma ordem de senhas utilizadas na criptografia. Além disso, as senhas podem ser combinadas com um salt alfanumérico, armazenado em um arquivo cuja localização é especificada nas configurações, para adicionar aleatoriedade e aumentar a segurança.

## Dependências

As únicas dependências necessárias para executar o Diary-CLI são:

- Python 3.8+

- Python Pip

- Python venv

O programa é multi-plataforma, podendo ser executado em ambientes Linux, MacOS e Windows.

## Instalação

Para criar um executável do Diary-CLI e torná-lo executável a partir de qualquer lugar em um ambiente Linux, siga as instruções abaixo em uma shell interativa:

1. Clone o repositório do Diary-CLI do GitHub:

```shell
git clone https://github.com/GabrielLins64/diary-cli
```

2. Navegue até o diretório do projeto.

```shell
cd diary-cli
```

3. Para manter o seu sistema limpo, a instalação utiliza ambientes virtuais Python, então instale o python-venv:

```shell
sudo apt-get install python3-venv
```

A partir daqui há 2 formas de instalar, a [instalação utilizando a ferramenta make](#instalação-com-make) (recomendada) ou a [instalação manual](#instalação-manual).

### Instalação com Make

1. Garanta que seu sistema possui a ferramenta [Make](https://www.gnu.org/software/make/).

**Atenção:** O programa irá pedir permissão de administrador durante a instalação para copiar o binário para `/usr/local/bin`, de forma a tornar o programa executável de qualquer lugar.

`sudo make install`: Para instalar o Diary-CLI. Após a instalação, o programa será executado de qualquer lugar com o comando `diarycli`.

`make build`: Para criar apenas o executável em `dist/main`.

`make clean`: Para limpar arquivos temporários e diretórios de build.

### Instalação manual

1. Crie um ambiente virtual e ative-o (recomendado mas opcional):

```shell
python -m venv venv
source venv/bin/activate
```

2. Instale as dependências com o Python Pip:

```shell
pip install -r requirements.txt
```

3. Agora crie o executável usando o Pyinstaller:

```shell
pyinstaller --onefile main.py
```

4. Finalmente, copie o executável gerado em `dist/main` para o diretório de binários locais:

```shell
sudo cp dist/main /usr/local/bin/diarycli
```

Agora você pode executar a aplicação de qualquer lugar usando o comando:

```shell
diarycli
```

## Como usar

O Diary-CLI possui uma interface interativa que permite ao usuário:

1. Buscar diretórios/arquivos.

2. Navegar pelo diretório rastreado pelo programa.

3. Configurar algumas opções, como:
   
   - Armazenamento (onde os subdiretórios e arquivos rastreados serão armazenados).

   - Editor padrão (para visualizar/editar os arquivos).

   - Arquivo de salt (salt utilizado na criptografia).

4. Visualizar ajuda por dentro da interface.

## Criptografia

O algoritmo de criptografia do Diary-CLI utiliza uma criptografia de chave simétrica. O usuário pode fornecer uma ou mais senhas para cada arquivo, separadas por espaços. Esse processo pode ser repetido mais de uma vez para o mesmo arquivo, mas é fundamental seguir a mesma ordem de senhas na descriptografia.

Além disso, as senhas podem ser combinadas com um salt alfanumérico, armazenado em um arquivo cuja localização é especificada nas configurações. Isso permite gerar hashes para adicionar aleatoriedade e evitar que pequenas mudanças nas senhas gerem saídas semelhantes.

O algoritmo é seguro e não é quebrável, mesmo pelo processo de força bruta, uma vez que pode ser gerada uma quantidade infinita de diferentes textos em linguagem natural a partir de combinações de senhas aleatórias.

**Importante:** É altamente recomendada a realização de um back-up de seus arquivos (ainda que criptografados), pois caso haja uma tentativa de quebra malsucedida por um invasor, o estado atual do arquivo criptografado será quase completamente irreversível, salvo se todo o processo de tentativa de quebra for realizado de forma inversa.

## Como contribuir

Se você deseja contribuir com o Diary-CLI, siga os passos abaixo:

1. Faça um fork do repositório oficial do Diary-CLI no GitHub clicando no botão "Fork" na parte superior direita da página do repositório.

2. Clone o repositório forkado para o seu computador:

```shell
git clone https://github.com/seu-usuario/diary-cli.git
```

3. Crie uma branch para realizar suas alterações:

```shell
cd diary-cli
git checkout -b minha-feature
```

4. Faça as alterações desejadas no código.

5. Commite suas alterações e envie-as para o GitHub:

```shell
git add .
git commit -m "Minha contribuição: descrição das alterações"
git push origin minha-feature
```

6. Abra um Pull Request no repositório oficial do Diary-CLI clicando no botão "Compare & pull request" na página do seu repositório forkado.

A equipe do Diary-CLI irá revisar suas alterações e, se tudo estiver correto, elas serão incorporadas ao projeto principal. Obrigado por contribuir!
