# Davi Villalva @ 2020

import mysql.connector
import json
from json import JSONDecodeError
import copy

# modifica objetos json em um banco de dados MySQL usando uma função
# que processa a modificação.
def modifica_objetos_json(
    bd,
    tabela,
    coluna_id,
    coluna_json,
    colunas_adicionais,
    processador,
    tamanho_pagina=10,
    max_paginas=1024
):
    cursor = bd.cursor()
    colunas = [coluna_id, coluna_json, *colunas_adicionais] 

    for pagina in range(0, max_paginas):
        linhas_modificadas = {}
        cursor.execute(f'SELECT {",".join(colunas)} FROM {tabela} LIMIT {pagina * tamanho_pagina}, {tamanho_pagina}')

        contagem_anterior = len(linhas_modificadas)
        nao_modificados = 0

        for linha in cursor:
            o_id, o_json_str = linha[:2]
            adicionais = linha[2:]

            try:
                o_json = json.loads(o_json_str)
                o_json_novo = processador(o_id, copy.deepcopy(o_json), *adicionais)

                if o_json != o_json_novo:
                    linhas_modificadas[o_id] = o_json_novo
                else:
                    nao_modificados += 1
            except JSONDecodeError:
                nao_modificados += 1
            
        linhas_processadas = len(linhas_modificadas) - contagem_anterior + nao_modificados

        for id, o_json in linhas_modificadas.items():
            cursor.execute(f'UPDATE {tabela} SET {coluna_json} = \'{json.dumps(o_json, separators=(",", ":"))}\' WHERE id = {id}')

        print(f'página {pagina * tamanho_pagina}-{(pagina + 1) * tamanho_pagina} - {len(linhas_modificadas) - contagem_anterior} linha(s) modificada(s), {nao_modificados} não modificado(s). Total de {linhas_processadas} linha(s) processada(s)')

        if linhas_processadas < tamanho_pagina:
            break
    
    bd.commit()

# Teste
bd = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='test'
)

#                           id  coluna_json  coluna_adicional
def processador_objeto_json(id, objeto_json, coluna_adicional):
    # Adicionando uma propriedade no objeto JSON com o valor 300
    objeto_json['exemplo'] = 300
    return objeto_json

modifica_objetos_json(
    bd,
    tabela='exemplo',
    coluna_id='id',
    coluna_json='coluna_json',
    colunas_adicionais=['coluna_adicional'],
    processador=processador_objeto_json,
    tamanho_pagina=3,
    max_paginas=1,
)