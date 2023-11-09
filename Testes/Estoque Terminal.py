import csv
import datetime
import pandas as pd

estoque = {}
historico_estoque = []

def carregar_estoque():
    """
    Carrega os dados do estoque a partir do arquivo CSV 'estoque.csv' e popula a estrutura de dados 'estoque'.
    """
    try:
        with open('estoque.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                numero = int(row['Numero'])
                ramificacao = int(row.get('Ramificacao', 1))
                estoque.setdefault(numero, {}).setdefault(ramificacao, []).append({
                    'nome': row['Nome'],
                    'valor': float(row['Valor']),
                    'quantidade': int(row['Quantidade']),
                    'valor_total': float(row['ValorTotal']),
                    'data_cadastro': datetime.date.fromisoformat(row['DataCadastro'])
                })
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Erro ao carregar o estoque: {e}")

def salvar_csv():
    """
    Salva os dados do estoque no arquivo CSV 'estoque.csv' e o histórico no arquivo 'historico_estoque.csv'.
    """
    with open('estoque.csv', 'w', newline='') as csvfile:
        fieldnames = ['Numero', 'Nome', 'Valor', 'Quantidade', 'ValorTotal', 'DataCadastro', 'Ramificacao']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for numero, ramificacoes in estoque.items():
            for ramificacao, registros in ramificacoes.items():
                for info in registros:
                    writer.writerow({'Numero': numero,
                                     'Nome': info['nome'],
                                     'Valor': info['valor'],
                                     'Quantidade': info['quantidade'],
                                     'ValorTotal': info['valor_total'],
                                     'DataCadastro': info['data_cadastro'].isoformat(),
                                     'Ramificacao': ramificacao})

        historico_df = pd.DataFrame(historico_estoque)
        historico_df.to_csv('historico_estoque.csv', index=False)

def obter_numero_valido(mensagem):
    """
    Obtém um número inteiro válido da entrada do usuário.

    Parâmetros:
    - mensagem: Mensagem a ser exibida ao solicitar a entrada.

    Retorna:
    - int: Número inteiro inserido pelo usuário.
    """
    while True:
        try:
            numero = int(input(mensagem))
            return numero
        except ValueError:
            print("Erro: Por favor, insira um número inteiro válido.")

def obter_quantidade_valida():
    """
    Obtém uma quantidade válida da entrada do usuário.

    Retorna:
    - int: Quantidade inserida pelo usuário.
    """
    while True:
        try:
            quantidade = int(input("Quantidade do Produto: "))
            if quantidade <= 0:
                print("Erro: A quantidade deve ser maior que zero.")
                continue
            return quantidade
        except ValueError:
            print("Erro: Por favor, insira uma quantidade válida.")

def cadastrar_produto(numero, nome, valor_str, quantidade):
    """
    Cadastra um novo produto no estoque.

    Parâmetros:
    - numero (int): Número do produto.
    - nome (str): Nome do produto.
    - valor_str (str): Valor do produto em formato de string.
    - quantidade (int): Quantidade do produto.
    """
    while True:
        try:
            valor = float(valor_str.replace(',', '.'))
            if valor < 0:
                print("Erro: O valor não pode ser negativo.")
                return
            break
        except ValueError:
            print("Erro: Valor inválido. Por favor, insira um valor numérico válido.")

    if quantidade <= 0:
        print("Erro: A quantidade deve ser maior que zero.")
        return

    data_atual = datetime.date.today()
    ramificacao = max(estoque.get(numero, {}), default=0) + 1

    estoque.setdefault(numero, {}).setdefault(ramificacao, []).append({
        'nome': nome,
        'valor': valor,
        'quantidade': quantidade,
        'valor_total': valor * quantidade,
        'data_cadastro': data_atual
    })

    historico_estoque.append({
        'numero': numero,
        'ramificacao': ramificacao,
        'nome': nome,
        'valor': valor,
        'quantidade': quantidade,
        'valor_total': valor * quantidade,
        'data_cadastro': data_atual
    })

    print(f"Produto {numero} ({nome}) cadastrado com sucesso.")
    salvar_csv()

def exibir_estoque():
    """
    Exibe informações detalhadas sobre o estoque, incluindo quantidade e valor total.
    """
    if estoque:
        print("Estoque:")
        valor_total_estoque = 0
        quantidade_total_estoque = 0

        for numero, ramificacoes in estoque.items():
            valor_total_produto = 0
            quantidade_total_produto = 0

            print(f"Produto {numero}:")
            for ramificacao, registros in ramificacoes.items():
                quantidade_total_ramificacao = sum(info['quantidade'] for info in registros)
                valor_total_ramificacao = sum(info['valor_total'] for info in registros)

                print(f"  Ramificação {ramificacao}:")
                print(f"    Quantidade Total: {quantidade_total_ramificacao}")
                print(f"    Valor Total: R${valor_total_ramificacao}")
                print("-" * 20)

                quantidade_total_produto += quantidade_total_ramificacao
                valor_total_produto += valor_total_ramificacao

            print(f"  Quantidade Total do Produto: {quantidade_total_produto}")
            print(f"  Valor Total do Produto: R${valor_total_produto}")
            print("=" * 20)

            quantidade_total_estoque += quantidade_total_produto
            valor_total_estoque += valor_total_produto

        print(f"Quantidade Total do Estoque: {quantidade_total_estoque}")
        print(f"Valor Total do Estoque: R${valor_total_estoque}")
    else:
        print("O estoque está vazio.")

def pesquisar_produto(numero):
    """
    Pesquisa e exibe informações detalhadas sobre um produto específico.

    Parâmetros:
    - numero (int): Número do produto a ser pesquisado.
    """
    if numero in estoque:
        for ramificacao, registros in estoque[numero].items():
            print(f"Produtos com número {numero} (Ramificação {ramificacao}):")
            for info in registros:
                print(f"  Nome: {info['nome']}")
                print(f"  Valor: R${info['valor']}")
                print(f"  Quantidade: {info['quantidade']}")
                print(f"  Valor Total: R${info['valor_total']}")
                print(f"  Data de cadastro: {info['data_cadastro']}")
                print("-" * 20)
    else:
        print(f"Produtos com número {numero} não encontrados no estoque.")

def editar_produto(numero, ramificacao):
    """
    Edita as informações de um produto específico.

    Parâmetros:
    - numero (int): Número do produto a ser editado.
    - ramificacao (int): Ramificação do produto a ser editado.
    """
    if numero in estoque and ramificacao in estoque[numero]:
        print(f"Editar Produto {numero} (Ramificação {ramificacao}):")
        print("1. Editar Nome")
        print("2. Editar Valor")
        print("3. Editar Quantidade")
        print("4. Voltar")

        escolha = input("Escolha uma opção (1/2/3/4): ")

        if escolha == '1':
            novo_nome = input("Novo Nome: ")
            for produto in estoque[numero][ramificacao]:
                produto['nome'] = novo_nome
            print("Nome editado com sucesso.")
            salvar_csv()
        elif escolha == '2':
            novo_valor_str = input("Novo Valor (use ponto como separador decimal): ")
            novo_valor = float(novo_valor_str.replace(',', '.'))
            for produto in estoque[numero][ramificacao]:
                produto['valor'] = novo_valor
                produto['valor_total'] = novo_valor * produto['quantidade']
            print("Valor editado com sucesso.")
            salvar_csv()
        elif escolha == '3':
            nova_quantidade = obter_quantidade_valida()
            for produto in estoque[numero][ramificacao]:
                produto['quantidade'] = nova_quantidade
                produto['valor_total'] = produto['valor'] * nova_quantidade
            print("Quantidade editada com sucesso.")
            salvar_csv()
        elif escolha == '4':
            print("Voltando ao menu principal.")
        else:
            print("Opção inválida. Tente novamente.")
    else:
        print(f"Produto {numero} (Ramificação {ramificacao}) não encontrado no estoque.")

# Carregar o estoque existente
carregar_estoque()

# Loop para cadastrar produtos em tempo real
while True:
    print("\nOpções:")
    print("1. Cadastrar Produto")
    print("2. Exibir Estoque")
    print("3. Pesquisar Produto")
    print("4. Editar Produto")
    print("5. Sair")

    escolha = input("Escolha uma opção (1/2/3/4/5): ")

    if escolha == '1':
        numero = obter_numero_valido("Número do Produto: ")
        nome = input("Nome do Produto: ")
        valor_str = input("Valor do Produto (use ponto como separador decimal): ")
        quantidade = obter_quantidade_valida()
        cadastrar_produto(numero, nome, valor_str, quantidade)
    elif escolha == '2':
        exibir_estoque()
    elif escolha == '3':
        numero_pesquisa = obter_numero_valido("Digite o número do produto para pesquisa: ")
        pesquisar_produto(numero_pesquisa)
    elif escolha == '4':
        numero_edicao = obter_numero_valido("Digite o número do produto para edição: ")
        ramificacao_edicao = obter_numero_valido("Digite a ramificação do produto para edição: ")
        editar_produto(numero_edicao, ramificacao_edicao)
    elif escolha == '5':
        print("Saindo do programa.")
        break
    else:
        print("Opção inválida. Tente novamente.")
