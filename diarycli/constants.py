"""Constants file
"""

TEXT_HELP_PTBR = \
"""[Descrição]
Este é um programa de gerenciamento e armazenamento de textos. Ao salvar qualquer texto, uma opção para criptografá-lo será mostrada utilizando uma senha (ver a seção [Criptografia]). Ao tentar abrir o texto encriptado por fora do programa, ou mesmo por dentro inserindo uma chave diferente, o conteúdo estará ilegível.

[Configurações]
A aplicação pode ser configurada nos seguintes aspectos: 
- Armazenamento: onde os diretórios e arquivos rastreados pelo programa são armazenados.
- Editor padrão: o editor padrão utilizado para editar um arquivo.
- Arquivo de salt: Onde o arquivo com o salt para as senhas será armazenado.
As configurações podem ser editadas logo no menu principal, acessando a opção \"Configurações\" e aceitam a utilização de variáveis de ambientes como, por exemplo, \"$HOME/meu/caminho/de/configuração\".

[Armazenamento]
Todos os textos são armazenados no diretório configurado em \"Configurações > Armazenamento\". Eles podem ser organizados em subdiretórios que podem ser navegados por dentro da aplicação.

[Edição]
A edição de textos é feita utilizando o editor configurado em \"Configurações > Editor\". O editor padrão é o \"vi\".

[Criptografia]
Para criptografar um texto, utilize a letra indicada no programa durante a seleção de arquivos. O mesmo procedimento é feito para decriptografar (que só é mostrado em arquivos com a extensão .enc). A criptografia utilizada é um algoritmo de criptografia de chave simétrica, onde só há um tipo de chave mantida pelo usuário, que é combinada opcionalmente com um salt, passada por uma função de hash e, então, combinada com o texto para sua encriptação. O processo de decriptografia do texto requer a mesma chave combinada com o texto criptografado. Além disso, a criptografia pode utilizar um salt (configurável em \"Configurações > Arquivo de salt\"). É válido lembrar que se um arquivo foi salvo com um salt, é necessário exatamente o mesmo salt para decriptografar o arquivo, ainda que as senhas coincidam. Por isso, nunca perca o arquivo de salt, se usar.
"""