# Conexão ao MongoDB Atlas com FastAPI e React
Nesse tutorial iremos falar sobre **criação, conexão, inserção e consulta** no banco de dados NoSQL **MongoDB Atlas**.

Escolhemos usar um banco de dados **não relacional** porque ele é mais simples de configurar, não exige o planejamento e a modelagem rígida de um banco SQL e, portanto, permite que a equipe concentre seus esforços na implementação do software.

Será utilizado um **Back-End em Python (FastAPI)** e um **Front-End em React**.

## O que é o MongoDB Atlas?

**MongoDB Atlas** é o serviço em nuvem oficial do MongoDB.

Ele oferece:
* Hospedagem gerenciada
* Backups automáticos
* Monitoramento e métricas
* Escalabilidade
* Conexões seguras via Internet

Em resumo, o Atlas elimina a dor de cabeça de instalar e configurar o MongoDB localmente.

## Criando o Cluster no MongoDB Atlas
### Passo 1 — Criar conta

1. Acesse: https://www.mongodb.com/cloud/atlas
2. Crie uma conta gratuita.

### Passo 2 — Criar um Projeto e o cluster

1. Após logar, clique em **“New Project”** e preencha as informações.
2. Clique em **“Create Cluster”**.
3. Escolha a opção **Free Tier (M0)**.
4. Escolha uma região próxima (por exemplo, AWS São Paulo).

### Passo 3 — Criar usuário e senha

1. Vá em **Database Access** → **Add New Database User**.
2. Escolha **Password Authentication**.
3. Defina **usuário** e **senha**.
4. Dê permissão de **Read and write**.
5. Clique em **Add User**.

### Passo 4 — Permitir IP de acesso
1. Vá em **Network Access** → **Add IP Address**.
2. Clique em Add Current IP Address (ou **adicione 0.0.0.0/0** para permitir qualquer IP — útil em desenvolvimento).
3. Salve.

### Passo 5 — Obter a URL de conexão

1. Vá em **Clusters** → **Connect** → **Connect your application**.
2. Copie a string de conexão, algo como: mongodb+srv://...
3. Guarde essa string em um arquivo **.env** - nunca a coloque diretamente no código.
4. Para usar `.env`, rode: `pip install python-dotenv.`

## Estrutura do Back-End
``` bash
app/
 ├── db.py
 ├── models.py
 ├── routers/
 │    └── users.py
 ├── main.py
 ├── .env
```

## Conectando o Atlas ao Back-End Python

### Passo 1 - Instalar dependência

No terminal do seu projet rode: `pip install pymongo`

### Passo 2 - Configurar variáveis de ambiente

**Arquivo** `.env`:

``` bash
MONGO_URI="mongodb+srv://..."
DB_NAME="db"
```
[!WARNING] Nunca suba este arquivo ao GitHub.

### Passo 3 - Conexão com o MongoDB Atlas

**Arquivo** `app/db.py`

``` python
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Lê a URI de conexão e o nome do banco
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB", "mydb")

# Cria o cliente que fará a conexão com o cluster do MongoDB Atlas
client = MongoClient(MONGO_URI)

# Escolher banco e coleção
db = client[DB_NAME]
```
MongoClient é a interface principal da biblioteca PyMongo, cada instância representa uma conexão ativa com o cluster. 

### Passo 4 - Criar os modelos de dados Pydantic

**Arquivo**: `app/models.py`
``` python
from pydantic import BaseModel
from typing import Optional
from bson import ObjectId

# Modelo que representa a estrutura dos documentos de usuário no MongoDB
class UserModel(BaseModel):
    id: Optional[str]
    username: str
    email: str
    hashed_password: str

    # Conversão para lidar com ObjectId do Mongo
    class Config:
        json_encoders = {ObjectId: str}
```
MongoDB usa `Objectd` como tipo de ID mas o `Pydantic` não entende esse tipo nativamente, então o encoder transforma em string JSON-friendly.

### Passo 5 - Criar rotas e algumas operações CRUD

