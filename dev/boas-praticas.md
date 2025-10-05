# Boas Práticas Essenciais de Desenvolvimento de Software em Equipe

Para garantir um processo de desenvolvimento coeso, eficiente e de alta qualidade, a adoção de padrões claros para versionamento de código e revisão é fundamental.

## Observações :

- Este tutorial visa ensinar um fluxo de boas práticas de desenvolvimento utilizando ferramentas de versionamento de código (Git/Github/Gitlab...).

- Note que nem sempre será possível seguir à risca todas as práticas descritas neste tutorial, mas esse é um modelo a ser seguido e que deixará o desenvolvimento da aplicação muito mais organizado.

## 1. Estratégia de Branching (Fluxo de Trabalho com Git)

Adotaremos uma versão simplificada do **Git Flow**, onde a branch principal para o desenvolvimento ativo é a develop.

### A Branch Principal de Desenvolvimento: develop

- A branch develop é a principal para a integração do trabalho de todos os desenvolvedores.

- Ela deve conter o código mais recente, estável o suficiente para ser testado e preparado para futuras liberações. Nunca desenvolva diretamente nesta branch.

### Branches de Trabalho (feature e fix)

Cada desenvolvedor deve isolar seu trabalho em uma **nova branch** criada a partir da develop para cada **funcionalidade (feature)** ou **correção (fix)** que for realizar.

### Padrão de Nomenclatura das Branches

Use o seguinte padrão de nomenclatura para que o propósito da branch seja claro e imediato:

- Para novas funcionalidades:
  `feature/titulo-da-feature`
  `(Exemplo: feature/adicionar-endpoint-de-login)`

- Para correções de bugs ou falhas:
  `fix/descricao-da-correcao`
  `(Exemplo: fix/corrigir-validacao-de-email)`

## 2. Padrão de Mensagens de Commit: Conventional Commits

A clareza nas mensagens de commit é essencial para rastrear o histórico do projeto e automatizar tarefas. Seguiremos o padrão **Conventional Commits**.

Este padrão exige que cada mensagem de commit comece com um tipo que especifica a natureza da mudança.

| Tipo (Type) | Descrição |
| :--- | :--- |
| **feat** | Nova funcionalidade. |
| **fix** | Correção de um bug. |
| **chore** | Alterações em ferramentas de build, configurações, ou tarefas de manutenção. |
| **docs** | Alterações apenas na documentação. |
| **style** | Alterações de formatação, espaços, ponto e vírgula, sem mudança lógica. |
| **refactor** | Uma mudança de código que não corrige um bug nem adiciona uma funcionalidade. |
| **test** | Adição, correção ou refatoração de testes. |
| **perf** | Uma mudança de código que visa melhorar a performance. |

### Exemplo de uso

``` Bash
git commit -m "feat: adicionar validação de senha no formulário de cadastro"
git commit -m "chore: atualizar versão do pacote X para 2.0.1"
git commit -m "fix: impedir que o modal feche ao clicar fora"
```

(Se necessário, consulte a documentação completa sobre [Convetional Commits](https://medium.com/linkapi-solutions/conventional-commits-pattern-3778d1a1e657))

## 3. Fluxo de Trabalho e Pull Requests (PRs)

Ao finalizar o desenvolvimento em sua branch e garantir que o código esteja pronto para integração, você deve criar um Pull Request (PR) para a branch develop.

### Etapas Finais de Desenvolvimento

1. Adicionar e Comitar as Mudanças:

```Bash
git add .
git commit -m "feat: sua mensagem de commit seguindo o padrão"
```

2. Enviar a Branch para o Repositório Remoto:

```Bash
git push -u origin feature/nome-da-sua-branch
```

### Criação e Descrição do Pull Request

O Pull Request serve como a proposta formal para incorporar suas mudanças.

### Conteúdo da Descrição do PR

Embora o título da branch e os commits ajudem, a descrição do PR é o local para fornecer um resumo claro do trabalho realizado. **Liste os principais pontos em tópicos**:

``` Markdown
**O que foi feito**
- Implementação da rota POST /users para criação de novos usuários.
- Ajuste na estilização do componente de botão (Button.js).
- Correção de bug de exibição na lista de itens vazia.
```

**A clareza na descrição simplifica enormemente o processo de Code Review.**

## 4. Boas Práticas de Code Review

O Code Review é um momento crucial para garantir a qualidade, identificar falhas e compartilhar conhecimento. As revisões devem ser focadas e construtivas.

### Princípios Fundamentais para Revisores

- **Foque no Código, Não na Pessoa**: A crítica deve ser sempre sobre o código e as escolhas técnicas. Mantenha o tom profissional e respeitoso.

- **Clareza e Construtividade**: Seja objetivo. Se você apontar um problema, ofereça sugestões claras e explique por que sua abordagem sugerida é melhor (ex: melhor performance, maior legibilidade, aderência a padrões).

- **Entenda o Contexto da Issue**: **Antes de começar a revisão**, leia a descrição do Pull Request e o ticket (ou task), entendendo o problema que a mudança visa resolver ou a funcionalidade que implementa.

### Focos da Revisão

**1. Lógica e Requisitos:**

  - O código atende completamente aos requisitos da task?
  - Ele resolve o problema proposto sem introduzir novos bugs?
  - Há cenários de erro ou edge cases (casos de contorno) que não foram tratados?

**2. Legibilidade e Manutenibilidade:**

  - O código é fácil de entender para alguém que não o escreveu?
  - Ele está utilizando nomes de variáveis e funções claros e descritivos?
  - **Princípio DRY (Don't Repeat Yourself)**: Existe código duplicado que poderia ser abstraído ou reutilizado?

**3. Aderência a Padrões:**

  - O código segue os padrões de linter e formater estabelecidos pelo projeto?
  - As práticas de segurança foram respeitadas?

Ao seguir estas boas práticas, a equipe garantirá um histórico de código limpo, um processo de integração suave e um produto final de maior qualidade e mais fácil de manter.
