"""Constants file
"""

TEXT_HELP_PTBR = \
"""[Descrição]
Este é um programa de gerenciamento e armazenamento de textos. Ao salvar qualquer texto, o mesmo será automaticamente criptografado utilizando uma chave secreta (ver a seção [Criptografia]). Ao tentar abrir o texto salvo por fora do programa, ou mesmo por dentro inserindo uma chave diferente, o conteúdo estará ilegível.

[Configurações]
A aplicação pode ser configurada nos seguintes aspectos: 
- Armazenamento: onde os diretórios e arquivos rastreados pelo programa são armazenados.
- Editor padrão: o editor padrão utilizado para editar um arquivo.
- Script de sincronização: o script utilizado para sincronizar os dados em núvem.
As configurações podem ser editadas logo no menu principal, acessando a opção \"Configurações\" e aceitam a utilização de variáveis de ambientes como, por exemplo, \"$HOME/meu/caminho/de/configuração\".

[Armazenamento]
Todos os textos são armazenados no diretório configurado em \"Configurações > Armazenamento\". Eles podem ser organizados em subdiretórios que podem ser navegados por dentro da aplicação.

[Edição]
A edição de textos é feita utilizando o editor configurado em \"Configurações > Editor\". O editor padrão é o \"vi\".

[Criptografia]
A criptografia utilizada é um algoritmo de criptografia de chave simétrica, onde só há um tipo de chave mantida pelo usuário, que é passada por uma função de hash e, então, combinada com o texto para sua encriptação. O processo de decriptografia do texto requer a mesma chave combinada com o texto criptografado.

[Sincronização com a Nuvem]
O programa também permite o encaixe de um script para a sincronização da estrutura de textos/subdiretórios com alguma plataforma na nuvem. Por padrão um script de sincronização com o GitHub é fornecido e deve ser configurado com as devidas variáveis de ambiente. O script padrão é executado fazendo, nesta ordem, um pull e um push para o repositório configurado. O script de sincronização pode ser trocado em \"Configurações > Script de sincronização\". A sincronização pode ser ativada no menu principal ao escolher \"Sincronizar\".

"""