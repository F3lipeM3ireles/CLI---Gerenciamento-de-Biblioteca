from collections import deque
from datetime import date

# A gente cadastrou alguns livros e usuários direto no código pra ficar mais interessante visualmente
livros = {
    "Harry Potter 1": ("JK Rowling", 1989, "Fantasia", True),
    "Harry Potter 2": ("JK Rowling", 1998, "Fantasia", True),
    "Harry Potter 3": ("JK Rowling", 1999, "Fantasia", True),
    "Harry Potter 4": ("JK Rowling", 2000, "Fantasia", True),
    "Harry Potter 5": ("JK Rowling", 2003, "Fantasia", True),
    "Harry Potter 6": ("JK Rowling", 2005, "Fantasia", True),
    "O Senhor dos Anéis": ("J.R.R. Tolkien", 1954, "Fantasia", True),
    "1984": ("George Orwell", 1949, "Distopia", True),
    "O Pequeno Príncipe": ("Antoine de Saint-Exupéry", 1943, "Infantil", True),
    "Dom Quixote": ("Miguel de Cervantes", 1605, "Clássico", True),
    "A Revolução dos Bichos": ("George Orwell", 1945, "Satírico", True)
}

usuarios = {
    1: "Pedro",
    2: "João",
    3: "Felipe",
    4: "Mariana",
    5: "Carlos",
    6: "Ana",
    7: "Lucas"
}

# Criamos essa variável pra guardar os empréstimos que foram feitos
# Essa informação seria composta do id do usuário, o nome do livro e a data do emprestimo
emprestimos = []  # Lista de tuplas: (usuario_id, titulo, data)

# De forma parecida, se o cliente quiser emprestar um livro que está indisponível, ele poderá fazer a reserva
# Nesse caso, ficará armazenado nessa variável o registro da reserva
# A variável é um dicionário, onde a chave é o livro, e o valor é uma fila com o id dos usuários
reservas = {}

# Aqui a gente fez algo semelhante a logs do sistema. Ele guarda as ações executadas em uma pilha 
pilha_operacoes = []


# Menu principal para navegação no sistema
# Exibe opções de cadastro, visualização, empréstimo, devolução e histórico
def menu():
    while True:
        print("\n===== Biblioteca CLI =====")
        print("1 - Cadastrar livro")
        print("2 - Cadastrar usuário")
        print("3 - Visualizar cadastros")
        print("4 - Emprestar livro")
        print("5 - Devolver livro")
        print("6 - Exibir histórico de operações")
        print("7 - Sair")
        escolha = input("Escolha uma opção: ").strip()

        if escolha == '1':
            cadastrar_livro()
        elif escolha == '2':
            cadastrar_usuario()
        elif escolha == '3':
            visualizar_cadastros()
        elif escolha == '4':
            emprestar_livro()
        elif escolha == '5':
            devolver_livro()
        elif escolha == '6':
            exibir_operacoes()
        elif escolha == '7':
            print("Adeus, vai pela sombra!")
            break
        else:
            print("Opção inválida. Tente novamente.")


# Função para cadastrar livros
# Solicita título, autor, ano e gênero, validando formatação e tipo de dado
# Adiciona livro ao dicionário com flag de disponibilidade
# Registra operação na pilha de logs

def cadastrar_livro():
    titulo = input("Escreva o nome do livro: ").strip().capitalize()
    while True:
        dados = input("Cadastre no formato: autor, ano, genero (separado por vírgula): ").split(',')
        if len(dados) != 3:
            print("Formato inválido. Use autor, ano, genero.")
            continue
        autor = dados[0].strip()
        try:
            ano = int(dados[1].strip())
        except ValueError:
            print("Ano inválido.")
            continue
        genero = dados[2].strip()
        break
    livros[titulo] = (autor, ano, genero, True)
    pilha_operacoes.append(f"Cadastro de livro: '{titulo}'")
    print(f"Livro '{titulo}' cadastrado com sucesso.")


# Função para cadastrar usuários
# Solicita ID e nome, garantindo ID numérico e não duplicado
# Adiciona usuário ao dicionário e registra operação

def cadastrar_usuario():
    while True:
        try:
            usuario_id = int(input("Informe o ID do novo usuário: ").strip())
        except ValueError:
            print("ID deve ser numérico.")
            continue
        if usuario_id in usuarios:
            print("ID já cadastrado!")
            continue
        break
    nome = input("Informe o nome do usuário: ").strip().capitalize()
    usuarios[usuario_id] = nome
    pilha_operacoes.append(f"Cadastro de usuário: {usuario_id} - {nome}")
    print(f"Usuário '{nome}' cadastrado com sucesso (ID: {usuario_id}).")


