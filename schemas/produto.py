from pydantic import BaseModel
from typing import List

class Produto():
    """ Define classe produto: produto .
    """
    imagem = 'https://a-static.mlcdn.com.br/400x600/livro-harry-potter-e-o-prisioneiro-de-azkaban-j-k-rowling/magazineluiza/223261100/744b73287326f6d9f16f79b0c37273cb.jpg'
    nome = 'Harry Potter e o prisioneiro de azkaban'
    autor = 'J.K. Rowling'
    descricao = 'Harry Potter e seus amigos retornam para lutar contra bruxos das trevas em seu terceiro ano em Hogwarts'
    valor = 32.99
    estoque = 17

    def __init__(self, imagem, nome, autor, descricao, valor, estoque):
        self.imagem = imagem
        self.nome = nome
        self.autor = autor
        self.descricao = descricao
        self.valor = valor
        self.estoque = estoque

    def __str__(self):
        return f"Produto: {self.nome}, Autor: {self.autor}, Descricao: {self.descricao}, Valor: {self.valor}, Estoque: {self.estoque}"

