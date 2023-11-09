import pandas as pd
import csv
from datetime import date
from tkinter import ttk, messagebox
import tkinter as tk


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
        self.create_notebook()

        # Adicionar as guias ao notebook
        self.tab_cadastro = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_cadastro, text='Cadastro')

        self.tab_estoque = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_estoque, text='Estoque')

        self.tab_pesquisa = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_pesquisa, text='Pesquisa')

        self.tab_edicao = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_edicao, text='Edição')

        self.tab_exclusao = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_exclusao, text='Exclusão')

        # Chamar métodos para criar widgets em cada guia
        self.create_cadastro_widgets()
        self.create_estoque_widgets()
        self.create_pesquisa_widgets()
        self.create_edicao_widgets()
        self.create_exclusao_widgets()

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(padx=10, pady=10, expand=True, fill='both')

    def create_cadastro_widgets(self):
        lbl_numero = ttk.Label(self.tab_cadastro, text='Número do Produto:')
        lbl_numero.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_numero = ttk.Entry(self.tab_cadastro)
        self.entry_numero.grid(row=0, column=1, padx=5, pady=5)

        lbl_nome = ttk.Label(self.tab_cadastro, text='Nome do Produto:')
        lbl_nome.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_nome = ttk.Entry(self.tab_cadastro)
        self.entry_nome.grid(row=1, column=1, padx=5, pady=5)

        lbl_valor = ttk.Label(self.tab_cadastro, text='Valor do Produto:')
        lbl_valor.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.entry_valor = ttk.Entry(self.tab_cadastro)
        self.entry_valor.grid(row=2, column=1, padx=5, pady=5)

        lbl_quantidade = ttk.Label(
            self.tab_cadastro, text='Quantidade do Produto:')
        lbl_quantidade.grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.entry_quantidade = ttk.Entry(self.tab_cadastro)
        self.entry_quantidade.grid(row=3, column=1, padx=5, pady=5)

        btn_cadastrar = ttk.Button(
            self.tab_cadastro, text='Cadastrar', command=self.cadastrar_produto)
        btn_cadastrar.grid(row=4, column=0, columnspan=2, pady=10)


    def create_estoque_widgets(self):
        self.text_estoque = tk.Text(
            self.tab_estoque, wrap=tk.WORD, width=60, height=20)
        self.text_estoque.grid(row=0, column=0, padx=5, pady=5)

        self.update_estoque_display()

    def create_pesquisa_widgets(self):
        lbl_pesquisa_numero = ttk.Label(
            self.tab_pesquisa, text='Número do Produto:')
        lbl_pesquisa_numero.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_pesquisa_numero = ttk.Entry(self.tab_pesquisa)
        self.entry_pesquisa_numero.grid(row=0, column=1, padx=5, pady=5)

        btn_pesquisar = ttk.Button(
            self.tab_pesquisa, text='Pesquisar', command=self.pesquisar_produto)
        btn_pesquisar.grid(row=0, column=2, pady=10)

        self.text_pesquisa_resultado = tk.Text(
            self.tab_pesquisa, wrap=tk.WORD, width=60, height=20)
        self.text_pesquisa_resultado.grid(
            row=1, column=0, columnspan=3, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(
            self.tab_pesquisa, command=self.text_pesquisa_resultado.yview)
        scrollbar.grid(row=1, column=3, sticky='ns')
        self.text_pesquisa_resultado['yscrollcommand'] = scrollbar.set

    def create_edicao_widgets(self):
        lbl_edicao_numero = ttk.Label(
            self.tab_edicao, text='Número do Produto:')
        lbl_edicao_numero.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_edicao_numero = ttk.Entry(self.tab_edicao)
        self.entry_edicao_numero.grid(row=0, column=1, padx=5, pady=5)

        lbl_edicao_ramificacao = ttk.Label(
            self.tab_edicao, text='Ramificação:')
        lbl_edicao_ramificacao.grid(
            row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_edicao_ramificacao = ttk.Entry(self.tab_edicao)
        self.entry_edicao_ramificacao.grid(row=1, column=1, padx=5, pady=5)

        btn_editar = ttk.Button(
            self.tab_edicao, text='Editar', command=self.abrir_janela_edicao)
        btn_editar.grid(row=2, column=0, columnspan=2, pady=10)

    def create_exclusao_widgets(self):
        lbl_exclusao_numero = ttk.Label(
            self.tab_exclusao, text='Número do Produto:')
        lbl_exclusao_numero.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_exclusao_numero = ttk.Entry(self.tab_exclusao)
        self.entry_exclusao_numero.grid(row=0, column=1, padx=5, pady=5)

        lbl_exclusao_ramificacao = ttk.Label(
            self.tab_exclusao, text='Ramificação:')
        lbl_exclusao_ramificacao.grid(
            row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_exclusao_ramificacao = ttk.Entry(self.tab_exclusao)
        self.entry_exclusao_ramificacao.grid(row=1, column=1, padx=5, pady=5)

        btn_excluir = ttk.Button(
            self.tab_exclusao, text='Excluir', command=self.abrir_janela_exclusao)
        btn_excluir.grid(row=2, column=0, columnspan=2, pady=10)

    def carregar_estoque(self):
        try:
            with open('estoque.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.adicionar_produto_do_csv(row)
        except FileNotFoundError:
            pass
        except Exception as e:
            messagebox.showerror(
                "Erro", f"Erro ao carregar o estoque: {e}")

    def adicionar_produto_do_csv(self, row):
        numero = int(row['Numero'])
        ramificacao = int(row.get('Ramificacao', 1))
        self.estoque.setdefault(numero, {}).setdefault(ramificacao, []).append({
            'nome': row['Nome'],
            'valor': float(row['Valor']),
            'quantidade': int(row['Quantidade']),
            'valor_total': float(row['ValorTotal']),
            'data_cadastro': date.fromisoformat(row['DataCadastro'])
        })

    def salvar_csv(self):
        dados_organizados = []

        for numero, ramificacoes in self.estoque.items():
            for ramificacao, registros in ramificacoes.items():
                for info in registros:
                    dados_organizados.append({
                        'Numero': numero,
                        'Ramificacao': ramificacao,
                        'Nome': info['nome'],
                        'Valor': info['valor'],
                        'Quantidade': info['quantidade'],
                        'ValorTotal': info['valor_total'],
                        'DataCadastro': info['data_cadastro'].isoformat()
                    })

        # Verificar se há dados antes de criar o DataFrame
        if dados_organizados:
            df = pd.DataFrame(dados_organizados)
            df.sort_values(by=['Numero', 'Ramificacao'], inplace=True)
            df.to_csv('estoque.csv', index=False)

            historico_df = pd.DataFrame(self.historico_estoque)
            historico_df.to_csv('historico_estoque.csv', index=False)
        else:
            # Se não houver dados, criar DataFrames vazios
            pd.DataFrame().to_csv('estoque.csv', index=False)
            pd.DataFrame(self.historico_estoque).to_csv('historico_estoque.csv', index=False)

    def cadastrar_produto(self):
        try:
            numero = int(self.entry_numero.get())
            nome = self.entry_nome.get()
            valor = float(self.entry_valor.get())
            quantidade = int(self.entry_quantidade.get())

            valor_total = valor * quantidade
            data_atual = date.today()

            # Adicionar uma nova entrada para o número do produto
            ramificacao = 1

            # Verificar se o número do produto já existe
            if numero in self.estoque:
                # Adicionar uma nova ramificação
                ramificacao = max(self.estoque[numero], default=0) + 1

            # Verificar se a ramificação já existe
            if ramificacao not in self.estoque.get(numero, {}):
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

                message = f"Ramificação {ramificacao} do Produto {numero} ({nome}) cadastrada com sucesso." if ramificacao > 1 else f"Produto {
                    numero} ({nome}) cadastrado com sucesso."
                messagebox.showinfo("Sucesso", message)

                self.salvar_csv()
                self.update_estoque_display()
            else:
                messagebox.showerror(
                    "Erro", "Ramificação já existe para este produto.")

        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores válidos.")
    def update_estoque_display(self):
        self.text_estoque.delete(1.0, tk.END)

        if self.estoque:
            sorted_numeros = sorted(self.estoque.keys())

            for numero in sorted_numeros:
                ramificacoes = self.estoque[numero]

                self.text_estoque.insert(tk.END, f"Produto {numero}: \n")

                valor_total_produto = 0
                quantidade_total_produto = 0

                sorted_ramificacoes = sorted(ramificacoes.keys())

                for ramificacao in sorted_ramificacoes:
                    registros = ramificacoes[ramificacao]

                    self.text_estoque.insert(
                        tk.END, f"  Ramificação {ramificacao}: \n")

                    for info in registros:
                        self.text_estoque.insert(
                            tk.END, f"    Nome: {info['nome']}\n")
                        self.text_estoque.insert(
                            tk.END, f"    Valor: R${info['valor']: .2f}\n")
                        self.text_estoque.insert(
                            tk.END, f"    Quantidade: {info['quantidade']}\n")
                        self.text_estoque.insert(
                            tk.END, f"    Valor Total: R${info['valor_total']: .2f}\n")
                        self.text_estoque.insert(
                            tk.END, f"    Data de Cadastro: {info['data_cadastro']}\n")
                        self.text_estoque.insert(
                            tk.END, "-" * 20 + "\n")

                        valor_total_produto += info['valor_total']
                        quantidade_total_produto += info['quantidade']

                self.text_estoque.insert(
                    tk.END, f"  Valor total referente ao (Produto {numero}): R${valor_total_produto: .2f}\n")
                self.text_estoque.insert(
                    tk.END, f"  Quantidade total referente ao (Produto {numero}): {quantidade_total_produto}\n")
                self.text_estoque.insert(tk.END, "=" * 20 + "\n")

        else:
            self.text_estoque.insert(tk.END, "O estoque está vazio.")


    def pesquisar_produto(self):
        try:
            numero_pesquisa = int(self.entry_pesquisa_numero.get())
            self.text_pesquisa_resultado.delete(1.0, tk.END)

            if numero_pesquisa in self.estoque:
                for ramificacao, registros in self.estoque[numero_pesquisa].items():
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
    def abrir_janela_edicao(self):
        try:
            numero_edicao = int(self.entry_edicao_numero.get())
            ramificacao_edicao = int(self.entry_edicao_ramificacao.get())

            if numero_edicao in self.estoque and ramificacao_edicao in self.estoque[numero_edicao]:
                produto_para_editar = self.estoque[numero_edicao][ramificacao_edicao][0]
                self.abrir_janela_edicao_produto(
                    numero_edicao, ramificacao_edicao, produto_para_editar)
            else:
                messagebox.showerror(
                    "Erro", "Produto não encontrado para edição.")

        except ValueError:
            messagebox.showerror(
                "Erro", "Por favor, insira números de produto e ramificação válidos.")
    def abrir_janela_edicao_produto(self, numero, ramificacao, produto):
        janela_edicao = tk.Toplevel(self.root)
        janela_edicao.title(
            f"Editar Produto {numero} - Ramificação {ramificacao}")

        lbl_nome = ttk.Label(janela_edicao, text='Nome do Produto:')
        lbl_nome.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        entry_nome = ttk.Entry(janela_edicao)
        entry_nome.grid(row=0, column=1, padx=5, pady=5)
        entry_nome.insert(0, produto['nome'])

        lbl_valor = ttk.Label(janela_edicao, text='Valor do Produto:')
        lbl_valor.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        entry_valor = ttk.Entry(janela_edicao)
        entry_valor.grid(row=1, column=1, padx=5, pady=5)
        entry_valor.insert(0, produto['valor'])

        lbl_quantidade = ttk.Label(
            janela_edicao, text='Quantidade do Produto:')
        lbl_quantidade.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        entry_quantidade = ttk.Entry(janela_edicao)
        entry_quantidade.grid(row=2, column=1, padx=5, pady=5)
        entry_quantidade.insert(0, produto['quantidade'])

        btn_salvar = ttk.Button(janela_edicao, text='Salvar',
                                command=lambda: self.salvar_edicao(numero, ramificacao, entry_nome.get(), entry_valor.get(), entry_quantidade.get(), janela_edicao))
        btn_salvar.grid(row=3, column=0, columnspan=2, pady=10)

    def salvar_edicao(self, numero, ramificacao, novo_nome, novo_valor, nova_quantidade, janela_edicao):
        try:
            novo_valor = float(novo_valor)
            nova_quantidade = int(nova_quantidade)

            produto_editado = {
                'nome': novo_nome,
                'valor': novo_valor,
                'quantidade': nova_quantidade,
                'valor_total': novo_valor * nova_quantidade,
                'data_cadastro': date.today()
            }

            # Atualizar o estoque com o produto editado
            self.estoque[numero][ramificacao] = [produto_editado]

            # Atualizar o histórico
            self.historico_estoque.append({
                'numero': numero,
                'ramificacao': ramificacao,
                'nome': novo_nome,
                'valor': novo_valor,
                'quantidade': nova_quantidade,
                'valor_total': novo_valor * nova_quantidade,
                'data_cadastro': date.today()
            })

            # Salvar as alterações no CSV
            self.salvar_csv()

            # Atualizar a exibição do estoque
            self.update_estoque_display()

            # Fechar a janela de edição
            janela_edicao.destroy()

            # Exibir mensagem de sucesso
            mensagem = f"Produto {numero} - Ramificação {ramificacao} editado com sucesso."
            messagebox.showinfo("Sucesso", mensagem)

        except ValueError:
            # Exibir mensagem de erro
            messagebox.showerror("Erro", "Por favor, insira valores válidos.")

    def abrir_janela_exclusao(self):
        try:
            numero_exclusao = int(self.entry_exclusao_numero.get())
            ramificacao_exclusao = int(self.entry_exclusao_ramificacao.get())

            if numero_exclusao in self.estoque and ramificacao_exclusao in self.estoque[numero_exclusao]:
                produto_para_excluir = self.estoque[numero_exclusao][ramificacao_exclusao][0]
                self.excluir_produto(
                    numero_exclusao, ramificacao_exclusao, produto_para_excluir)
            else:
                messagebox.showerror(
                    "Erro", "Produto não encontrado para exclusão.")

        except ValueError:
            messagebox.showerror(
                "Erro", "Por favor, insira números de produto e ramificação válidos.")

    def excluir_produto(self, numero, ramificacao, produto):
        confirmacao = messagebox.askyesno(
            "Confirmação", f"Tem certeza que deseja excluir o Produto {numero} - Ramificação {ramificacao}?")

        if confirmacao:
            # Remover o produto do estoque
            if ramificacao in self.estoque.get(numero, {}):
                del self.estoque[numero][ramificacao]

                # Se não houver mais ramificações, remova o número do produto
                if not self.estoque[numero]:
                    del self.estoque[numero]

                # Atualizar o histórico
                self.historico_estoque.append({
                    'numero': numero,
                    'ramificacao': ramificacao,
                    'nome': produto['nome'],
                    'valor': produto['valor'],
                    'quantidade': produto['quantidade'],
                    'valor_total': produto['valor_total'],
                    'data_cadastro': date.today(),
                    'acao': 'exclusao'
                })

                # Salvar as alterações no CSV
                self.salvar_csv()

                # Atualizar a exibição do estoque
                self.update_estoque_display()

                # Exibir mensagem de sucesso
                mensagem = f"Produto {
                    numero} - Ramificação {ramificacao} excluído com sucesso."
                messagebox.showinfo("Sucesso", mensagem)

            else:
                messagebox.showerror(
                    "Erro", "Ramificação não encontrada para exclusão.")


if __name__ == "__main__":
    root = tk.Tk()
    app = EstoqueApp(root)
    root.mainloop()