**Arquivo** `app/routers/users.py`
``` python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from bson import ObjectId
from ..db import db
from ..models import UserModel

# Define a router da rota /users
router = APIRouter(prefix="/users")

# Modelo de entrada para criação de usuário (sem ID nem hash)
class CreateUser(BaseModel):
    username: str
    email: str
    password: str

# POST /users cria um novo usuário
@router.post("/", response_model=UserModel)
def create_user(user: CreateUser):
    # Verifica se já existe um usuário com o mesmo e-mail
    existing = db.users.fin_one({"email": user_email})
    if existing:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    
    # Monta o documento a ser salvo
    doc = {
        "username": user.username,
        "email": user.email,
        # Simula a hash da senha (em produção use bcrypt ou passlib)
        "hashed_password": "hashed-" + user.password
    }

    # Insere o documento no MongoDB
    result = db.users.insert_one(doc)

    # Recupera o documento recém-criado
    created = db.users.find_one({"_id": result.inserted_id})

    # Retorna o usuário criado no formato do modelo Pydantic
    return UserModel(
        id=str(created["_id"]),
        username=created["username"],
        email=created["email"],
        hashed_password=created["hashed-password"]
    )

# GET /users lista usuários com limite de resultados
@router.get("/", response_model=list[UserModel])
def list_users(limit: int = 10):
    # Busca todos os usuários
    users = list(db.users.find().limit(limit))

    # Converte cada ObjectId para string
    return [
        UserModel(
            id=str(u["_id"]),
            username=u["username"],
            email=u["email"],
            hashed_password=u["hashed_password"]
        )
        for u in users
    ]
    return users

# GET /users/{user_id} busca usuário pelo ID
@router.get("/{user_id}", response_model=UserModel)
def get_user(user_id: str):
    # Converte a string para ObjectId para consultar no MongoDB
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(404, "Usuário não encontrado")
    
    return UserModel(
        id=str(user["_id"]),
        username=user["username"],
        email=user["email"],
        hashed_password=user["hashed_password"]
    )
```
`db.users` acessa a coleção `users` dentro do banco definido em `db.py`, cada endpoint traduz as operações CRUD diretamente em comandos PyMongo (`find_one`, `insert_one`, `find`, etc). No contexto de um sistema com React por exemplo, o frontend chamará esses endpoints com axios ou fetch().

### Passo 6 - Inicializar o servidor FastAPI

**Arquivo**: `app/main.py`
``` python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users

# Cria a instância principal do FastAPI
app = FastAI(title="Exemplo MongoDB Atlas + FastAPI")

# Permite que o frontend acesse a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui o router de usuários
app.include_router(users.router)

# Endpoint simples de teste
@app.get("/")
def root():
    return {"message": "API conectada ao MongoDB Atlas."}
```

### Passo 7 - Rodar o servidor

`uvicorn app.main:app --reload`.

Acesse no navegador:

👉 http://localhost:8000/docs.

Essa é a **documentação interativa Swagger** gerada automaticamente pelo FastAPI.

## Conectando com o Front-End React

No seu projeto React, instale o **Axios**: `npm install axios`

**Arquivo:** `src/api/users.js`

``` javascript
import axios from "axios"
const API = "http://localhost:8000"

export const createUser = async (data) => {
    const res = await axios.post(`${API}/users/`, data)
    return res.data
}

export const getUsers = async () => {
    const res = await axios.get(`${API}/users`)
    return res.data
}
```
O frontend envia requisições HTTP (GET, POST, etc.) ao backend, o FastAPI recebe e roteia para a função correspondente. Nesse caso, a função acessa o MongoDB Atlas via PyMongo, o resultado é convertido em JSON e devolvido ao frontend (o front sempre espera um **JSON**).

## Boas Práticas
* **Não exponha credenciais**: use `.env`.
* **Hash real de senhas:** utilize `bcrypt` ou `passlib`.
* **Valide dados com Pydantic.**
* **Ative autenticação JWT** se for necessário controle de usuários