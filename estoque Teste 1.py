import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import date
import csv
import pandas as pd


class EstoqueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestão de Estoque")

        self.estoque = {}
        self.historico_estoque = []

        # Carregar o estoque existente
        self.carregar_estoque()

        # Criar widgets
        self.create_widgets()

    def create_widgets(self):
        # Criar notebook (abas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(padx=10, pady=10, expand=True, fill='both')

        # Aba de Cadastro
        self.tab_cadastro = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_cadastro, text='Cadastrar Produto')
        self.create_cadastro_widgets()

        # Aba de Estoque
        self.tab_estoque = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_estoque, text='Exibir Estoque')
        self.create_estoque_widgets()

        # Aba de Pesquisa
        self.tab_pesquisa = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_pesquisa, text='Pesquisar Produto')
        self.create_pesquisa_widgets()

    def create_cadastro_widgets(self):
        # Número do Produto
        lbl_numero = ttk.Label(self.tab_cadastro, text='Número do Produto:')
        lbl_numero.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_numero = ttk.Entry(self.tab_cadastro)
        self.entry_numero.grid(row=0, column=1, padx=5, pady=5)

        # Nome do Produto
        lbl_nome = ttk.Label(self.tab_cadastro, text='Nome do Produto:')
        lbl_nome.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_nome = ttk.Entry(self.tab_cadastro)
        self.entry_nome.grid(row=1, column=1, padx=5, pady=5)

        # Valor do Produto
        lbl_valor = ttk.Label(self.tab_cadastro, text='Valor do Produto:')
        lbl_valor.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.entry_valor = ttk.Entry(self.tab_cadastro)
        self.entry_valor.grid(row=2, column=1, padx=5, pady=5)

        # Quantidade do Produto
        lbl_quantidade = ttk.Label(
            self.tab_cadastro, text='Quantidade do Produto:')
        lbl_quantidade.grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.entry_quantidade = ttk.Entry(self.tab_cadastro)
        self.entry_quantidade.grid(row=3, column=1, padx=5, pady=5)

        # Botão Cadastrar
        btn_cadastrar = ttk.Button(
            self.tab_cadastro, text='Cadastrar', command=self.cadastrar_produto)
        btn_cadastrar.grid(row=4, column=0, columnspan=2, pady=10)

    def create_estoque_widgets(self):
        # Área de exibição do Estoque
        self.text_estoque = tk.Text(
            self.tab_estoque, wrap=tk.WORD, width=60, height=20)
        self.text_estoque.grid(row=0, column=0, padx=5, pady=5)

        # Atualizar a exibição do estoque
        self.update_estoque_display()

    def create_pesquisa_widgets(self):
        # Número do Produto para Pesquisa
        lbl_pesquisa_numero = ttk.Label(
            self.tab_pesquisa, text='Número do Produto:')
        lbl_pesquisa_numero.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_pesquisa_numero = ttk.Entry(self.tab_pesquisa)
        self.entry_pesquisa_numero.grid(row=0, column=1, padx=5, pady=5)

        # Botão Pesquisar
        btn_pesquisar = ttk.Button(
            self.tab_pesquisa, text='Pesquisar', command=self.pesquisar_produto)
        btn_pesquisar.grid(row=1, column=0, columnspan=2, pady=10)

        # Área de exibição do resultado da pesquisa
        self.text_pesquisa_resultado = tk.Text(
            self.tab_pesquisa, wrap=tk.WORD, width=60, height=20)
        self.text_pesquisa_resultado.grid(row=2, column=3, padx=5, pady=5)

    def carregar_estoque(self):
        try:
            with open('estoque.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    numero = int(row['Numero'])
                    ramificacao = int(row.get('Ramificacao', 1))
                    self.estoque.setdefault(numero, {}).setdefault(ramificacao, []).append({
                        'nome': row['Nome'],
                        'valor': float(row['Valor']),
                        'quantidade': int(row['Quantidade']),
                        'valor_total': float(row['ValorTotal']),
                        'data_cadastro': date.fromisoformat(row['DataCadastro'])
                    })
        except FileNotFoundError:
            pass
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar o estoque: {e}")

    def salvar_csv(self):
        # Organizar dados antes de salvar
        dados_organizados = []
        for numero, ramificacoes in self.estoque.items():
            for ramificacao, registros in ramificacoes.items():
                for info in registros:
                    dados_organizados.append({
                        'Numero': numero,
                        'Ramificacao': ramificacao,  # Adicione esta linha
                        'Nome': info['nome'],
                        'Valor': info['valor'],
                        'Quantidade': info['quantidade'],
                        'ValorTotal': info['valor_total'],
                        'DataCadastro': info['data_cadastro'].isoformat()
                    })

        # Converter dados para DataFrame do pandas
        df = pd.DataFrame(dados_organizados)

        # Ordenar por número do produto e ramificação
        df.sort_values(by=['Numero', 'Ramificacao'], inplace=True)

        # Salvar dados ordenados no arquivo CSV
        df.to_csv('estoque.csv', index=False)

        # Salvar histórico
        historico_df = pd.DataFrame(self.historico_estoque)
        historico_df.to_csv('historico_estoque.csv', index=False)





    def cadastrar_produto(self):
        try:
            numero = int(self.entry_numero.get())
            nome = self.entry_nome.get()
            valor = float(self.entry_valor.get())
            quantidade = int(self.entry_quantidade.get())

            valor_total = valor * quantidade
            data_atual = date.today()
            ramificacao = max(self.estoque.get(numero, {}), default=0) + 1

            self.estoque.setdefault(numero, {}).setdefault(ramificacao, []).append({
                'nome': nome,
                'valor': valor,
                'quantidade': quantidade,
                'valor_total': valor_total,
                'data_cadastro': data_atual
            })

            self.historico_estoque.append({
                'numero': numero,
                'ramificacao': ramificacao,
                'nome': nome,
                'valor': valor,
                'quantidade': quantidade,
                'valor_total': valor_total,
                'data_cadastro': data_atual
            })

            if ramificacao > 1:
                messagebox.showinfo("Sucesso", f"Ramificação {ramificacao} do Produto {numero} ({nome}) cadastrada com sucesso.")
            else:
                messagebox.showinfo("Sucesso", f"Produto {numero} ({nome}) cadastrado com sucesso.")
                
            self.salvar_csv()
            self.update_estoque_display()

        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores válidos.")


    def update_estoque_display(self):
        self.text_estoque.delete(1.0, tk.END)  # Limpar o texto atual

        if self.estoque:
            # Ordenar os números dos produtos de forma crescente
            sorted_numeros = sorted(self.estoque.keys())

            for numero in sorted_numeros:
                ramificacoes = self.estoque[numero]

                self.text_estoque.insert(tk.END, f"Produto {numero}: \n")

                valor_total_produto = 0
                quantidade_total_produto = 0

                # Ordenar as ramificações de forma crescente
                sorted_ramificacoes = sorted(ramificacoes.keys())

                for ramificacao in sorted_ramificacoes:
                    registros = ramificacoes[ramificacao]

                    self.text_estoque.insert(tk.END, f"  Ramificação {ramificacao}: \n")

                    for info in registros:
                        self.text_estoque.insert(tk.END, f"    Nome: {info['nome']}\n")
                        self.text_estoque.insert(tk.END, f"    Valor: R${info['valor']:.2f}\n")  # Formatando para 2 casas decimais
                        self.text_estoque.insert(tk.END, f"    Quantidade: {info['quantidade']}\n")
                        self.text_estoque.insert(tk.END, f"    Valor Total: R${info['valor_total']:.2f}\n")  # Formatando para 2 casas decimais
                        self.text_estoque.insert(tk.END, f"    Data de Cadastro: {info['data_cadastro']}\n")
                        self.text_estoque.insert(tk.END, "-" * 20 + "\n")

                        # Atualizar valores totais do produto
                        valor_total_produto += info['valor_total']
                        quantidade_total_produto += info['quantidade']

                self.text_estoque.insert(
                    tk.END, f"  Valor total referente ao (Produto {numero}): R${valor_total_produto:.2f}\n")  # Formatando para 2 casas decimais
                self.text_estoque.insert(
                    tk.END, f"  Quantidade total referente ao (Produto {numero}): {quantidade_total_produto}\n")
                self.text_estoque.insert(tk.END, "=" * 20 + "\n")

        else:
            self.text_estoque.insert(tk.END, "O estoque está vazio.")

            

    def pesquisar_produto(self):
        try:
            numero_pesquisa = int(self.entry_pesquisa_numero.get())

            # Limpar a área de resultado
            self.text_pesquisa_resultado.delete(1.0, tk.END)

            # Pesquisar o produto no estoque
            if numero_pesquisa in self.estoque:
                for ramificacao, registros in self.estoque[numero_pesquisa].items():
                    # Exibir informações da primeira ramificação encontrada
                    info = registros[0]
                    self.text_pesquisa_resultado.insert(
                        tk.END, f"Nome: {info['nome']}\n")
                    self.text_pesquisa_resultado.insert(
                        tk.END, f"Valor: R${info['valor']}\n")
                    self.text_pesquisa_resultado.insert(
                        tk.END, f"Quantidade: {info['quantidade']}\n")
                    self.text_pesquisa_resultado.insert(
                        tk.END, f"Valor Total: R${info['valor_total']}\n")
                    self.text_pesquisa_resultado.insert(
                        tk.END, f"Data de Cadastro: {info['data_cadastro']}\n")
                    self.text_pesquisa_resultado.insert(
                        tk.END, "-" * 20 + "\n")

                self.text_pesquisa_resultado.insert(tk.END, "=" * 20 + "\n")
            else:
                self.text_pesquisa_resultado.insert(
                    tk.END, f"Produto {numero_pesquisa} não encontrado no estoque.\n")

        except ValueError:
            messagebox.showerror(
                "Erro", "Por favor, insira um número de produto válido.")

if __name__ == "__main__":
    root = tk.Tk()
    app = EstoqueApp(root)
    root.mainloop()
