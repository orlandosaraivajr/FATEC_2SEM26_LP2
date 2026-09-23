import wget
import pandas as pd

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSPxryxjiyOz0bW5AIaB45RrgU-mp9O-bCFWWa9NIsu8f-80FZEz-dUKIR6fZ9qeGBW83clfV3-L_zF/pub?output=xlsx"
filename = wget.download(url)

df = pd.read_excel(filename, index_col=0)
df_filtrado = df[df['Curso'].str.contains('Multiplataforma', case=False, na=False)]

df_filtrado = df[
    df.iloc[:, 1].str.contains('Multiplataforma', case=False, na=False) &  # Buscar curso DSM
    df.iloc[:, 4].str.contains('Indeterminado', case=False, na=False)  # Buscar Indeterminados
]

print(f"\n\n CURSO DSM com editais indeterminados")
print( 40 * "*")
for index, row in df_filtrado.iterrows():
    print(f" {index}, Fatec: {row['Fatec']} => {row['Disciplina']}")
