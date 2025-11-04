from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from schemas import Token,UsuarioLogin
from authh import gerar_hash, verificar_senha, criar_token, verificar_token

app = FastAPI()

# Em um app real, isso viria de um banco de dados
usuarios = {
    "teste": {
        "email": "teste@gmail.com",
        "senha": gerar_hash("40028922") 
    }
}

@app.post("/token", response_model=Token)
def login(dados: UsuarioLogin):
    """
    Endpoint de login.
    Recebe 'nome' e 'senha' de um modelo pydantic UsuarioLogin.
    Valida as credenciais e retorna um token de acesso.
    """
    # Busca o usuário no nosso "banco de dados"
    usuario = usuarios.get(dados.nome)
    # Verifica se o usuário existe e se a senha está correta
    if not usuario or not verificar_senha(dados.senha, usuario.get("senha")):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")
    # Se as credenciais estiverem corretas, cria um token
    token = criar_token(dados.nome)
    # Retorna o token no formato personalizado 'Token'
    return {"access_token": token, "tipo": "bearer"}

# NOTA SOBRE AUTENTICAÇÃO NO /docs do FastAPI
#
# Como este endpoint de login espera um JSON (definido pelo Pydantic) e não o padrão de formulário, o botão global "Authorize" (cadeado) e não o padrão de formulário, o botão global "Authorize" (cadeado) no topo da página /docs NÃO FUNCIONARÁ.
# Você só poderá testar endpoints protegidos manualmente colando o token no cabeçalho da sua requisição
# Se quiser usar o botão global pesquise por "OAuth2PasswordRequestForm"
# No entanto, essa forma é menos flexível, pois requer um corpo de requisição específico (application/x-www-form-urlencoded), que é menos prático para front-ends modernos que preferem JSON.


@app.get("/usuario-logado")
def usuario_logado(nome: str = Depends(verificar_token)):
    """
    Endpoint protegido.
    Só pode ser acessado se um token 'Bearer' válido for
    enviado no cabeçalho 'Authorization'.
    
    A dependência 'verificar_token' faz todo o trabalho de validação.
    """
    # Se a função 'verificar_token' for bem-sucedida, 'nome' conterá
    # o username extraído do token.
    return {"nome_do_usuario": nome, "msg": "Token válido e usuário autenticado!"}