# Protegendo Páginas com JWT no React

Este guia mostra as formas **mais simples** de proteger páginas no **React** usando **JWT (JSON Web Token)**.
A ideia é impedir que um usuário acesse certas rotas se não estiver autenticado.

---

## Entendendo o contexto

O backend envia um **JWT** quando o usuário faz login. Esse token é a prova de que o usuário está autenticado.
No frontend (React), você precisa:

1. Armazenar o token (geralmente no `localStorage`).
2. Impedir o acesso às páginas privadas quando o token não existir ou for inválido.

Proteção usando Contexto Global (React Context)

### Exemplo de implementação:

```jsx
// src/AuthContext.jsx
import { createContext, useContext, useState } from "react";

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("token"));

  const login = (newToken) => {
    localStorage.setItem("token", newToken);
    setToken(newToken);
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  const isAuthenticated = !!token;

  return (
    <AuthContext.Provider value={{ token, isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
```

```jsx
// src/App.jsx
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./AuthContext";
import Login from "./Login";
import Dashboard from "./Dashboard";

function PrivateRoute({ children }) {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/login" />;
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
```

**Como funciona:**

Aqui está o seu texto formatado como um `README.md`.

-----

# README: Guia de Autenticação em React

Este guia descreve um sistema de autenticação em React usando Context API e React Router.

## `AuthContext.jsx`

O `AuthContext.jsx` é responsável por gerenciar o estado global de autenticação.

  * **`createContext()`**: Cria um contexto global para armazenar e compartilhar o estado de autenticação (token, login e logout) em toda a aplicação.

  * **`useState(localStorage.getItem("token"))`**: Inicializa o estado com o token salvo no navegador (caso o usuário já tenha feito login antes).

  * **`login(newToken)`**: Salva o token no `localStorage` e atualiza o estado do contexto.

      * *Isso garante que, mesmo ao recarregar a página, o usuário continue logado.*

  * **`logout()`**: Remove o token do `localStorage` e limpa o estado de autenticação.

  * **`isAuthenticated = !!token`**: Converte a string do `token` em um valor booleano (`true` se existir, `false` se não existir).

  * **`AuthContext.Provider`**: Disponibiliza as funções e o estado (`token`, `isAuthenticated`, `login`, `logout`) para qualquer componente dentro da aplicação.

  * **`useAuth()`**: É um *custom hook* que facilita o acesso ao contexto em qualquer componente:

    ```jsx
    const { login, logout, isAuthenticated } = useAuth();
    ```

## `App.jsx`

O `App.jsx` configura as rotas da aplicação e protege o conteúdo privado.

  * **`AuthProvider`**: Envolve toda a aplicação, permitindo que qualquer componente acesse o estado de autenticação global.
  * **`BrowserRouter` / `Routes` / `Route`**: Gerenciam as rotas do app com `react-router-dom`.
  * **`PrivateRoute`**: Componente que protege rotas privadas.
      * Ele usa `useAuth()` para verificar se o usuário está autenticado.
      * Se **sim**, renderiza o conteúdo (`children`).
      * Se **não**, redireciona o usuário para a tela de login (`<Navigate to="/login" />`).
  * **Rotas Públicas e Privadas**:
      * `/login`: Acesso livre.
      * `/dashboard`: Protegida, acessível apenas se `isAuthenticated` for verdadeiro.