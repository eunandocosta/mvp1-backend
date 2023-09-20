from flask import request, jsonify, redirect
from flask_openapi3 import OpenAPI, Info, Tag
from typing import List
from flask_cors import CORS

from sqlalchemy.exc import IntegrityError

from model.__init__ import *
from schemas.produto import Produto
from logger import logger

from pydantic import BaseModel

#schema para o Swagger
""""""

class ProdutoSchema(BaseModel):
    """ Define classe produto: produto .
    """
    imagem = 'https://a-static.mlcdn.com.br/400x600/livro-harry-potter-e-o-prisioneiro-de-azkaban-j-k-rowling/magazineluiza/223261100/744b73287326f6d9f16f79b0c37273cb.jpg'
    nome = 'Harry Potter e o prisioneiro de azkaban'
    autor = 'J.K. Rowling'
    descricao = 'Harry Potter e seus amigos retornam para lutar contra bruxos das trevas em seu terceiro ano em Hogwarts'
    valor = 32.99
    estoque = 17

class ProdutoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do produto.
    """
    nome: str = "Teste"

class ProdutoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_produtos(produtos: List[Produto]):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    result = []
    for produto in produtos:
        result.append({
            "imagem" : produto.imagem,
            "nome" : produto.nome,
            "autor" : produto.autor,
            "descricao" : produto.descricao,
            "valor" : produto.valor,
            "estoque" : produto.valor,
        })

    return {"produtos": result}

def apresenta_produto(produto: Produto):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    return {
        "imagem" : produto.imagem,
        "nome" : produto.nome,
        "autor" : produto.autor,
        "descricao" : produto.descricao,
        "valor" : produto.valor,
        "estoque" : produto.valor,
    }

""""""
info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)

#Configuração do banco de dados
database = './database/loja.db'

CORS(app, origins=['*'], methods=['GET', 'POST', 'DELETE', 'PATCH'])

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
produto_tag = Tag(name="Produto", description="Adição, visualização e remoção de produtos à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/swagger', tags=[produto_tag])
def insert(form: ProdutoSchema):
    """Insere um produto
    """
    try:
        produto = Produto(
            imagem = form.imagem,
            nome = form.nome,
            autor = form.autor,
            descricao = form.descricao,
            valor = form.valor,
            estoque = form.estoque
        )
        print(produto)
        logger.debug(f"Adicionando produto de nome: '{produto.nome}'")
        return apresenta_produto(produto), 200
    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Produto de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar produto '{produto.nome}', {error_msg}")
        return {"mesage": error_msg}, 409
    
@app.delete('/swagger', tags=[produto_tag])
def delete(query: ProdutoBuscaSchema):
    """Deleta um Produto a partir do nome de produto informado
    Retorna uma mensagem de confirmação da remoção.
    """
    try:
        lista = []
        produtos = produto_show()
        for produto in produtos:
            print(produto['nome'])
            lista.append(produto['nome'])
        if query.nome in lista:
            produto_delete(query.nome)
            return {"mesage": "Produto removido", "nome": query.nome}
    except Exception as e:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao deletar produto #'{produto}', {error_msg}")
        return {"mesage": error_msg}, 404
    
@app.get('/swagger', tags=[produto_tag])
def getter(query: ProdutoBuscaSchema):
    """Encontra um Produto a partir do nome de produto informado
    Retorna uma mensagem de confirmação da remoção.
    """
    logger.debug(f"Coletando produtos ")
    produtos = []

    try:
        lista = []
        produtos = produto_show()
        for produto in produtos:
            print(produto['nome'])
            lista.append(produto['nome'])
        if query.nome in lista:
            produto_delete(query.nome)
            return {"mesage": "Produto encontrado", "nome": query.nome}
    except Exception as e:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao encontrar produto #'{query.nome}', {error_msg}")
        return {"mesage": error_msg}, 408

# Insere itens na tabela produtos
@app.route('/produto/inserir', methods=['POST'])
def inserir_produto():
    """Insere itens na tabela produtos"""
    try:
        data = request.get_json()  # Recebe os dados do front-end
        novo_produto = Produto(data['imagem'], 
                               data['nome'], 
                               data['autor'], 
                               data['descricao'], 
                               data['valor'], 
                               data['estoque'])
        resultado = produto_insert(novo_produto)
        logger.debug(f"Inserindo produto {novo_produto.nome}")
        return jsonify({'message': 'Sucesso em inserir dados'}), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao inserir dados: {str(e)}'}), 500

#Exibe os itens da tabela produto
@app.route('/produto/exibir', methods=['GET'])
def exibir_produto():
    """Exibe os itens da tabela produto"""
    try:
        dados = produto_show()
        return jsonify({'dados': dados}), 202
    except Exception as e:
        return jsonify({'error': 'Erro ao mostrar dados: ' + str(e)}), 500

# Deleta itens da tabela produto
@app.route('/produto/deletar/<nome>', methods=['DELETE'])
def deletar_produto(nome):
    """Deleta itens da tabela produto"""
    try:
        app.logger.info(f"Tentando excluir produto {nome}")
        if produto_delete(nome) == True:
            app.logger.info(f"Produto {nome} excluído com sucesso")
            return jsonify({"message": f'Produto {nome} deletado com sucesso'}), 200
        else:
            return jsonify({"error": f"Produto {nome} não encontrado"}), 404
    except Exception as e:
        app.logger.error(f"Erro ao excluir produto {nome}: {str(e)}")
        return jsonify({"error": f"Erro ao excluir produto {nome}: {str(e)}"}), 500

    
# Altera a quantidade do estoque de um determinado item da tabela produto
@app.route('/produto/estoque/<nome>', methods=['PATCH'])
def atualizar_estoque(nome):
    """Altera a quantidade do estoque de um determinado item da tabela produto"""
    try:
        data = request.get_json()
        novoEstoque = data.get('novoEstoque')

        if novoEstoque is not None:
            if produto_patch(nome, novoEstoque):
                return jsonify({"message": f'Estoque do produto {nome} atualizado com sucesso'}), 200
            else:
                return jsonify({"error": f"Produto {nome} não encontrado"}), 404
        else:
            return jsonify({"error": "Parâmetro 'novoEstoque' ausente na solicitação"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)