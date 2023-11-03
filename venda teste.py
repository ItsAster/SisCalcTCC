import csv
from datetime import datetime

class Produto:
    def __init__(self, nome, quantidade, preco_compra):
        self.nome = nome
        self.quantidade = quantidade
        self.preco_compra = preco_compra

class Estoque:
    def __init__(self):
        self.produtos = {}
        self.nome_arquivo_csv = 'estoque.csv'
        self.nome_pasta_vendas = 'vendas'
        self.carregar_estoque_csv()

    def cadastrar_produto(self, numero, nome, quantidade, preco_compra):
        if numero in self.produtos:
            # Se o produto já existe, cria uma nova ramificação
            ramificacao = f'{nome}_{len(self.produtos[numero]) + 1}'
            self.produtos[numero][ramificacao] = Produto(nome, quantidade, preco_compra)
            print(f'Produto cadastrado com sucesso: {ramificacao} (Número: {numero})')
        else:
            # Se o produto não existe, cria uma nova entrada
            self.produtos[numero] = {'ramificacao_1': Produto(nome, quantidade, preco_compra)}
            print(f'Produto cadastrado com sucesso: {nome} (Número: {numero}, Ramificação: 1)')

        # Atualiza o arquivo CSV automaticamente
        self.salvar_estoque_csv()

    def vender_produto(self, numero, quantidade, preco_venda):
        if numero in self.produtos:
            quantidade_total_estoque = sum(produto.quantidade for produto in self.produtos[numero].values())

            if quantidade_total_estoque >= quantidade:
                total_restituicao = 0
                detalhes_venda = []

                for ramificacao, produto in self.produtos[numero].items():
                    if quantidade > 0:
                        quantidade_venda = min(quantidade, produto.quantidade)
                        produto.quantidade -= quantidade_venda
                        quantidade -= quantidade_venda

                        diferenca = (preco_venda - produto.preco_compra) * quantidade_venda
                        imposto = diferenca * 0.1  # Exemplo de imposto de 10%
                        total_restituicao += diferenca - imposto

                        print(f'Diferenca: {diferenca}, Imposto: {imposto}')
                        detalhes_venda.append({
                            'Produto': produto.nome,
                            'Ramificação': ramificacao,
                            'Quantidade Vendida': quantidade_venda,
                            'Valor de Venda': preco_venda,
                            'Valor de Compra': produto.preco_compra,
                            'Imposto': imposto,
                            'Tipo Imposto': 'A Receber' if diferenca < 0 else 'A Pagar'
                        })

                # Atualiza o arquivo CSV do estoque
                self.salvar_estoque_csv()

                # Cria a planilha de detalhes da venda
                self.criar_planilha_venda(detalhes_venda, total_restituicao)

                return total_restituicao

            else:
                print(f'Erro: Quantidade insuficiente no estoque do produto {numero}.')
                return 0

        else:
            print(f'Erro: Produto com número {numero} não encontrado no estoque.')
            return 0

    def criar_planilha_venda(self, detalhes_venda, total_restituicao):
        try:
            # Gera um nome de arquivo único baseado na data e hora
            nome_arquivo = f'{self.nome_pasta_vendas}/venda_{datetime.now().strftime("%Y%m%d%H%M%S")}.csv'

            with open(nome_arquivo, 'w', newline='') as arquivo_csv:
                escrever_csv = csv.writer(arquivo_csv)
                escrever_csv.writerow(['Produto', 'Ramificação', 'Quantidade Vendida', 'Valor de Venda', 'Valor de Compra', 'Imposto', 'Tipo Imposto'])

                for detalhe in detalhes_venda:
                    escrever_csv.writerow([detalhe['Produto'], detalhe['Ramificação'], detalhe['Quantidade Vendida'],
                                           detalhe['Valor de Venda'], detalhe['Valor de Compra'], detalhe['Imposto'], detalhe['Tipo Imposto']])

                if total_restituicao > 0:
                    print(f'Planilha de venda criada com sucesso: {nome_arquivo}')
                    print(f'Total a pagar pela receita: R${total_restituicao:.2f}')
                elif total_restituicao < 0:
                    print(f'Planilha de venda criada com sucesso: {nome_arquivo}')
                    print(f'Total a receber pela receita: R${-total_restituicao:.2f}')
                else:
                    print('Planilha de venda criada, mas nenhum valor a pagar ou receber.')

        except Exception as e:
            print(f'Erro ao criar a planilha de venda: {e}')

    def calcular_estoque_total(self):
        estoque_total = {}

        for numero, ramificacoes in self.produtos.items():
            for ramificacao, produto in ramificacoes.items():
                if produto.nome not in estoque_total:
                    estoque_total[produto.nome] = {'Quantidade': 0, 'Valor Total': 0}
                estoque_total[produto.nome]['Quantidade'] += produto.quantidade
                estoque_total[produto.nome]['Valor Total'] += produto.quantidade * produto.preco_compra

        return estoque_total

    def salvar_estoque_csv(self):
        with open(self.nome_arquivo_csv, 'w', newline='') as arquivo_csv:
            escrever_csv = csv.writer(arquivo_csv)
            escrever_csv.writerow(['Número', 'Ramificação', 'Nome', 'Quantidade', 'Preço Compra'])
            for numero, ramificacoes in self.produtos.items():
                for ramificacao, produto in ramificacoes.items():
                    escrever_csv.writerow([numero, ramificacao, produto.nome, produto.quantidade, produto.preco_compra])

    def carregar_estoque_csv(self):
        try:
            with open(self.nome_arquivo_csv, 'r') as arquivo_csv:
                leitor_csv = csv.reader(arquivo_csv)
                next(leitor_csv)  # Pula o cabeçalho
                for linha in leitor_csv:
                    numero, ramificacao, nome, quantidade, preco_compra = linha
                    numero = int(numero)
                    quantidade = int(quantidade)
                    preco_compra = float(preco_compra)
                    if numero not in self.produtos:
                        self.produtos[numero] = {}
                    self.produtos[numero][ramificacao] = Produto(nome, quantidade, preco_compra)
            print(f'Estoque carregado de {self.nome_arquivo_csv}')
        except FileNotFoundError:
            print('Arquivo CSV não encontrado. Criando novo estoque.')

    def criar_pasta_vendas(self):
        try:
            import os
            os.makedirs(self.nome_pasta_vendas, exist_ok=True)
        except Exception as e:
            print(f'Erro ao criar a pasta de vendas: {e}')

