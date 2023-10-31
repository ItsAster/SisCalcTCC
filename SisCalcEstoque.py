import csv
import datetime

estoque = {}
historico_estoque = []  # Lista para manter histórico de cadastros

def carregar_estoque():
    try:
        with open('estoque.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                numero = int(row['Numero'])
                if 'Ramificacao' in row:
                    ramificacao = int(row['Ramificacao'])
                else:
                    # Caso 'Ramificacao' não esteja presente, assume-se 1 como padrão
                    ramificacao = 1

                if numero not in estoque:
                    estoque[numero] = {}
                if ramificacao not in estoque[numero]:
                    estoque[numero][ramificacao] = []
                estoque[numero][ramificacao].append({
                    'nome': row['Nome'],
                    'valor': float(row['Valor']),
                    'quantidade': int(row['Quantidade']),
                    'valor_total': float(row['ValorTotal']),
                    'data_cadastro': datetime.date.fromisoformat(row['DataCadastro'])
                })
    except FileNotFoundError:
        pass

def cadastrar_produto(numero, nome, valor_str, quantidade):
    valor = float(valor_str.replace(',', '.'))  # Substituir vírgula por ponto e converter para float
    data_atual = datetime.date.today()
    ramificacao = 1

    if numero in estoque:
        # Se o produto já existe no estoque, determinar a próxima ramificação
        ramificacao = max(estoque[numero].keys()) + 1 if estoque[numero] else 1

    if numero not in estoque:
        estoque[numero] = {}

    if ramificacao not in estoque[numero]:
        estoque[numero][ramificacao] = []

    valor_total = valor * quantidade
    estoque[numero][ramificacao].append({
        'nome': nome,
        'valor': valor,
        'quantidade': quantidade,
        'valor_total': valor_total,
        'data_cadastro': data_atual
    })

    # Adicionar o novo cadastro ao histórico
    historico_estoque.append({
        'numero': numero,
        'ramificacao': ramificacao,
        'nome': nome,
        'valor': valor,
        'quantidade': quantidade,
        'valor_total': valor_total,
        'data_cadastro': data_atual
    })

    print(f"Produto {numero} ({nome}) cadastrado com sucesso.")
    salvar_csv()  # Salvar automaticamente após cadastrar




def exibir_estoque():
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
    if numero in estoque:
        for ramificacao, registros in estoque[numero].items():
            print(f"Produtos com número {numero} (Ramificação {ramificacao}):")
            for i, info in enumerate(registros, start=1):
                print(f"Cadastro {i}:")
                print(f"  Nome: {info['nome']}")
                print(f"  Valor: R${info['valor']}")
                print(f"  Quantidade: {info['quantidade']}")
                print(f"  Valor Total: R${info['valor_total']}")
                print(f"  Data de cadastro: {info['data_cadastro']}")
                print("-" * 20)
    else:
        print(f"Produtos com número {numero} não encontrados no estoque.")





def editar_produto(numero, ramificacao):
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
            nova_quantidade = int(input("Nova Quantidade: "))
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


        


def salvar_csv():
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

    with open('historico_estoque.csv', 'w', newline='') as historico_file:
        historico_fieldnames = ['Numero', 'Ramificacao', 'Nome', 'Valor', 'Quantidade', 'ValorTotal', 'DataCadastro']
        historico_writer = csv.DictWriter(historico_file, fieldnames=historico_fieldnames)

        historico_writer.writeheader()

        for item in historico_estoque:
            historico_writer.writerow({'Numero': item['numero'],
                                       'Ramificacao': item['ramificacao'],
                                       'Nome': item['nome'],
                                       'Valor': item['valor'],
                                       'Quantidade': item['quantidade'],
                                       'ValorTotal': item['valor_total'],
                                       'DataCadastro': item['data_cadastro'].isoformat()})

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
        while True:
            try:
                numero = int(input("Número do Produto: "))
                break  # Saia do loop se a conversão for bem-sucedida
            except ValueError:
                print("Por favor, insira um número válido.")

        nome = input("Nome do Produto: ")
        valor_str = input("Valor do Produto (use ponto como separador decimal): ")

        # Loop para garantir que o usuário forneça uma quantidade válida
        while True:
            try:
                quantidade = int(input("Quantidade do Produto: "))
                break  # Saia do loop se a conversão for bem-sucedida
            except ValueError:
                print("Por favor, insira uma quantidade válida.")

        cadastrar_produto(numero, nome, valor_str, quantidade)
    elif escolha == '2':
        exibir_estoque()
    elif escolha == '3':
        numero_pesquisa = int(input("Digite o número do produto para pesquisa: "))
        pesquisar_produto(numero_pesquisa)
    elif escolha == '4':
        numero_edicao = int(input("Digite o número do produto para edição: "))
        ramificacao_edicao = int(input("Digite a ramificação do produto para edição: "))
        editar_produto(numero_edicao, ramificacao_edicao)
    elif escolha == '5':
        print("Saindo do programa.")
        break
    else:
        print("Opção inválida. Tente novamente.")
