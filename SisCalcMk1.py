import os
import json
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import csv

class SistemaNota:
    HEADER = ['Código', 'Descrição', 'NCM', 'Quantidade',
              'Preço Unitário', 'Empresa', 'CNPJ', 'Ramificação NCM']

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Notas")
        self.dados_notas = []
        self.ramificacoes_ncm = {}
        self.carregar_ramificacoes()

        self.notebook = ttk.Notebook(root)
        self.notebook.grid(row=0, column=0, columnspan=2, pady=5)

        self.aba_cadastro_nfe = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_cadastro_nfe, text='Cadastro via Nota Fiscal')
        self.criar_widgets_cadastro_nfe()

        self.aba_cadastro_manual = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_cadastro_manual, text='Cadastro Manual')
        self.criar_widgets_cadastro_manual()

        self.aba_visualizar_estoque = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_visualizar_estoque, text='Visualizar Estoque')
        self.criar_widgets_visualizar_estoque()

    def carregar_ramificacoes(self):
        try:
            with open('ramificacoes.json', 'r') as file:
                self.ramificacoes_ncm = json.load(file)
        except FileNotFoundError:
            self.ramificacoes_ncm = {}

    def salvar_ramificacoes(self):
        with open('ramificacoes.json', 'w') as file:
            json.dump(self.ramificacoes_ncm, file)

    def criar_widgets_cadastro_manual(self):
        labels = ["Código:", "Descrição:", "NCM:", "Quantidade:",
                  "Preço Unitário:", "Empresa:", "CNPJ:"]
        entries = []

        for i, label in enumerate(labels):
            tk.Label(self.aba_cadastro_manual, text=label).grid(
                row=i, column=0, padx=5, pady=5, sticky="w")
            entry = tk.Entry(self.aba_cadastro_manual)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries.append(entry)

        tk.Button(self.aba_cadastro_manual, text="Cadastrar Compra Manual", command=lambda: self.cadastrar_compra_manual(entries)).grid(
            row=7, column=0, padx=5, pady=5, columnspan=2)

    def criar_widgets_cadastro_nfe(self):
        tk.Button(self.aba_cadastro_nfe, text="Selecionar Arquivos XML", command=self.selecionar_arquivos_nfe).grid(
            row=0, column=0, padx=5, pady=5, columnspan=2)

        tk.Button(self.aba_cadastro_nfe, text="Cadastrar Compra via Nota Fiscal", command=self.cadastrar_compra_nfe).grid(
            row=1, column=0, padx=5, pady=5, columnspan=2)

    def criar_widgets_visualizar_estoque(self):
        columns = self.HEADER
        self.treeview_estoque = ttk.Treeview(
            self.aba_visualizar_estoque, columns=columns, show='headings'
        )

        for col in columns:
            self.treeview_estoque.heading(col, text=col)
            self.treeview_estoque.column(col, width=200)  # Ajuste a largura conforme necessário

        yscroll = ttk.Scrollbar(self.aba_visualizar_estoque,
                                orient='vertical', command=self.treeview_estoque.yview)
        yscroll.grid(row=0, column=1, sticky='ns')
        self.treeview_estoque.configure(yscrollcommand=yscroll.set)

        xscroll = ttk.Scrollbar(self.aba_visualizar_estoque,
                                orient='horizontal', command=self.treeview_estoque.xview)
        xscroll.grid(row=1, column=0, sticky='ew')
        self.treeview_estoque.configure(xscrollcommand=xscroll.set)

        self.treeview_estoque.grid(row=0, column=0, padx=10, pady=10)
        self.treeview_estoque['height'] = 50  # Substitua 20 pelo número desejado de linhas visíveis

        tk.Button(self.aba_visualizar_estoque, text="Atualizar Estoque", command=self.visualizar_estoque).grid(
            row=1, column=0, padx=5, pady=5, sticky='e'+'w')



    def visualizar_estoque(self):
        caminho_csv = 'dados_notas.csv'
        existing_data = []

        if os.path.isfile(caminho_csv):
            with open(caminho_csv, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                existing_data = list(reader)

        self.treeview_estoque.delete(*self.treeview_estoque.get_children())

        if existing_data and existing_data[0][2] not in self.HEADER:
            self.HEADER.append(existing_data[0][2])

        total_estoque_por_ncm = {}  # Dicionário para armazenar a quantidade total por NCM
        total_valor_por_ncm = {}    # Dicionário para armazenar o valor total por NCM

        for row in existing_data[1:]:
            ncm = row[2]
            quantidade_estoque = self.ramificacoes_ncm.get(ncm, 0)
            row.append(quantidade_estoque)
            self.treeview_estoque.insert('', 'end', values=row)

            # Atualizar a quantidade total por NCM
            total_estoque_por_ncm[ncm] = total_estoque_por_ncm.get(ncm, 0) + float(row[3])  # Coluna 'Quantidade'

            # Atualizar o valor total por NCM
            valor_unitario = float(row[4])  # Coluna 'Preço Unitário'
            total_valor_por_ncm[ncm] = total_valor_por_ncm.get(ncm, 0) + float(row[3]) * valor_unitario

        if existing_data and existing_data[0][2] not in self.HEADER:
            self.HEADER.pop()

        # Imprimir a quantidade total no estoque e o valor total do estoque por NCM
        for ncm, quantidade_total in total_estoque_por_ncm.items():
            valor_total = total_valor_por_ncm.get(ncm, 0)
            print(f"NCM: {ncm}, Quantidade Total no Estoque: {quantidade_total}, Valor Total do Estoque: {valor_total}")

# Restante do código...


    def obter_valor_unitario_por_ncm(self, existing_data, ncm):
        for row in existing_data[1:]:
            if row[2] == ncm:
                valor_unitario_str = row[5]

                try:
                    valor_unitario = float(valor_unitario_str)
                    return valor_unitario
                except ValueError:
                    print(f"Valor unitário inválido para NCM {ncm}: {valor_unitario_str}")
                    return 10.0

        return 10.0


    def salvar_csv(self, dados_nota):
        ncm = dados_nota[2]
        ramificacao_ncm = self.ramificacoes_ncm.get(ncm, 0)

        caminho_csv = 'dados_notas.csv'
        dados_nota = [str(item) if item is not None else '' for item in dados_nota]
        dados_nota.append(ramificacao_ncm)

        existing_data = []
        if os.path.isfile(caminho_csv):
            with open(caminho_csv, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                existing_data = list(reader)

        ncm_exists = any(row[2] == ncm for row in existing_data)

        with open(caminho_csv, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            if not existing_data or not any(row[2] == self.HEADER[2] for row in existing_data):
                writer.writerow(self.HEADER)

            existing_data.append(dados_nota)
            sorted_data = sorted(existing_data[1:], key=lambda x: x[2])
            sorted_data.insert(0, existing_data[0])

            writer.writerows(sorted_data)

        return caminho_csv if ncm_exists else None

    def extrair_dados_nota(self, caminho_xml):
        tree = ET.parse(caminho_xml)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

        codigo = root.find('.//nfe:ide/nfe:cNF', namespaces=ns).text
        descricao = root.find(
            './/nfe:det/nfe:prod/nfe:xProd', namespaces=ns).text
        ncm = root.find('.//nfe:det/nfe:prod/nfe:NCM', namespaces=ns).text
        quantidade = root.find(
            './/nfe:det/nfe:prod/nfe:qCom', namespaces=ns).text
        preco_unitario = root.find(
            './/nfe:det/nfe:prod/nfe:vUnCom', namespaces=ns).text
        empresa = root.find('.//nfe:emit/nfe:xNome', namespaces=ns).text
        cnpj = root.find('.//nfe:emit/nfe:CNPJ', namespaces=ns).text

        return codigo, descricao, ncm, quantidade, preco_unitario, empresa, cnpj

    def atualizar_ramificacoes_ncm(self, ncm):
        existing_ncm_count = self.ramificacoes_ncm.get(ncm, 0)
        caminho_csv = 'dados_notas.csv'
        existing_data = []

        if os.path.isfile(caminho_csv):
            with open(caminho_csv, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                existing_data = list(reader)

        ncm_exists_in_csv = any(row[2] == ncm for row in existing_data)

        if not ncm_exists_in_csv:
            self.ramificacoes_ncm[ncm] = 1
        else:
            self.ramificacoes_ncm[ncm] = existing_ncm_count + 1

    def cadastrar_compra_manual(self, entries):
        dados_nota = [entry.get() for entry in entries]

        if not all(dados_nota):
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        self.atualizar_ramificacoes_ncm(dados_nota[2])

        try:
            caminho_csv = self.salvar_csv(dados_nota)
            if caminho_csv:
                messagebox.showinfo("Sucesso", "Compra cadastrada com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar a compra no CSV: {str(e)}")

    def cadastrar_compra_nfe(self):
        if not self.dados_notas:
            messagebox.showerror("Erro", "Selecione pelo menos um arquivo XML.")
            return

        for caminho_xml in self.dados_notas:
            try:
                dados_nota = self.extrair_dados_nota(caminho_xml)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao extrair dados do XML ({caminho_xml}): {str(e)}")
                continue

            self.atualizar_ramificacoes_ncm(dados_nota[2])

            try:
                self.salvar_csv(dados_nota)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar dados no CSV ({caminho_xml}): {str(e)}")

        messagebox.showinfo("Sucesso", "Dados extraídos e salvos no arquivo CSV.")

    def selecionar_arquivos_nfe(self):
        try:
            # Abre uma janela de seleção de arquivos
            arquivos_xml = filedialog.askopenfilenames(filetypes=[("Arquivos XML", "*.xml")])

            # Verifica se o usuário cancelou a seleção ou não escolheu nenhum arquivo
            if not arquivos_xml:
                messagebox.showinfo("Informação", "Nenhum arquivo XML selecionado.")
                return

            # Atualiza a lista de dados_notas com os caminhos dos arquivos XML
            self.dados_notas = list(arquivos_xml)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao selecionar arquivos XML: {str(e)}")

        # Feedback ao usuário
        messagebox.showinfo("Sucesso", "Arquivos XML selecionados com sucesso.")

    def on_close(self):
        self.salvar_ramificacoes()
        self.root.destroy()

# Criar a janela principal
root = tk.Tk()
sistema_nota = SistemaNota(root)
root.geometry("1650x1150")
root.protocol("WM_DELETE_WINDOW", sistema_nota.on_close)
root.mainloop()