# Função para obter dados de cadastro
def obter_dados_cadastro():
    numero = int(input('Digite o número do produto a ser cadastrado: '))
    nome = input('Digite o nome do produto a ser comprado: ')
    quantidade = int(input('Digite a quantidade a ser comprada: '))
    preco_compra = float(input('Digite o preço de compra por unidade: '))
    return numero, nome, quantidade, preco_compra

# Função para obter dados de venda
def obter_dados_venda():
    numero = int(input('Digite o número do produto a ser vendido: '))
    quantidade = int(input('Digite a quantidade a ser vendida: '))
    preco_venda = float(input('Digite o preço de venda por unidade: '))
    return numero, quantidade, preco_venda

# Exemplo de uso
estoque = Estoque()
estoque.criar_pasta_vendas()

while True:
    print("\nOpções:")
    print("1. Cadastrar Produto")
    print("2. Vender Produto")
    print("3. Calcular Estoque Total")
    print("4. Sair")

    opcao = input("Escolha uma opção (1, 2, 3 ou 4): ")

    if opcao == "1":
        estoque.cadastrar_produto(*obter_dados_cadastro())
    elif opcao == "2":
        total_restituicao = estoque.vender_produto(*obter_dados_venda())
        if total_restituicao > 0:
            print(f'Total a pagar para receita: R${total_restituicao:.2f}')
        elif total_restituicao < 0:
            print(f'Total a receber pela receita: R${-total_restituicao:.2f}')
        else:
            print('Nenhum valor a pagar ou receber.')
    elif opcao == "3":
        estoque_total = estoque.calcular_estoque_total()
        print('\nEstoque Total:')
        for produto, info in estoque_total.items():
            print(f'{produto}: {info["Quantidade"]} unidades, Valor Total: R${info["Valor Total"]:.2f}')
    elif opcao == "4":
        print("Programa encerrado.")
        break
    else:
        print("Opção inválida. Tente novamente.")
