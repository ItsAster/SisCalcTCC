import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import xml.etree.ElementTree as ET
import pandas as pd

# Dicionário de namespaces
namespaces = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

# Listas para armazenar os dados de compras e vendas
dados_compras = []
dados_vendas = []

# Referência para o widget de visualização de dados
visualizar_dados_text_compras = None
visualizar_dados_text_vendas = None

# Função para extrair dados de uma única compra
def extrair_dados_compra(infNFe):
    for det in infNFe.findall(".//nfe:det", namespaces):
        compra = {
            "Tipo": "Compra",
            "Data da Emissão da Nota Fiscal": "",
            "Chave de Acesso": "",
            "Informações para o Cálculo": "",
            "CNPJ Emitente": "",
            "Nome Emitente": "",
            "UF Emitente": "",
            "Destinatário": "",
            "Nº do Item na NFe da Venda": "",
            "Descrição do Produto": "",
            "Código do Produto": "",
            "NCM": "",
            "EAN": "",
            "Unidade Comercializada": "",
            "Quantidade Comercializada": "",
            "Valor Unitário da Venda": "",
            "Produto ST": "",
            "Alíquota Interna": "",
            "Valor Unitário da Venda Presumida": ""
        }

        dhEmi_element = infNFe.find(".//nfe:dhEmi", namespaces)
        chNFe_element = infNFe.find(".//nfe:chNFe", namespaces)

        # Adicionar verificações antes de acessar os atributos
        if dhEmi_element is not None:
            compra["Data da Emissão da Nota Fiscal"] = dhEmi_element.text

        if chNFe_element is not None:
            compra["Chave de Acesso"] = chNFe_element.text

        compra["Informações para o Cálculo"] = infNFe.find(
            ".//nfe:natOp", namespaces).text

        emitente = infNFe.find(".//nfe:emit", namespaces)
        compra["CNPJ Emitente"] = emitente.find(".//nfe:CNPJ", namespaces).text
        compra["Nome Emitente"] = emitente.find(
            ".//nfe:xNome", namespaces).text
        compra["UF Emitente"] = emitente.find(".//nfe:UF", namespaces).text

        destinatario = infNFe.find(".//nfe:dest", namespaces)
        destinatario_id = destinatario.find(".//nfe:CPF | .//nfe:CNPJ", namespaces)
        if destinatario_id is not None:
            compra["Destinatário"] = destinatario_id.text

        compra["Nº do Item na NFe da Venda"] = det.get("nItem")
        produto = det.find(".//nfe:prod", namespaces)
        compra["Descrição do Produto"] = produto.find(
            ".//nfe:xProd", namespaces).text
        compra["Código do Produto"] = produto.find(
            ".//nfe:cProd", namespaces).text
        compra["NCM"] = produto.find(
            ".//nfe:NCM", namespaces).text
        compra["EAN"] = produto.find(
            ".//nfe:cEAN", namespaces).text
        compra["Unidade Comercializada"] = produto.find(
            ".//nfe:uCom", namespaces).text
        compra["Quantidade Comercializada"] = produto.find(
            ".//nfe:qCom", namespaces).text
        compra["Valor Unitário da Venda"] = produto.find(
            ".//nfe:vUnCom", namespaces).text

        produto_st = det.find(
            ".//nfe:imposto/nfe:ICMS/nfe:ICMSSN102", namespaces)
        if produto_st is not None and produto_st.find(".//nfe:CSOSN", namespaces).text == "103":
            compra["Produto ST"] = "Sim"
        else:
            compra["Produto ST"] = "Não"

        dados_compras.append(compra)

