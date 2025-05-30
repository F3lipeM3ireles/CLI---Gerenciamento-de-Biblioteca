# Sistema de Gerenciamento de Biblioteca CLI

Felipe Meireles - RA 2012841

José Carlos Fujii - RA 1994006

João Vitor Alvez de Paula - RA 1993855

Este é um sistema de gerenciamento de biblioteca, feito em Python como uma aplicação de Interface de Linha de Comando (CLI). 
Ele permite o cadastro de livros e usuários, o empréstimo e devolução de livros, a visualização de itens cadastrados e um histórico das operações realizadas. 
O sistema também implementa uma funcionalidade de fila de reserva para livros indisponíveis.

## 📝 Sumário

* [Funcionalidades Principais](#-funcionalidades-principais)
* [Estruturas de Dados Utilizadas](#-estruturas-de-dados-utilizadas)
* [Funcionalidades Detalhadas (Módulos do Código)](#️-funcionalidades-detalhadas-módulos-do-código)
    * [`menu()`](#menu)
    * [`cadastrar_livro()`](#cadastrar_livro)
    * [`cadastrar_usuario()`](#cadastrar_usuario)
    * [`visualizar_cadastros()`](#visualizar_cadastros)
    * [`emprestar_livro()`](#emprestar_livro)
    * [`devolver_livro()`](#devolver_livro)
    * [`exibir_operacoes()`](#exibir_operacoes)
* [Como Executar](#-como-executar)
* [Dependências](#-dependências)
* [Dados Iniciais](#-dados-iniciais)
* [Possíveis Melhorias Futuras](#-possíveis-melhorias-futuras)
* [Autor](#-autor)

---

## ✨ Funcionalidades Principais

O sistema oferece as seguintes funcionalidades básicas:

* **Cadastro de Livros:** Permite adicionar novos livros ao para a biblioteca, informando título, autor, ano de publicação e gênero. Cada livro também possui um status de disponibilidade.
* **Cadastro de Usuários:** Permite registrar novos usuários no sistema com um ID único e nome.
* **Visualização de Cadastros:**
    * Lista todos os livros cadastrados, informando seus detalhes e se estão "Disponível" ou "Emprestado".
    * Lista todos os usuários registrados no sistema com seus respectivos IDs e nomes.
* **Empréstimo de Livros:**
    * Permite que um usuário registrado pegue um livro emprestado.
    * Verifica a disponibilidade do livro antes de efetuar o empréstimo.
    * Registra a data do empréstimo utilizando a data atual como default.
* **Reserva de Livros:**
    * Caso um livro desejado esteja atualmente emprestado, o usuário tem a opção de entrar em uma fila de reserva para esse livro.
    * A fila de reserva é gerenciada usando uma estrutura de dados `deque` (fila), garantindo que o primeiro usuário a reservar seja o primeiro a receber o livro quando ele for devolvido 
* **Devolução de Livros:**
    * Permite que um usuário devolva um livro que foi previamente emprestado.
    * Atualiza o status de disponibilidade do livro para "Disponível".
    * Após a devolução, se houver usuários na fila de reserva para o livro devolvido, o livro é automaticamente emprestado ao primeiro usuário da fila.
* **Histórico de Operações:**
    * Mantém um registro, semelhante a um log, de todas as ações realizadas no sistema, como cadastro de livros, cadastro de usuários, empréstimos, devoluções e reservas.
    * O histórico é armazenado em uma pilha (`pilha_operacoes`) e exibido em formato LIFO (Last-In, First-Out), mostrando as operações mais recentes primeiro.
* **Interface de Linha de Comando (CLI):** Todas as interações com o sistema são feitas através do console.

---

## 💾 Estruturas de Dados Utilizadas

O sistema utiliza diversas estruturas de dados para gerenciar as informações de forma eficiente:

* **`livros` (Dicionário):**
    * **Estrutura:** `{ "Título do Livro": ("Autor", Ano, "Gênero", Disponibilidade_Booleana) }`
    * **Chave:** Título do livro (string), que atua como identificador único.
    * **Valor:** Uma tupla contendo:
        * Nome do autor (string).
        * Ano de publicação (inteiro).
        * Gênero do livro (string).
        * Status de disponibilidade (booleano: `True` para disponível, `False` para emprestado).
    * **Justificativa:** Dicionários oferecem acesso rápido aos dados do livro pelo título. A tupla é usada para agrupar informações relacionadas a cada livro. A flag de disponibilidade é crucial para o controle de empréstimos.

* **`usuarios` (Dicionário):**
    * **Estrutura:** `{ ID_Usuario: "Nome do Usuário" }`
    * **Chave:** ID do usuário (inteiro), que é um identificador único.
    * **Valor:** Nome do usuário (string).
    * **Justificativa:** Similar aos livros, o ID do usuário permite acesso rápido às informações do usuário.

* **`emprestimos` (Lista de Tuplas):**
    * **Estrutura:** `[ (ID_Usuario, "Título do Livro", data_emprestimo), ... ]`
    * **Cada Tupla:** Contém o ID do usuário que pegou o livro emprestado, o título do livro e a data em que o empréstimo foi realizado.
    * **Justificativa:** Uma lista é adequada para armazenar o registro cronológico dos empréstimos ativos. A busca para devolução pode ser $O(n)$, mas para o escopo do projeto, é aceitável.

* **`reservas` (Dicionário de Deques):**
    * **Estrutura:** `{ "Título do Livro": deque([ID_Usuario1, ID_Usuario2, ...]), ... }`
    * **Chave:** Título do livro (string) que possui uma fila de reserva.
    * **Valor:** Um objeto `deque` contendo os IDs dos usuários que estão na fila de espera por aquele livro, na ordem em que realizaram a reserva.
    * **Justificativa:** Um dicionário mapeia cada livro que possui reservas para sua respectiva fila. A estrutura `deque` é ideal para implementar filas, pois oferece operações eficientes de `append` (para adicionar ao final, $O(1)$) e `popleft` (para remover do início, $O(1)$), garantindo a lógica FIFO para as reservas.

* **`pilha_operacoes` (Lista como Pilha):**
    * **Estrutura:** `[ "Descrição da Operação 1", "Descrição da Operação 2", ... ]`
    * **Elementos:** Strings normais que descrevem as operações realizadas no sistema (ex: "Cadastro de livro: 'Título'").
    * **Justificativa:** Uma lista Python pode ser usada como uma pilha (LIFO - Last-In, First-Out) utilizando o método `append` para adicionar elementos ao topo (equivalente a `push`) e iterando de forma reversa (`reversed()`) ou usando `pop()` para remover/acessar o elemento do topo. Isso permite registrar e visualizar o histórico de ações do sistema.

---

## ⚙️ Funcionalidades Detalhadas (Módulos do Código)

O código é organizado em várias funções para separar as responsabilidades e facilitar a manutenção:

### `menu()`
* **Descrição:** É a função principal que controla a navegação do usuário pelo sistema. Apresenta um menu numerado com todas as opções disponíveis.
* **Fluxo:**
    1.  Exibe um cabeçalho "===== Biblioteca CLI =====".
    2.  Lista as opções disponíveis:
        * 1 - Cadastrar livro
        * 2 - Cadastrar usuário
        * 3 - Visualizar cadastros
        * 4 - Emprestar livro
        * 5 - Devolver livro
        * 6 - Exibir histórico de operações
        * 7 - Sair
    3.  Solicita ao usuário que escolha uma opção.
    4.  Com base na entrada do usuário (convertida para string e com espaços removidos), chama a função correspondente (`cadastrar_livro()`, `cadastrar_usuario()`, etc.).
    5.  Se a opção for '7', exibe uma mensagem de despedida ("Adeus, vai pela sombra!") e encerra o loop, finalizando o programa.
    6.  Se a opção for inválida, exibe "Opção inválida. Tente novamente." e reapresenta o menu.
    7.  O menu continua em loop até que o usuário escolha a opção de sair.

### `cadastrar_livro()`
* **Descrição:** Responsável por coletar os dados de um novo livro e adicioná-lo ao dicionário `livros`.
* **Entradas do Usuário:** Título do livro, autor, ano de publicação e gênero.
* **Processo:**
    1.  Solicita o título do livro (com `.strip().capitalize()` para formatação).
    2.  Entra em um loop para solicitar autor, ano e gênero, esperando uma entrada no formato "autor, ano, genero".
    3.  Valida se a entrada contém exatamente 3 partes após o `split(',')`. Se não, exibe "Formato inválido." e continua no loop.
    4.  Tenta converter o ano para inteiro. Se `ValueError` ocorrer, exibe "Ano inválido." e continua.
    5.  Se todas as validações passarem, armazena os dados.
    6.  Adiciona o livro ao dicionário `livros` com o título como chave e uma tupla `(autor, ano, genero, True)` como valor (o `True` indica que o livro está inicialmente disponível).
    7.  Adiciona uma string formatada à `pilha_operacoes` registrando o cadastro (ex: "Cadastro de livro: 'O Pequeno Príncipe'").
    8.  Exibe uma mensagem de confirmação (ex: "Livro 'O Pequeno Príncipe' cadastrado com sucesso.").

### `cadastrar_usuario()`
* **Descrição:** Responsável por coletar os dados de um novo usuário e adicioná-lo ao dicionário `usuarios`.
* **Entradas do Usuário:** ID do usuário e nome do usuário.
* **Processo:**
    1.  Entra em um loop para solicitar o ID do novo usuário.
    2.  Tenta converter o ID para inteiro. Se `ValueError`, exibe "ID deve ser numérico." e continua.
    3.  Verifica se o ID já existe no dicionário `usuarios`. Se sim, exibe "ID já cadastrado!" e continua.
    4.  Se o ID for válido e único, sai do loop.
    5.  Solicita o nome do usuário (com `.strip().capitalize()`).
    6.  Adiciona o usuário ao dicionário `usuarios` com o ID como chave e o nome como valor.
    7.  Adiciona uma string formatada à `pilha_operacoes` (ex: "Cadastro de usuário: 10 - Maria Silva").
    8.  Exibe uma mensagem de confirmação (ex: "Usuário 'Maria Silva' cadastrado com sucesso (ID: 10).").

### `visualizar_cadastros()`
* **Descrição:** Permite ao usuário escolher entre listar os livros cadastrados ou os usuários cadastrados.
* **Processo:**
    1.  Entra em um loop apresentando as opções "1 - Livros" e "2 - Usuários".
    2.  Solicita a escolha do usuário.
    3.  **Se '1' (Livros):**
        * Imprime um cabeçalho "\n== Livros ==".
        * Itera sobre o dicionário `livros`. Para cada item:
            * Desempacota as informações (autor, ano, genero, disponivel).
            * Define a string `status` como "Disponível" se `disponivel` for `True`, caso contrário "Emprestado".
            * Imprime os detalhes do livro e seu status (ex: "- Harry Potter 1: JK Rowling, 1989, Fantasia -> Disponível").
        * Encerra o loop de visualização.
    4.  **Se '2' (Usuários):**
        * Imprime um cabeçalho "\n== Usuários ==".
        * Itera sobre o dicionário `usuarios`. Para cada item:
            * Imprime o ID e o nome do usuário (ex: "- 1: Pedro").
        * Encerra o loop de visualização.
    5.  Se a opção for inválida, exibe "Opção inválida. Escolha 1 ou 2." e continua no loop.

### `emprestar_livro()`
* **Descrição:** Gerencia o processo de empréstimo de um livro a um usuário, incluindo a opção de reserva se o livro estiver indisponível.
* **Entradas do Usuário:** ID do usuário e título do livro.
* **Processo:**
    1.  **Validação do Usuário:**
        * Loop para solicitar o ID do usuário.
        * Valida se o ID é numérico e se o usuário existe em `usuarios`. Continua no loop até um ID válido ser fornecido.
    2.  **Listagem de Livros Disponíveis:**
        * Cria uma lista `disponiveis` com os títulos dos livros onde `info[3]` (disponibilidade) é `True`.
        * Se não houver livros disponíveis, exibe "Não há livros disponíveis." e retorna.
        * Imprime um cabeçalho "\n== Livros disponíveis ==" e lista cada livro disponível com seus detalhes.
    3.  **Seleção do Livro:**
        * Loop para solicitar o título do livro.
        * Valida se o título do livro existe no dicionário `livros`. Continua no loop até um título válido ser fornecido.
    4.  **Processamento do Empréstimo/Reserva:**
        * Obtém os dados do livro (autor, ano, genero, disponivel).
        * **Se `disponivel` for `True`:**
            * Atualiza a entrada do livro em `livros`, mudando a disponibilidade para `False`.
            * Adiciona uma tupla `(usuario_id, titulo, date.today())` à lista `emprestimos`.
            * Registra a operação na `pilha_operacoes` (ex: "Empréstimo: usuário 1 -> '1984'").
            * Exibe mensagem de sucesso (ex: "Livro '1984' emprestado para Pedro.").
        * **Se `disponivel` for `False`:**
            * Exibe "Livro '[titulo]' indisponível.".
            * Pergunta ao usuário "Deseja reservar? (S/N)".
            * **Se 'S' (Sim):**
                * Usa `reservas.setdefault(titulo, deque())` para obter a fila de reserva para o livro (ou criar uma nova `deque` se não existir).
                * Adiciona `usuario_id` à fila de reserva com `.append()`.
                * Registra a operação na `pilha_operacoes` (ex: "Reserva: usuário 1 para '1984'").
                * Exibe mensagem de confirmação da reserva.

### `devolver_livro()`
* **Descrição:** Processa a devolução de um livro. Se houver reservas para o livro devolvido, automaticamente o empresta para o próximo usuário na fila.
* **Entradas do Usuário:** ID do usuário e título do livro.
* **Processo:**
    1.  **Validação do Usuário:**
        * Loop para solicitar o ID do usuário, validando se é numérico.
    2.  **Validação do Livro e Empréstimo:**
        * Loop para solicitar o título do livro a ser devolvido.
        * Verifica se existe algum empréstimo ativo para a combinação `(usuario_id, titulo)` na lista `emprestimos`. Se não, exibe "Empréstimo não encontrado." e continua no loop.
    3.  **Processamento da Devolução:**
        * Itera sobre a lista `emprestimos` com `enumerate` para encontrar o índice do empréstimo correspondente.
        * Quando encontrado:
            * Obtém os dados originais do livro (autor, ano, genero).
            * Atualiza a entrada do livro em `livros`, mudando a disponibilidade para `True`.
            * Remove o registro do empréstimo da lista `emprestimos` usando `emprestimos.pop(idx)`.
            * Registra a operação na `pilha_operacoes` (ex: "Devolução: usuário 1 -> '1984'").
            * Exibe mensagem de sucesso (ex: "Livro '1984' devolvido por Pedro.").
    4.  **Processamento da Fila de Reserva (se aplicável):**
        * Verifica se há reservas para o `titulo` devolvido usando `reservas.get(titulo)` (que retorna `None` ou uma `deque` vazia se não houver reservas, o que avalia para `False`).
        * **Se houver reservas:**
            * Obtém o ID do próximo usuário da fila usando `reservas[titulo].popleft()`.
            * Atualiza a entrada do livro em `livros`, mudando a disponibilidade para `False` (emprestado novamente).
            * Adiciona uma nova tupla de empréstimo `(prox_usuario_id, titulo, date.today())` à lista `emprestimos`.
            * Registra a operação na `pilha_operacoes` (ex: "Empréstimo automático: usuário 2 -> '1984'").
            * Exibe mensagem sobre o empréstimo automático (ex: "Livro '1984' agora emprestado automaticamente para usuário 2.").
        * A função então retorna, pois a devolução e possível empréstimo automático foram concluídos.

### `exibir_operacoes()`
* **Descrição:** Mostra o histórico de todas as operações significativas que foram registradas na `pilha_operacoes`.
* **Processo:**
    1.  Imprime um cabeçalho "\n== Pilha de operações (LIFO) ==".
    2.  Itera sobre a `pilha_operacoes` utilizando `reversed(pilha_operacoes)`. Isso garante que as operações sejam exibidas da mais recente para a mais antiga (comportamento LIFO).
    3.  Para cada `operacao` (string) na pilha, imprime-a formatada (ex: "- Cadastro de livro: 'Harry Potter 1'").

---

## 🚀 Como Executar

1.  **Pré-requisitos:** Certifique-se de ter o Python 3 instalado em seu sistema.
2.  **Salvar o Código:** Salve o conteúdo do script fornecido em um arquivo com a extensão `.py` (por exemplo, `biblioteca_cli.py` ou `trabalho2.py`).
3.  **Abrir Terminal/Prompt de Comando:**
    * No Windows: Abra o Prompt de Comando (cmd) ou PowerShell.
    * No macOS/Linux: Abra o Terminal.
4.  **Navegar até o Diretório:** Use o comando `cd` para navegar até o diretório (pasta) onde você salvou o arquivo `.py`.
    ```bash
    cd caminho/para/o/diretorio
    ```
5.  **Executar o Script:** Digite o seguinte comando e pressione Enter:
    ```bash
    python nome_do_arquivo.py
    ```
    (Substitua `nome_do_arquivo.py` pelo nome real do seu arquivo, ex: `python biblioteca_cli.py`)
6.  **Interagir com o Menu:** O menu principal da biblioteca será exibido no console. Siga as instruções na tela, digitando o número da opção desejada e pressionando Enter.

---

## 🔗 Dependências

O script utiliza os seguintes módulos da biblioteca padrão do Python:

* **`collections.deque`**: Utilizado para implementar a fila de reservas de livros de forma eficiente (operações de adicionar e remover do início/fim em tempo constante).
* **`datetime.date`**: Utilizado para registrar a data atual no momento em que um livro é emprestado.

Não são necessárias instalações de pacotes externos (via pip, por exemplo). Todas as dependências já vêm inclusas na instalação padrão do Python.

---

## 📊 Dados Iniciais

Para facilitar a demonstração e o teste inicial do sistema, alguns livros e usuários já vêm cadastrados diretamente no código:

* **Livros Pré-cadastrados:**
    * "Harry Potter 1" a "Harry Potter 6"
    * "O Senhor dos Anéis"
    * "1984"
    * "O Pequeno Príncipe"
    * "Dom Quixote"
    * "A Revolução dos Bichos"
    * Todos iniciam com status `True` (Disponível).

* **Usuários Pré-cadastrados:**
    * ID 1: "Pedro"
    * ID 2: "João"
    * ID 3: "Felipe"
    * ID 4: "Mariana"
    * ID 5: "Carlos"
    * ID 6: "Ana"
    * ID 7: "Lucas"

Esses dados iniciais permitem que o usuário comece a interagir com as funcionalidades de empréstimo e devolução imediatamente, sem a necessidade de cadastrar tudo do zero.

---

## 🔮 Possíveis Melhorias Futuras

Embora funcional, o sistema pode ser expandido com diversas melhorias:

* **Persistência de Dados:**
    * Salvar os dicionários `livros`, `usuarios` e as listas `emprestimos`, `reservas`, `pilha_operacoes` em arquivos (ex: JSON, CSV, Pickle ou um banco de dados simples como SQLite).
    * Carregar esses dados ao iniciar o programa, para que as informações não sejam perdidas ao fechar a aplicação.
* **Busca Avançada:**
    * Implementar funcionalidades de busca mais refinadas para livros (por autor, gênero, ano) e usuários (por parte do nome).
* **Edição e Exclusão de Registros:**
    * Permitir editar informações de livros e usuários já cadastrados.
    * Permitir excluir livros e usuários (com devidas validações, como não excluir livro emprestado ou usuário com empréstimos ativos).
* **Validação de Datas e Prazos:**
    * Implementar um sistema de data de devolução esperada para os empréstimos.
    * Notificar sobre livros atrasados ou calcular multas (simples).
* **Interface Gráfica do Usuário (GUI):**
    * Desenvolver uma interface gráfica utilizando bibliotecas como Tkinter (padrão do Python), PyQt, Kivy, ou até mesmo uma interface web simples com Flask/Django para uma experiência de usuário mais rica e visual.
* **Relatórios:**
    * Geração de relatórios básicos, como:
        * Livros mais emprestados.
        * Usuários com mais empréstimos.
        * Livros disponíveis/emprestados.
* **Autenticação de Usuários (Operadores):**
    * Se o sistema fosse usado por múltiplos bibliotecários, um sistema de login simples poderia ser implementado.
* **Tratamento de Erros Mais Robusto:**
    * Expandir o tratamento de exceções para cobrir mais casos de erro e fornecer feedback mais claro ao usuário.
* **Testes Unitários e de Integração:**
    * Escrever testes automatizados para garantir a robustez e o correto funcionamento de cada função e do sistema como um todo.
* **Paginação:**
    * Para visualização de listas muito grandes de livros ou usuários, implementar um sistema de paginação.
* **Internacionalização (i18n):**
    * Permitir que as mensagens do sistema sejam exibidas em diferentes idiomas.

---


Este documento foi feito para detalhar o funcionamento do código


---
