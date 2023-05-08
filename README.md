# API pública dos Correios

Programa simples para retornar os dados da API pública dos Correios.

## Instalação

Clone este repositório:

```shell
$ git clone https://github.com/enzo-santos/publicapi-correios.git
$ cd publicapi-correios
```

Opcionalmente, ative um ambiente virtual:

```shell
$ python -m venv <nome-ambiente>
$ <nome-ambiente>\Scripts\activate
```

Instale as dependências:

```shell
$ python -m pip install -r requirements.txt
```

## Uso

Execute o arquivo *main.py* com o código de rastreamento a ser consultado:

```shell
$ python main.py AB123456789BR
```

Alternativamente, para evitar inserir o código toda vez ou evitar persistir o código no histórico
do prompt de comando, crie um arquivo no diretório raiz deste projeto com o nome *.env* e adicione
o código de rastreamento a ser consultado:

```dotenv
CODIGO_RASTREAMENTO=AB123456789BR
```

```shell
$ python main.py
```

O arquivo *.env* basicamente introduz de forma temporária as variáveis declaradas nele nas 
variáveis de ambiente do sistema. Então caso você prefira adicionar uma variável de ambiente
ao invés de um arquivo *.env*, o script funcionará da mesma maneira.

O código primeiro será lido do argumento do script e depois, caso não exista, do arquivo *.env*
ou das variáveis de ambiente.

Note que o script falhará se

- nenhum código de rastreamento for fornecido, seja pelo argumento do script, pelo arquivo *.env* ou
pelas variáveis de ambiente

```shell
$ python main.py
[!] Erro: Nenhum código de rastreamento encontrado
```

- mais de um código de rastreamento for fornecido pelo argumento do script

```shell
$ python main.py AB123456789BR CD987654321BR
[!] Erro: Esperei 1 argumento, mas recebi 2
```

- um código de rastramento inválido for fornecido

```shell
$ python main.py ABCDEF
[!] Erro: Código de rastreamento inválido (ABCDEF)
```

Ao ser executado corretamente, o código exibirá uma imagem com um captcha a ser solucionado:

```shell
$ python main.py AB123456789BR
[?] Digite o captcha exibido:
```

Caso o captcha seja inserido incorretamente, uma mensagem de erro aparecerá:

```shell
$ python -m main.py
[?] Digite o captcha exibido: ABCDEF
[!] Erro: O captcha inserido está incorreto
```

Caso o captcha seja inserido corretamente, dois arquivos serão salvos no diretório *outputs*:
*resultado.json* e *dataMaxima.json*, contendo as informações sobre o código solicitado fornecido:

```shell
$ python -m main.py
[?] Digite o captcha exibido: VWXYZ
[#] Código obtido com sucesso
```

O arquivo *resultado.json* contém informações como a modalidade de envio e uma lista de eventos
representando o percurso do pacote pelos centros de distribuição.

O arquivo *dataMaxima.json* contém informações como o CEP de origem, o CEP de destino,
o prazo de entrega em dias, a data da postagem, a data máxima da entrega, a data do último
evento e uma descrição detalhada do último evento.
