from schemas.produto import Produto
from typing import List

def apresenta_produto(produto: Produto):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    return {
        "imagem": produto.imagem,
        "nome": produto.nome,
        "autor": produto.autor,
        "descricao": produto.descricao,
        "valor": produto.valor,
        "estoque": produto.estoque
    }

def apresenta_produtos(produtos: List[Produto]):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    result = []
    for produto in produtos:
        result.append({
            "imagem": produto.imagem,
            "nome": produto.nome,
            "autor": produto.autor,
            "descricao": produto.descricao,
            "valor": produto.valor,
            "estoque": produto.estoque
        })

    return {"produtos": result}