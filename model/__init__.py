import sqlite3
from datetime import datetime
import os

def produto_create():
    try:
        db_path = './database'

        # Cria se o diretorio não existir
        os.makedirs(db_path, exist_ok=True)

        #Cria e direciona a base de dados para a pasta desejada
        db_path_join = os.path.join(db_path, 'loja.db')
        
        #Conecta a base de dados
        conexao = sqlite3.connect(db_path_join)
        cursor = conexao.cursor()
        
        #Cria a tabela na base de dados
        cursor.execute("""CREATE TABLE IF NOT EXISTS produtos(
                        imagem TEXT NOT NULL,
                        nome TEXT NOT NULL UNIQUE,
                        autor TEXT NOT NULL,
                        data_insercao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        descricao TEXT NOT NULL, 
                        valor FLOAT NOT NULL,
                        estoque INTEGER NOT NULL
        )""")
        
        conexao.commit()
        conexao.close()

        return True
    except Exception as e:
        return str(e) if e is not None else "Erro desconhecido"

def produto_insert(self):
    try:
        db_path_join = os.path.join('./database', 'loja.db')
        conexao = sqlite3.connect(db_path_join)
        cursor = conexao.cursor()
        date = datetime.now()
        cursor.execute("""INSERT INTO produtos(
                    imagem, nome, autor, data_insercao, descricao, valor, estoque
        ) VALUES (
                    ?,?,?,?,?,?,?
        )""", (self.imagem, self.nome, self.autor, date, self.descricao, self.valor, self.estoque))
        conexao.commit()
        conexao.close()
        return True
    except Exception as e:
        return 'Erro: '+str(e)
    
def produto_show():
    try:
        db_path_join = os.path.join('./database', 'loja.db')
        conexao = sqlite3.connect(db_path_join)
        cursor = conexao.cursor()
        # Execute uma consulta para obter os nomes das colunas
        cursor.execute("PRAGMA table_info(produtos)")
        nomes_colunas = [coluna[1] for coluna in cursor.fetchall()]
        # Selecione os dados que você precisa
        cursor.execute("SELECT * FROM produtos")
        dados = cursor.fetchall()
        resultado = [dict(zip(nomes_colunas, linha)) for linha in dados]
        conexao.close()
        return resultado
    except Exception as e:
        return 'Erro: ' + str(e)
    
def produto_delete(nome):
    try:
        db_path_join = os.path.join('./database', 'loja.db')
        conexao = sqlite3.connect(db_path_join)
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM produtos WHERE nome = ?", (nome,))
        conexao.commit()
        conexao.close()
        
        return True # Indica que a exclusão foi bem-sucedida
    except Exception as e:
        return False  # Indica que ocorreu um erro durante a exclusão
    
def __str__(self):
    return f"Nome: {self.nome}, Autor: {self.autor}, Data de Inserção: {self.data_insercao}, Valor: {self.valor}, Descrição: {self.descricao}"

def produto_patch(nome, novo_estoque):
    try:
        db_path_join = os.path.join('./database', 'loja.db')
        conexao = sqlite3.connect(db_path_join)
        cursor = conexao.cursor()
        consulta_sql = "UPDATE produtos SET estoque = ? WHERE nome = ?"
        cursor.execute(consulta_sql, (novo_estoque, nome))
        conexao.commit()
        conexao.close()
        return True
    except Exception as e:
        return False

produto_create()
