from jose import jwt, JWTError
from bcrypt import hashpw, checkpw, gensalt
from datetime import datetime, timezone, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

# Coloque ambos como variáveis de ambiente em um app real
CHAVE_SECRETA = "troque-esta-chave-secreta-por-algo-seguro"
ALGORITMO = "HS256"

# Ele olha o cabeçalho Authorization da requisição, verifica se ele começa com Bearer e extrai a string do token
oauth2 = OAuth2PasswordBearer(tokenUrl="token")

def gerar_hash(senha: str) -> bytes:
    """Gera um hash seguro para uma senha em texto plano."""
    return hashpw(senha.encode('utf-8'), gensalt())

def verificar_senha(senha: str, senha_hash: bytes) -> bool:
    """Verifica se uma senha em texto plano corresponde a um hash salvo."""
    return checkpw(senha.encode('utf-8'), senha_hash)

def criar_token(username: str):
    """Cria um novo token de acesso JWT."""
    payload = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    token = jwt.encode(payload, CHAVE_SECRETA, algorithm=ALGORITMO)
    return token

def verificar_token(token: str = Depends(oauth2)):
    """
    Uma dependência do FastAPI para verificar o token JWT.
    Extrai o token do cabeçalho "Authorization: Bearer <token>"
    e retorna o username (sub) se o token for válido.
    """
    try:
        payload = jwt.decode(token, CHAVE_SECRETA, algorithms=[ALGORITMO])
        nome = payload.get("sub")
        if not nome:
            raise HTTPException(status_code=401, detail="Token inválido")
        return nome
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")