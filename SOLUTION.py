import os
import chardet
from bs4 import BeautifulSoup
import pandas as pd

pathPatentes = 'PATENTES'

dataPatente = []

def code(archive):
    with open(archive, 'rb') as f:
        result = chardet.detect(f.read())
        print('ARQUIVO CODIFICADO PARA LEITURA')
    return result['encoding']

def getData(archive):
    encoding = code(archive)

    with open(archive, 'r', encoding=encoding) as file:
        soup = BeautifulSoup(file, 'html.parser')

        archiveName = os.path.basename(archive)

        cnpjTag = soup.find(text='CNPJ:')
        cnpj = cnpjTag.find_next().get_text(strip=True) if cnpjTag else 'NENHUM ITEM ENCONTRADO'

        resultadoTag = soup.find(text='Resultado:')
        resultadoText = resultadoTag.find_next().get_text(strip=True) if resultadoTag else '0'
        resultado = int(resultadoText.split()[0]) if resultadoText.split()[0].isdigit() else 0

        if resultado == 0:
            dataPatente.append([archiveName, cnpj, resultado, '-', '-', '-', '-'])
        else:
            rowPatente = soup.find_all('tr', {'class': 'patente'})
            for row in rowPatente:
                numero_pedido = row.find('td', {'class': 'numero_pedido'}).get_text(strip=True)
                data_deposito = row.find('td', {'class': 'data_deposito'}).get_text(strip=True)
                titulo = row.find('td', {'class': 'titulo'}).get_text(strip=True)
                ipc = row.find('td', {'class': 'ipc'}).get_text(strip=True)
                dataPatente.append([archiveName, cnpj, resultado, numero_pedido, data_deposito, titulo, ipc])

for archive in os.listdir(pathPatentes):
    if archive.endswith('.html'):
        pathArchive = os.path.join(pathPatentes, archive)
        getData(pathArchive)

columns = ['Arquivo', 'CNPJ', 'RESULTADO', 'NÚMERO DO PEDIDO', 'Data do Depósito', 'Título', 'IPC']
df = pd.DataFrame(dataPatente, columns=columns)

df.to_html('PATENTES.HTML', index=False, justify='center')

print("DADOS EXTRAIDOS.")
