import os
import re
import sys
import json
import tempfile
import urllib.parse
import urllib.request
import http.cookiejar

import dotenv


def _read_json(url, params=None):
    url = f'{url}?{urllib.parse.urlencode(params)}'
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    data = json.loads(response.read().decode('utf-8'))
    return data


def main():
    dotenv.load_dotenv()

    args = sys.argv[1:]
    CODIGO_RASTREAMENTO = os.getenv('CODIGO_RASTREAMENTO')

    if len(args) > 1:
        print(f'[!] Erro: Esperei 1 argumento, mas recebi {len(args)}')
        exit(1)

    codigo_rastreamento = None
    if len(args) == 1:
        codigo_rastreamento = args[0]
    elif CODIGO_RASTREAMENTO is not None:
        codigo_rastreamento = CODIGO_RASTREAMENTO
    else:
        print(f'[!] Erro: Nenhum código de rastreamento encontrado')
        exit()

    codigo_rastreamento = codigo_rastreamento.strip()
    if not re.match(r'[A-Z]{2}[0-9]{9}BR', codigo_rastreamento):
        print(f'[!] Erro: Código de rastreamento inválido ({codigo_rastreamento})')
        exit(1)

    # Define uma sessão HTTP
    cookie_jar = http.cookiejar.CookieJar()
    cookie_processor = urllib.request.HTTPCookieProcessor(cookie_jar)
    opener = urllib.request.build_opener(cookie_processor)
    urllib.request.install_opener(opener)

    # Carrega o captcha para ser utilizado
    request = urllib.request.Request('https://rastreamento.correios.com.br/core/securimage/securimage_show.php')
    response = urllib.request.urlopen(request)
    
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        f.write(response.read())

    try:
        os.startfile(f.name)
        valor_captcha = input('[?] Digite o captcha exibido: ').strip()

    finally:
        os.remove(f.name)

    # Utiliza o valor do captcha na requisição do primeiro resultado
    data = _read_json(
        'https://rastreamento.correios.com.br/app/resultado.php',
        {'objeto': codigo_rastreamento, 'captcha': valor_captcha, 'mqs': 'S'},
    )

    if data.get('erro', 'false') == 'true':
        print('[!] Erro: O captcha inserido está incorreto')
        exit(1)

    output_dir = os.path.join('outputs', codigo_rastreamento)
    try:
        os.makedirs(output_dir)
    except FileExistsError:
        pass

    with open(os.path.join(output_dir, 'resultado.json'), 'w+', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Utiliza o valor do finalizador mais recente na requisição do segundo resultado
    dados_eventos = data.get('eventos')
    if dados_eventos:
        tipo_postal = dados_eventos[0].get('finalizador')
        if tipo_postal:
            data = _read_json(
                'https://rastreamento.correios.com.br/app/dataMaxima.php',
                {'objeto': codigo_rastreamento, 'tipoPostal': tipo_postal},
            )
            with open(os.path.join(output_dir, 'dataMaxima.json'), 'w+', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

    print('[#] Código obtido com sucesso')

main()