# Função para visualizar cadastros
# Permite escolher listar livros com status (Disponível/Emprestado) ou usuários

def visualizar_cadastros():
    while True:
        print("1 - Livros")
        print("2 - Usuários")
        opcao = input("O que deseja visualizar? ").strip()
        if opcao == '1':
            print("\n== Livros ==")
            for titulo, info in livros.items():
                autor, ano, genero, disponivel = info
                status = "Disponível" if disponivel else "Emprestado"
                print(f"- {titulo}: {autor}, {ano}, {genero} -> {status}")
            break
        elif opcao == '2':
            print("\n== Usuários ==")
            for usuario_id, nome in usuarios.items():
                print(f"- {usuario_id}: {nome}")
            break
        else:
            print("Opção inválida. Escolha 1 ou 2.")


# Função para emprestar livro
# Valida ID de usuário, exibe livros disponíveis e solicita título
# Atualiza flag, registra empréstimo e adiciona à pilha
# Se indisponível, oferta reserva e registra

def emprestar_livro():
    while True:
        try:
            usuario_id = int(input("ID do usuário: ").strip())
        except ValueError:
            print("ID inválido.")
            continue
        if usuario_id not in usuarios:
            print("Usuário não cadastrado.")
            continue
        break

    disponiveis = [titulo for titulo, info in livros.items() if info[3]]
    if not disponiveis:
        print("Não há livros disponíveis.")
        return
    print("\n== Livros disponíveis ==")
    for titulo in disponiveis:
        autor, ano, genero, _ = livros[titulo]
        print(f"- {titulo}: {autor}, {ano}, {genero}")

    while True:
        titulo = input("Título do livro: ").strip()
        if titulo not in livros:
            print("Livro não cadastrado.")
            continue
        break
    autor, ano, genero, disponivel = livros[titulo]
    if disponivel:
        livros[titulo] = (autor, ano, genero, False)
        emprestimos.append((usuario_id, titulo, date.today()))
        pilha_operacoes.append(f"Empréstimo: usuário {usuario_id} -> '{titulo}'")
        print(f"Livro '{titulo}' emprestado para {usuarios[usuario_id]}.")
    else:
        print(f"Livro '{titulo}' indisponível.")
        resp = input("Deseja reservar? (S/N) ").strip().upper()
        if resp == 'S':
            reservas.setdefault(titulo, deque()).append(usuario_id)
            pilha_operacoes.append(f"Reserva: usuário {usuario_id} para '{titulo}'")
            print(f"Usuário {usuario_id} adicionado à fila de reserva de '{titulo}'.")


# Função para devolver livro
# Solicita ID e título, verifica empréstimo na lista
# Atualiza flag, remove empréstimo, registra operação
# Se existir reserva, faz empréstimo automático ao próximo

def devolver_livro():
    while True:
        try:
            usuario_id = int(input("ID do usuário: ").strip())
        except ValueError:
            print("ID inválido.")
            continue
        break
    while True:
        titulo = input("Título do livro a devolver: ").strip()
        if not any(u == usuario_id and t == titulo for u, t, _ in emprestimos):
            print("Empréstimo não encontrado. Verifique ID e título.")
            continue
        break
    for idx, (u, t, _) in enumerate(emprestimos):
        if u == usuario_id and t == titulo:
            autor, ano, genero, _ = livros[titulo]
            livros[titulo] = (autor, ano, genero, True)
            emprestimos.pop(idx)
            pilha_operacoes.append(f"Devolução: usuário {usuario_id} -> '{titulo}'")
            print(f"Livro '{titulo}' devolvido por {usuarios[usuario_id]}.")
            if reservas.get(titulo):
                prox = reservas[titulo].popleft()
                livros[titulo] = (autor, ano, genero, False)
                emprestimos.append((prox, titulo, date.today()))
                pilha_operacoes.append(f"Empréstimo automático: usuário {prox} -> '{titulo}'")
                print(f"Livro '{titulo}' agora emprestado automaticamente para usuário {prox}.")
            return


# Função para exibir histórico de operações (LIFO)
def exibir_operacoes():
    print("\n== Pilha de operações (LIFO) ==")
    for operacao in reversed(pilha_operacoes):
        print(f"- {operacao}")


if __name__ == '__main__':
    menu()