# Função para extrair dados de uma única venda
def extrair_dados_venda(infNFe):
    for det in infNFe.findall(".//nfe:det", namespaces):
        venda = {
            "Tipo": "Venda",
            "Data da Emissão da Nota Fiscal": "",
            "Chave de Acesso": "",
            "Informações para o Cálculo": "",
            "CNPJ Emitente": "",
            "Nome Emitente": "",
            "UF Emitente": "",
            "Destinatário": "",
            "Nº do Item na NFe da Venda": "",
            "Descrição do Produto": "",
            "Código do Produto": "",
            "NCM": "",
            "EAN": "",
            "Unidade Comercializada": "",
            "Quantidade Comercializada": "",
            "Valor Unitário da Venda": "",
            "Produto ST": "",
            "Alíquota Interna": "",
            "Valor Unitário da Venda Presumida": ""
        }

        dhEmi_element = infNFe.find(".//nfe:dhEmi", namespaces)
        chNFe_element = infNFe.find(".//nfe:chNFe", namespaces)

        # Adicionar verificações antes de acessar os atributos
        if dhEmi_element is not None:
            venda["Data da Emissão da Nota Fiscal"] = dhEmi_element.text

        if chNFe_element is not None:
            venda["Chave de Acesso"] = chNFe_element.text

        venda["Informações para o Cálculo"] = infNFe.find(
            ".//nfe:natOp", namespaces).text

        emitente = infNFe.find(".//nfe:emit", namespaces)
        venda["CNPJ Emitente"] = emitente.find(".//nfe:CNPJ", namespaces).text
        venda["Nome Emitente"] = emitente.find(
            ".//nfe:xNome", namespaces).text
        venda["UF Emitente"] = emitente.find(".//nfe:UF", namespaces).text

        destinatario = infNFe.find(".//nfe:dest", namespaces)
        destinatario_id = destinatario.find(".//nfe:CPF | .//nfe:CNPJ", namespaces)
        if destinatario_id is not None:
            venda["Destinatário"] = destinatario_id.text

        venda["Nº do Item na NFe da Venda"] = det.get("nItem")
        produto = det.find(".//nfe:prod", namespaces)
        venda["Descrição do Produto"] = produto.find(
            ".//nfe:xProd", namespaces).text
        venda["Código do Produto"] = produto.find(
            ".//nfe:cProd", namespaces).text
        venda["NCM"] = produto.find(
            ".//nfe:NCM", namespaces).text
        venda["EAN"] = produto.find(
            ".//nfe:cEAN", namespaces).text
        venda["Unidade Comercializada"] = produto.find(
            ".//nfe:uCom", namespaces).text
        venda["Quantidade Comercializada"] = produto.find(
            ".//nfe:qCom", namespaces).text
        venda["Valor Unitário da Venda"] = produto.find(
            ".//nfe:vUnCom", namespaces).text

        produto_st = det.find(
            ".//nfe:imposto/nfe:ICMS/nfe:ICMSSN102", namespaces)
        if produto_st is not None and produto_st.find(".//nfe:CSOSN", namespaces).text == "103":
            venda["Produto ST"] = "Sim"
        else:
            venda["Produto ST"] = "Não"

        dados_vendas.append(venda)

# Função para extrair dados de um arquivo XML
def extrair_dados_nfe(xml_files, tipo, csv_file=None, text_widget=None):
    try:
        if tipo == "Compra":
            dados = dados_compras
            extrair_dados = extrair_dados_compra
            visualizar_text_widget = visualizar_dados_text_compras
        elif tipo == "Venda":
            dados = dados_vendas
            extrair_dados = extrair_dados_venda
            visualizar_text_widget = visualizar_dados_text_vendas

        if visualizar_text_widget is not None:
            visualizar_text_widget.delete(1.0, tk.END)
            visualizar_text_widget.insert(
                tk.END, "Processando... Por favor, aguarde.")

        dados.clear()  # Limpa a lista antes de processar novos arquivos

        for xml_file in xml_files:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            for infNFe in root.findall(".//nfe:infNFe", namespaces):
                extrair_dados(infNFe)

        if visualizar_text_widget is not None:
            visualizar_dados(csv_file, visualizar_text_widget)  # Atualiza a visualização após processar os arquivos

        messagebox.showinfo(
            "Concluído", f"{len(xml_files)} arquivos processados e dados salvos em '{tipo.lower()}s.csv'.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")


# Função para salvar os dados em um arquivo CSV
def salvar_csv(csv_file):
    if csv_file == "compras.csv":
        df = pd.DataFrame(dados_compras)
    elif csv_file == "vendas.csv":
        df = pd.DataFrame(dados_vendas)

    # Verificar se o DataFrame está vazio
    if df.empty:
        return

    # Verificar se o arquivo CSV existe e não está vazio
    try:
        existing_df = pd.read_csv(csv_file)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        existing_df = pd.DataFrame()

    # Concatenar os DataFrames
    df = pd.concat([existing_df, df], ignore_index=True)

    # Converter a coluna "NCM" para formato numérico, se possível
    df["NCM"] = pd.to_numeric(df["NCM"], errors="coerce")

    # Verificar se o DataFrame está vazio após as operações anteriores
    if df.empty:
        return

    # Ordenar por ordem crescente usando o NCM como filtro
    df = df.sort_values(by=["NCM"])

    # Salvar no arquivo CSV
    df.to_csv(csv_file, index=False)

# Função para carregar arquivos XML
def carregar_arquivos(tipo, text_widget=None):
    if tipo == "Compra":
        csv_file = "compras.csv"
    elif tipo == "Venda":
        csv_file = "vendas.csv"

    arquivos_xml = filedialog.askopenfilenames(
        title=f"Selecione os arquivos XML de {tipo}", filetypes=[("XML files", "*.xml")])
    if arquivos_xml:
        extrair_dados_nfe(arquivos_xml, tipo, csv_file, text_widget)
        salvar_csv(csv_file)

