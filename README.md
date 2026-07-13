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
  - **Gian Victor Gonçalves Figueiredo** - [Gian-Figueiredo](https://github.com/Gian-Figueiredo)

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

# Justificativa das Tecnologias Escolhidas

A stack tecnológica foi definida priorizando **facilidade de desenvolvimento, integração entre as ferramentas, curva de aprendizado e possibilidade de evolução futura**, buscando atender ao prazo do projeto sem comprometer a qualidade da arquitetura.

* **Python 3.12+:** *Felipe precisa escrever* (foi escolhido por ser uma linguagem madura, produtiva e amplamente utilizada no desenvolvimento de aplicações web e APIs.)

* **PyWebView:** Facilidade na integração do python com o React.

* **TypeScript:** foi escolhido para o frontend por fornecer tipagem estática, reduzindo erros durante o desenvolvimento e facilitando a manutenção do código.

* **React:** foi selecionado devido à sua arquitetura baseada em componentes, permitindo maior reutilização de código e organização da interface.

* **Vite:** será utilizado como ferramenta de build por oferecer inicialização rápida, compilação eficiente e configuração simples, acelerando o desenvolvimento.

* **React Router v7 (HashRouter):** será responsável pela navegação entre as telas da aplicação. A utilização do **HashRouter** garante compatibilidade com a hospedagem no GitHub Pages sem necessidade de configurações adicionais no servidor.

* **Tailwind CSS:** foi adotado para agilizar o desenvolvimento da interface, permitindo criar layouts responsivos de forma rápida e consistente sem a necessidade de grandes arquivos CSS.

Em conjunto, essas tecnologias formam uma stack moderna, amplamente utilizada pela comunidade e compatível entre si, oferecendo um bom equilíbrio entre produtividade, facilidade de manutenção e possibilidade de evolução do projeto.
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
