import pymysql
import math

from app import db_host, db_username, db_password, db_name

db = pymysql.connect(host=db_host, user=db_username, password=db_password, database=db_name)
c = db.cursor(pymysql.cursors.DictCursor)

def resultados(pagina):
    tamanho = 5
    inicio = (pagina - 1) * tamanho
    query = "SELECT COUNT(*) FROM vagas"
    c.execute(query)
    total_dados = c.fetchall()[0]['COUNT(*)']
    total_paginas = math.ceil(total_dados / tamanho) 

    query = f'SELECT * FROM vagas \
            LIMIT {inicio}, {tamanho}'
    c.execute(query)
    vagas = c.fetchall()
        
    return Paginacao(pagina, total_paginas, vagas)

class Paginacao:

    def __init__(self, pagina, total_paginas, vagas):
        self.pagina = pagina
        self.total_paginas = total_paginas
        self.vagas = vagas

        for vaga in vagas:
            vaga['salario'] = f'R$ {vaga["salario"]:.2f}'.replace('.', ',')
            if len(vaga['salario']) == 10:
                vaga['salario'] = f'{vaga["salario"][0:4]}.{vaga["salario"][4:-3]}'
            else:
                vaga['salario'] = f'{vaga["salario"][0:5]}.{vaga["salario"][5:-3]}'


def vagas_usuario(pagina, id):
    tamanho = 5
    inicio = (pagina - 1) * tamanho
    query = f"SELECT COUNT(*) FROM inscricoes WHERE id_usuario = {id}"
    c.execute(query)
    total_dados = c.fetchall()[0]['COUNT(*)']
    total_paginas = math.ceil(total_dados / tamanho) 

    query = f'SELECT V.nome, V.localidade, V.salario, V.responsabilidades \
            FROM inscricoes I INNER JOIN usuarios U ON I.id_usuario = U.id \
            INNER JOIN vagas V ON I.id_vaga = V.id \
            WHERE U.id = {id} \
            LIMIT {inicio}, {tamanho}'
    
    c.execute(query)
    vagas = c.fetchall()
    
    return Paginacao(pagina, total_paginas, vagas)


