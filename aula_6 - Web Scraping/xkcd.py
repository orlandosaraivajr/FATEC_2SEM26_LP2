#! python3
# xkcd.py - Baixa todas as histórias em quadrinhos do XKCD.

import os
import sys

import bs4
import requests

URL_BASE = 'https://xkcd.com'
PASTA = 'xkcd'


def baixar_xkcd(limite=None):
    url = URL_BASE                      # começa pela página inicial
    os.makedirs(PASTA, exist_ok=True)   # salva as imagens em ./xkcd
    baixadas = 0

    while not url.endswith('#'):        # o "Prev" da primeira tirinha aponta para '#'
        if limite is not None and baixadas >= limite:
            break

        # Baixa a página.
        print(f'Baixando página {url}...')
        res = requests.get(url)
        if res.status_code == 404:
            # A tirinha 404 não existe (piada do autor): pula para a anterior.
            numero = int(url.rstrip('/').split('/')[-1])
            url = f'{URL_BASE}/{numero - 1}/'
            continue
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text, 'html.parser')

        # Encontra a URL da imagem da tirinha.
        imagem = soup.select('#comic img')
        if not imagem:
            print('Imagem não encontrada nesta página.')
        else:
            url_imagem = 'https:' + imagem[0].get('src')
            arquivo = os.path.join(PASTA, os.path.basename(url_imagem))

            if os.path.exists(arquivo):
                print(f'Imagem {arquivo} já existe, pulando.')
            else:
                # Baixa a imagem e salva em ./xkcd.
                print(f'Baixando imagem {url_imagem}...')
                res = requests.get(url_imagem)
                res.raise_for_status()
                with open(arquivo, 'wb') as f:
                    for bloco in res.iter_content(100000):
                        f.write(bloco)
            baixadas += 1

        # Pega a URL do botão "Prev".
        anterior = soup.select('a[rel="prev"]')[0]
        url = URL_BASE + anterior.get('href')

    print('Concluído.')


if __name__ == '__main__':
    # Opcional: python xkcd.py 10  -> baixa apenas as 10 tirinhas mais recentes
    limite = int(sys.argv[1]) if len(sys.argv) > 1 else None
    baixar_xkcd(limite)
