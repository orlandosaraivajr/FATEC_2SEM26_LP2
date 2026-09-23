import os
from html.parser import HTMLParser

import wget
import pandas as pd

url = "https://cgesg.cps.sp.gov.br/editais-cgesg/"
filename = "editais_cgesg.html"

colunas = [
    'Edital', 'Fatec', 'Curso', 'Disciplina', 'Area', 'Determinado',
    'Periodo', 'Abertura', 'Limite', 'Link Edital', 'Link Ficha', 'Link Tabela',
]


class TabelaEditais(HTMLParser):
    """Lê as células 'content-export' de cada linha da tabela de editais."""

    def __init__(self):
        super().__init__()
        self.linhas = []
        self.linha = None
        self.celula = None

    def handle_starttag(self, tag, attrs):
        classes = (dict(attrs).get('class') or '').split()
        if tag == 'tr':
            self.linha = []
        elif tag == 'td' and self.linha is not None and 'content-export' in classes:
            self.celula = ''

    def handle_data(self, data):
        if self.celula is not None:
            self.celula += data

    def handle_endtag(self, tag):
        if tag == 'td' and self.celula is not None:
            self.linha.append(self.celula.strip())
            self.celula = None
        elif tag == 'tr' and self.linha is not None:
            if len(self.linha) == len(colunas):
                self.linhas.append(self.linha)
            self.linha = None


if os.path.exists(filename):
    os.remove(filename)
wget.download(url, out=filename)

with open(filename, encoding='utf-8') as f:
    parser = TabelaEditais()
    parser.feed(f.read())

df = pd.DataFrame(parser.linhas, columns=colunas)

df_filtrado = df[
    df['Curso'].str.contains('Multiplataforma', case=False, na=False) &  # Buscar curso DSM
    df['Determinado'].str.contains('Indeterminado', case=False, na=False)  # Buscar Indeterminados
]

print(f"\n\n CURSO DSM com editais indeterminados")
print(40 * "*")
for index, row in df_filtrado.iterrows():
    print(f" {row['Edital']}, Fatec: {row['Fatec']} => {row['Disciplina']} "
          f"(inscrições até {row['Limite']})")
