# UNO Online – Assíncrono

Este projeto acadêmico é desenvolvido na Universidade Federal do Pará (UFPA) com foco nos pilares da **Programação Orientada a Objetos (POO)**, demonstrando na prática os conceitos do paradigma através de um jogo de cartas multiplayer assíncrono.

## 🎓 Contexto Acadêmico

- **Instituição:** Universidade Federal do Pará (UFPA)
- **Instituto:** Instituto de Ciências Exatas e Naturais (ICEN)
- **Disciplina:** Paradigmas de Linguagem de Programação
- **Professor:** Lídio Campos
- **Equipe:**
  - **Felipe Lisboa Brasil** – [FelipeBrasill](https://github.com/FelipeBrasill)
  - **Alessandro Reali Lopes Silva** – [reali-705](https://github.com/reali-705)

## 📑 Sumário

- [Objetivos de Aprendizagem](#objetivos-de-aprendizagem)
- [O Projeto](#o-projeto)
- [Conceitos de POO Aplicados](#conceitos-de-poo-aplicados)
- [Tecnologias e Ferramentas](#tecnologias-e-ferramentas)
- [Documentação Técnica e Estrutura](#documentação-técnica-e-estrutura)

---

## Objetivos de Aprendizagem

Este projeto aplica na prática os fundamentos do **Paradigma Orientado a Objetos** através da modelagem de um jogo de cartas real, com ênfase em:

### Programação Orientada a Objetos (POO)

Compreender e aplicar os quatro pilares (abstração, herança, polimorfismo, encapsulamento) na modelagem das entidades do jogo. A POO permite criar uma hierarquia clara de classes — como `Carta`, `CartaComum` e `CartaAcao` — reutilizar lógica comum e manter o sistema extensível para novos tipos de cartas e efeitos.

### Separação de Responsabilidades (Layered Architecture)

O backend é organizado em camadas com responsabilidades distintas: **models** (entidades e regras do domínio), **services** (lógica de negócio e orquestração da partida), **routers** (interface HTTP) e **database** (persistência do estado). Esse padrão garante que mudanças em uma camada não propaguem efeitos colaterais nas demais.

### Modelagem de Domínio com UML

O design das classes foi guiado por um diagrama UML construído previamente, traduzindo relacionamentos como composição, agregação e herança diretamente para o código Python, tornando o diagrama um artefato vivo do projeto.

---

## O Projeto

O projeto é uma implementação didática do jogo **UNO** no formato multiplayer assíncrono — jogadores fazem suas jogadas em momentos diferentes, similar a um jogo de xadrez por correspondência. O estado da partida é persistido entre turnos, e cada jogador consulta o estado atual ao acessar o jogo.

A lógica é organizada em entidades bem definidas (cartas, baralho, mão, pilha de descarte, jogador e partida), com regras aplicadas de forma centralizada pela camada de serviço.

---

## Conceitos de POO Aplicados

### Abstração

`Carta` é uma classe abstrata que define o contrato comum (cor, identidade) sem ser instanciada diretamente. Toda carta no jogo é necessariamente uma `CartaComum` ou `CartaAcao`.

### Herança

Especialização progressiva: `Carta` → `CartaComum` / `CartaAcao`. `CartaComum` adiciona o atributo `numero`; `CartaAcao` adiciona `tipoEfeito` e o comportamento de efeito especial.

### Polimorfismo

A `Partida` pode operar sobre qualquer `Carta` de forma uniforme ao validar jogadas, e delega a aplicação de efeitos especificamente para `CartaAcao` via `aplicar_efeito_carta()`.

### Encapsulamento

Atributos críticos como `cartas` do `Baralho`, `mao` do `Jogador` e `turno` da `Partida` são privados e acessados apenas por métodos controlados, prevenindo manipulação direta do estado do jogo.

### Composição e Agregação

`Partida` compõe `Baralho` e `PilhaDescarte` (ciclo de vida dependente). `Jogador` compõe `Mao`. As cartas são gerenciadas pelas estruturas que as contêm em cada momento da partida.

---

## Tecnologias e Ferramentas

* **Linguagem (Backend):** Python 3.12+
* **Framework (Backend):** FastAPI
* **Persistência:** *A definir* (SQLite, PostgreSQL ou outra)
* **Linguagem (Frontend):** TypeScript
* **Framework (Frontend):** React
* **Bundler/Tooling:** Vite
* **Router:** React Router v7 (HashRouter)
* **Gerenciamento de Estado Global:** Zustand
* **Estilização (CSS):** TailwindCSS
* **Cliente HTTP:** Axios
* **Gerenciamento de Requisições HTTP:** Tanstack Query
* **Comunicação:** REST API assíncrona (HTTP + JSON)
* **Documentação da API:** OpenAPI + Swagger UI (gerados automaticamente pelo FastAPI)
* **Integração OpenAPI no Frontend:** Orval
* **Hospedagem (Frontend):** GitHub Pages
* **Hospedagem (Backend):** *A definir* (Heroku, Railway, Render ou outro)
* **Hospedagem (Banco de Dados):** *A definir* (Heroku, Railway, Render ou outro)

---

# Justificativa das Tecnologias Escolhidas

A stack tecnológica foi definida priorizando **facilidade de desenvolvimento, integração entre as ferramentas, curva de aprendizado e possibilidade de evolução futura**, buscando atender ao prazo do projeto sem comprometer a qualidade da arquitetura.

* **Python 3.12+:** *Felipe precisa escrever* (foi escolhido por ser uma linguagem madura, produtiva e amplamente utilizada no desenvolvimento de aplicações web e APIs.)

* **FastAPI:** *Felipe precisa escrever* (foi selecionado por sua performance, suporte a tipagem, documentação automática e facilidade de integração com Python.)

* **TypeScript:** foi escolhido para o frontend por fornecer tipagem estática, reduzindo erros durante o desenvolvimento e facilitando a manutenção do código.

* **React:** foi selecionado devido à sua arquitetura baseada em componentes, permitindo maior reutilização de código e organização da interface.

* **Vite:** será utilizado como ferramenta de build por oferecer inicialização rápida, compilação eficiente e configuração simples, acelerando o desenvolvimento.

* **React Router v7 (HashRouter):** será responsável pela navegação entre as telas da aplicação. A utilização do **HashRouter** garante compatibilidade com a hospedagem no GitHub Pages sem necessidade de configurações adicionais no servidor.

* **Zustand:** foi escolhido para o gerenciamento do estado global por possuir uma API simples, baixo volume de código e excelente integração com React e TypeScript.

* **Tailwind CSS:** foi adotado para agilizar o desenvolvimento da interface, permitindo criar layouts responsivos de forma rápida e consistente sem a necessidade de grandes arquivos CSS.

* **Axios:** será utilizado como cliente HTTP por oferecer uma API simples, suporte a interceptadores e boa integração com aplicações React.

* **TanStack Query:** ficará responsável pelo gerenciamento dos dados remotos, realizando cache automático, atualização de dados e controle de estados de carregamento e erro, reduzindo a necessidade de lógica manual.

* **OpenAPI + Swagger UI:**, gerados automaticamente pelo FastAPI, serão utilizados para documentar a API e manter uma especificação padronizada dos endpoints.

* **Orval:** será empregado para gerar automaticamente os tipos TypeScript e o cliente da API a partir da especificação OpenAPI, reduzindo código repetitivo e mantendo o frontend sincronizado com o backend.

* **GitHub Pages:** foi escolhido para hospedar o frontend por ser uma solução gratuita, simples de configurar e adequada para aplicações estáticas desenvolvidas com React.

Em conjunto, essas tecnologias formam uma stack moderna, amplamente utilizada pela comunidade e compatível entre si, oferecendo um bom equilíbrio entre produtividade, facilidade de manutenção e possibilidade de evolução do projeto.

---

## Riscos Técnicos e Estratégias de Mitigação

### 1. Hospedagem do Frontend (GitHub Pages)

**Risco:** O GitHub Pages hospeda apenas arquivos estáticos e possui limitações quanto ao uso de rotas.

**Impacto:** Utilizar o `BrowserRouter` poderia causar erros 404 ao acessar páginas diretamente.

**Mitigação:** Utilizar o `HashRouter` do React Router v7, garantindo compatibilidade com o GitHub Pages sem necessidade de configurações adicionais.

**Observações:** Caso o sistema evolua para uma hospedagem que suporte rotas, o `BrowserRouter` poderá ser adotado futuramente.

---
---

### 2. Comunicação entre Frontend e Backend

**Risco:** O frontend e o backend estarão hospedados em domínios diferentes.

**Impacto:** Requisições podem ser bloqueadas por políticas de CORS.

**Mitigação:** Configurar corretamente o middleware de CORS no FastAPI, permitindo acesso apenas aos domínios autorizados do frontend.

---
---

### 3. Alterações na API

**Risco:** Mudanças nos endpoints ou nos modelos de dados podem causar incompatibilidades com o frontend.

**Impacto:** Erros de compilação ou falhas durante a execução.

**Mitigação:** Utilizar o OpenAPI do FastAPI em conjunto com o Orval para regenerar automaticamente os tipos e clientes TypeScript sempre que a API for modificada.

---
---

### 4. Crescimento do Estado Global

**Risco:** Armazenar dados remotos e estado da interface no mesmo local pode dificultar a manutenção.

**Impacto:** Código mais complexo e maior chance de inconsistências.

**Mitigação:** Manter uma separação clara de responsabilidades:

* **Zustand:** estado global da aplicação (autenticação, configurações, estado da interface).
* **TanStack Query:** dados obtidos do servidor (salas, partidas, jogadores, ranking etc.).

---
---

### 5. Hospedagem do Backend e Banco de Dados

**Risco:** A plataforma de hospedagem ainda não foi definida.

**Impacto:** Algumas plataformas possuem limitações de recursos, armazenamento ou tempo de inatividade ("sleep"), o que pode afetar a disponibilidade da aplicação.

**Mitigação:** Avaliar as opções (Railway, Render, Heroku ou outras) considerando custos, disponibilidade, desempenho e suporte ao FastAPI antes da implantação definitiva.

---
---

### 6. Evolução para Comunicação em Tempo Real

**Risco:** A versão inicial utilizará apenas REST, o que pode exigir consultas periódicas para atualizar informações da partida.

**Impacto:** Pequeno atraso na sincronização entre os jogadores e aumento no número de requisições ao servidor.

**Mitigação:** A arquitetura foi planejada para permitir a futura adoção de WebSockets sem necessidade de substituir as tecnologias já escolhidas.

---
---

### 7. Dependência de Ferramentas Geradas

**Risco:** O código gerado pelo Orval pode ficar desatualizado em relação ao backend.

**Impacto:** Inconsistências entre o frontend e a API.

**Mitigação:** Sempre que houver alterações na especificação OpenAPI, regenerar os arquivos do Orval antes de iniciar novos desenvolvimentos ou gerar uma nova versão do sistema.

---
---

### Considerações

Os riscos identificados não impedem o desenvolvimento do projeto, mas representam pontos que exigem atenção durante sua evolução. As tecnologias selecionadas foram escolhidas de forma a minimizar esses riscos e permitir que a aplicação cresça de maneira organizada, com possibilidade de incorporar novas funcionalidades no futuro sem necessidade de mudanças significativas na arquitetura.


---

## Documentação Técnica e Estrutura

### Documentação

- **[Diagrama de Classes](docs/diagrams/class-diagram.md)** – Hierarquia de classes, atributos, métodos e relacionamentos (composição, agregação, herança)
- **[Diagrama de Arquitetura](docs/diagrams/architecture.md)** – Visão em camadas, fluxo de dados entre frontend, routers, services e models

### Mapa de Pacotes

```plaintext
uno/
├── docs/                                   # 📖 Documentação Técnica
│   └── diagrams/
│       ├── class-diagram.md                # Diagrama UML de classes
│       └── architecture.md                 # Arquitetura em camadas
│
├── backend/
│   ├── main.py                             # ⚙️ Entrypoint FastAPI
│   │
│   ├── models/                             # 🃏 Entidades do Domínio (POO)
│   │   ├── carta.py                        # Classe abstrata base
│   │   ├── carta_comum.py                  # Herda Carta – possui numero
│   │   ├── carta_acao.py                   # Herda Carta – possui tipoEfeito
│   │   ├── baralho.py                      # Pilha de cartas, embaralha e distribui
│   │   ├── mao.py                          # Cartas na mão do jogador
│   │   ├── pilha_descarte.py               # Cartas já jogadas
│   │   ├── jogador.py                      # Compra, joga, passa
│   │   └── partida.py                      # Orquestra turno, ordem e estado
│   │
│   ├── routers/                            # 🌐 Interface HTTP (Controllers)
│   │   ├── partida.py                      # POST /partida, GET /partida/{id}
│   │   └── jogada.py                       # POST /jogada, /comprar, /passar
│   │
│   ├── services/                           # 🧠 Lógica de Negócio
│   │   └── partida_service.py              # Valida jogadas, aplica efeitos, avança turno
│   │
│   └── database/                           # 💾 Persistência de Estado
│       └── db.py                           # Salva e carrega estado da partida
│
└── frontend/                               # 🎨 Interface do Jogador
    ├── index.html                          # Estrutura da página
    ├── style.css                           # Estilo visual
    └── js/
        ├── api.js                          # Chamadas fetch ao backend
        ├── ui.js                           # Renderização do estado do jogo
        └── game.js                         # Interação do jogador (clicar, jogar)
```

---

[⬆️ Voltar ao topo](#uno-online--assíncrono)