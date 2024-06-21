import os
import chardet
from bs4 import BeautifulSoup
import pandas as pd

pathPatentes = 'PATENTES'

dataPatente = []

def code(archive):
    with open(archive, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def getData(archive):
    encoding = code(archive)

    with open(archive, 'r', encoding=encoding) as file:
        soup = BeautifulSoup(file, 'html.parser')

        archiveName = os.path.basename(archive)

        cnpj = 'NENHUM ITEM ENCONTRADO'
        cnpjTag = soup.find('div', id='tituloEResumoContext')
        if cnpjTag:
            cnpjFont = cnpjTag.find('font', class_='normal')
            if cnpjFont and 'CPF ou CNPJ do Depositante:' in cnpjFont.get_text(strip=True):
                cnpjText = cnpjFont.get_text(strip=True)
                cnpj = cnpjText.split(': ')[1].strip()

        resultado = 0
        resultadoTag = soup.find('font', class_='normal')
        if resultadoTag:
            text = resultadoTag.get_text(strip=True)
            if 'Foram encontrados' in text:
                i = text.index('Foram encontrados') + len('Foram encontrados')
                iFim = text.index('processos')
                resultadoText = text[i:iFim].strip()
                resultado = int(resultadoText) if resultadoText.isdigit() else 0

        dataPatente.append([archiveName, cnpj, resultado])

for archive in os.listdir(pathPatentes):
    if archive.endswith('.html'):
        pathArchive = os.path.join(pathPatentes, archive)
        getData(pathArchive)

columns = ['Arquivo', 'CNPJ', 'RESULTADO']
df = pd.DataFrame(dataPatente, columns=columns)

df.to_html('PATENTES.HTML', index=False, justify='center')

print("DADOS COLETADOS")
