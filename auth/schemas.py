from pydantic import BaseModel

class UsuarioLogin(BaseModel):
    nome: str
    senha: str

class Token(BaseModel):
    access_token: str
    token_type: str