# Função para visualizar dados
def visualizar_dados(csv_file=None, text_widget=None):
    try:
        if csv_file is None:
            csv_file = "compras.csv"  # Nome padrão para visualizar dados de compras

        if "compras" in csv_file:
            df = pd.read_csv("compras.csv")
            tipo = "Compras"
        elif "vendas" in csv_file:
            df = pd.read_csv("vendas.csv")
            tipo = "Vendas"
        else:
            # Se o nome do arquivo não contiver "compras" ou "vendas", exibir uma mensagem adequada
            text_widget.delete(1.0, tk.END)
            text_widget.insert(
                tk.END, "O arquivo não é reconhecido como compras ou vendas.")
            return

        # Verificar se o DataFrame está vazio
        if df.empty:
            text_widget.delete(1.0, tk.END)
            text_widget.insert(
                tk.END, f"O arquivo '{csv_file}' está vazio.")
            return

        # Formatar DataFrame como string com ajustes
        formatted_data = f"{tipo}:\n"
        for idx, row in df.iterrows():
            formatted_data += f"\nProduto {idx + 1}:\n"
            for key, value in row.items():
                formatted_data += f"  - {key}: {value}\n"

        # Limpar e inserir os dados no widget
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, formatted_data)
    except FileNotFoundError:
        text_widget.delete(1.0, tk.END)
        text_widget.insert(
            tk.END, f"O arquivo '{csv_file}' não foi encontrado.")
    except pd.errors.EmptyDataError:
        text_widget.delete(1.0, tk.END)
        text_widget.insert(
            tk.END, f"O arquivo '{csv_file}' está vazio.")

# Função para criar a aba de visualização de dados de compras
def criar_aba_visualizar_dados_compras():
    aba = ttk.Frame(tab_control)
    tab_control.add(aba, text='Visualizar Dados Compras')

    visualizar_dados_text_compras = tk.Text(aba, height=20, width=80)
    visualizar_dados_text_compras.pack(padx=20, pady=20)

    visualizar_dados_btn = tk.Button(
        aba, text="Visualizar Dados Compras", command=lambda: visualizar_dados("compras.csv", visualizar_dados_text_compras))
    visualizar_dados_btn.pack(pady=20)

    # Retornar a referência do widget para que ele possa ser acessado globalmente
    return visualizar_dados_text_compras

# Função para criar a aba de carregar NFE compra
def criar_aba_carregar_nfe_compra():
    aba = ttk.Frame(tab_control)
    tab_control.add(aba, text='Carregar NFE Compra')

    btn_carregar_compra = tk.Button(
        aba, text="Carregar NFE Compra", command=lambda: carregar_arquivos("Compra"))
    btn_carregar_compra.pack(pady=20)

# Função para criar a aba de carregar NFE venda
def criar_aba_carregar_nfe_venda():
    aba = ttk.Frame(tab_control)
    tab_control.add(aba, text='Carregar NFE Venda')

    btn_carregar_venda = tk.Button(
        aba, text="Carregar NFE Venda", command=lambda: carregar_arquivos("Venda", visualizar_dados_text_vendas))
    btn_carregar_venda.pack(pady=20)

# Função para criar a aba de visualização de dados de vendas
def criar_aba_visualizar_dados_vendas():
    aba = ttk.Frame(tab_control)
    tab_control.add(aba, text='Visualizar Dados Vendas')

    visualizar_dados_text_vendas = tk.Text(aba, height=20, width=80)
    visualizar_dados_text_vendas.pack(padx=20, pady=20)

    visualizar_dados_btn = tk.Button(
        aba, text="Visualizar Dados Vendas", command=lambda: visualizar_dados("vendas.csv", visualizar_dados_text_vendas))
    visualizar_dados_btn.pack(pady=20)

    # Retornar a referência do widget para que ele possa ser acessado globalmente
    return visualizar_dados_text_vendas

# Criar a interface gráfica
root = tk.Tk()
root.title("Sistema de Cálculo")

# Criar notebook com abas
tab_control = ttk.Notebook(root)

# Criar abas
criar_aba_carregar_nfe_compra()
visualizar_dados_text_compras = criar_aba_visualizar_dados_compras()
criar_aba_carregar_nfe_venda()
visualizar_dados_text_vendas = criar_aba_visualizar_dados_vendas()

# Iniciar o loop principal
tab_control.pack(expand=1, fill='both')
root.mainloop()
