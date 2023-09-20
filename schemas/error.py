from pydantic import BaseModel

class ProdutoErrSchema(BaseModel):
    """ Exibe mensagem de erro
    """
    mesage: str
    erro: str
