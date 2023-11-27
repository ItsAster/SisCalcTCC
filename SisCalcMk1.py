import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import xml.etree.ElementTree as ET
import pandas as pd
import time

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



def calculo_ICMS(barra_progresso, text_widget=None):
    try:
        # Carregando os dados das planilhas
        compras_df = pd.read_csv('Compras_Teste_Calculo_21-11.csv', sep=';', decimal=',', thousands='.', encoding='latin1')
        vendas_df = pd.read_csv('Vendas_Teste_Calculo_21-11.csv', sep=';', decimal=',', thousands='.', encoding='latin1')

        # Removendo "R$" do campo "BCST Unitaria" e substituindo ',' por '.'
        compras_df['BCST Unitaria'] = pd.to_numeric(compras_df['BCST Unitaria'].replace('[^\d.,]', '', regex=True).str.replace(',', '.'), errors='coerce')
        vendas_df['Valor Unitario da Venda'] = pd.to_numeric(vendas_df['Valor Unitario da Venda'].replace('[^\d.,]', '', regex=True).str.replace(',', '.'), errors='coerce')

        # Inicializando a variável de ramificação
        ramificacao = 0

        # Criar um DataFrame para armazenar os resultados
        resultado_df = pd.DataFrame(columns=[
            'Letra D', 'Sequencial da Linha', 'Chave de Acesso da NF Venda', 'Nr do Item na NF da Venda',
            'Fator de Conversão', 'Código do Produto na NFe de Venda', 'Valor Unitário de Venda',
            'Quantidade Vendida', 'Chave de Acesso da Compra', 'Nr do Item na NFe da Compra',
            'Código Interno do Produto na NFe Compra', 'BCST Unitária', 'Diferença', 'Valor do ICMS A Restituir ou Complementar',
            'Período de Escrituração da NFe de Compra AAAAMM'
        ])

        # Variável para sequenciar as linhas
        sequencial_linha = 1

        # Iterando sobre as linhas da tabela de vendas
        for _, venda_row in vendas_df.iterrows():
            calculo_icmsst = 0
            contador = 0
            nome_do_produto = venda_row['Descricao do Produto Vendido']
            print(nome_do_produto)

            # 2º - Verificar se o valor da coluna 'Sequencial EAN' do produto selecionado da 1ª regra da tabela Vendas_Testes_CSV.csv é encontrado na coluna 'Sequencial EAN' da planilha Compras_Testes_Valores_3_CSV.csv são iguais
            sequencial_ean_venda = venda_row['Sequencial EAN']
            compras_selecionadas = compras_df[compras_df['Sequencial EAN'] == sequencial_ean_venda]
            lista_compras_selecionadas = [compras_selecionadas]

            # Verificando se a compra foi encontrada
            if compras_selecionadas.empty:
                print(f"Produto {nome_do_produto} com Sequencial EAN {sequencial_ean_venda} não encontrado no estoque")
                continue

            # 3º - Se a 3ª regra passar, verificar se o valor da coluna 'Informacoes para o Calculo do Estoque da Venda' do produto selecionado da 1ª regra da planilha Vendas_Testes_CSV.csv for igual a 'consumidor final'
            if venda_row['Informacoes para o Calculo do Estoque da Venda'] != 'consumidor final':
                print(f"Produto {nome_do_produto} não foi vendido para consumidor final")
                continue

            # 4º - Se a 4ª regra passar, verificar se o valor da coluna 'Produto ST?' do produto selecionado da 1ª regra da planilha Vendas_Testes_CSV.csv for igual a 'Sim'
            if venda_row['Produto ST?'] != 'sim':
                print(f"Produto {nome_do_produto} não é Produto ST")
                continue

            # 5º - Verificar se o valor da coluna 'Data Emissao da Venda' do produto selecionado da 1ª regra é maior que o valor da coluna 'Data Emissao da Compra' dos produtos selecionados com EAN igual na 2ª regra
            data_emissao_venda = pd.to_datetime(venda_row['Data da Emissao da Venda'], format='mixed', dayfirst=True)
            compras_selecionadas = compras_selecionadas[pd.to_datetime(compras_selecionadas['Data da Emissao da Compra'], format='mixed', dayfirst=True) < data_emissao_venda]
            print('Passou AQUI')
            # 6º - Calcular a diferença de valores
            quantidade_venda = venda_row['Quantidade Vendida']
            for index_compras, compra_row in compras_selecionadas.iterrows():
                if quantidade_venda <= 0:
                    index_compras = index_compras - 1
                    print("For 2 Break")
                    print(index_compras)
                    break
                icmsst_total = 0
                print(f"index_compras = {index_compras}")
                print(compra_row)
                quantidade_compra = compra_row['Quantidade em Unidades']
                print(f"Quantidade de produto COMPRA = {quantidade_compra} - Antes do While")
                print(f"Quantidade de produto VENDA = {quantidade_venda} - Antes do While")

                # aqui valida a entrada da quantida de venda
                while quantidade_venda > 0 and quantidade_compra > 0:
                    compra_especifica_ramificacao = compras_df.loc[compras_df['Ramificacao'] == ramificacao]
                    print(compra_especifica_ramificacao)

                    if quantidade_compra < quantidade_venda:
                        vendaCalculo = quantidade_compra
                    else:
                        vendaCalculo = quantidade_venda
                    diferenca_valores = round(compra_row['BCST Unitaria'] - venda_row['Valor Unitario da Venda'], 2)
                    # quantidade = min(quantidade_compra, quantidade_venda)
                    novaQuantidadeProdutoCompra = quantidade_compra - quantidade_venda

                    if novaQuantidadeProdutoCompra < 0:
                        novaQuantidadeProdutoCompra = 0
                    else:
                        index_compras = index_compras
                    # quantidade_compra -= quantidade
                    compras_df.loc[index_compras, 'Quantidade em Unidades'] = novaQuantidadeProdutoCompra
                    compras_df.to_csv('Compras_Teste_Calculo_21-11.csv', index=False)
                    quantidade_venda = quantidade_venda - quantidade_compra
                    if quantidade_venda < 0:
                        quantidade_venda = 0
                    aliquota = venda_row['Aliquota Interna']
                    print(f"{diferenca_valores} * {vendaCalculo} * {aliquota}")
                    calculo_icmsst = round((diferenca_valores * vendaCalculo * (venda_row['Aliquota Interna']) / 100), 2)
                    print(calculo_icmsst)

                    if contador == 0:
                        guardar_calculo_icmsst = calculo_icmsst
                        contador = contador + 1
                    else:
                        guardar_calculo_icmsst = guardar_calculo_icmsst + calculo_icmsst

                    if novaQuantidadeProdutoCompra == 0 and ramificacao >= 0:
                        ramificacao = ramificacao + 1
                        print("While Break")
                        break
                    print('///// Teste While ///////')

                progresso_atual = int((index_compras / len(compras_selecionadas)) * 100)
                barra_progresso["value"] = progresso_atual
                barra_progresso.update_idletasks()
                barra_progresso.step(10)  # Ajuste conforme necessário
                barra_progresso.update()

            if diferenca_valores > 0:
                print(f"O produto {nome_do_produto} com valor {guardar_calculo_icmsst} pode ser ressarcido na receita")
            else:
                calculo_icmsst = calculo_icmsst * -1
                print(f"O produto {nome_do_produto} com valor {guardar_calculo_icmsst} deve ser pago para a receita")

            print('///// Teste For - 2 ///////')

            print('///// Teste For - 1 ///////')
            if diferenca_valores < 0:
                diferenca_valores = diferenca_valores * -1
            nova_linha = pd.DataFrame({
                'Letra D': ['D'],
                'Sequencial da Linha': [sequencial_linha],  # Substitua 'sequencial_da_linha' pelo valor correto
                'Chave de Acesso da NF Venda': [venda_row['Chave de Acesso da NF Venda']],
                'Nr do Item na NF da Venda': [venda_row['Nr do Item na NFe da Venda']],
                'Fator de Conversão': [1],
                'Código do Produto na NFe de Venda': ['Falta no CSV - Venda'],
                'Valor Unitário de Venda': [venda_row['Valor Unitario da Venda']],
                'Quantidade Vendida': [venda_row['Quantidade Vendida']],
                'Chave de Acesso da Compra': [compra_row['Chave de Acesso da Compra']],
                'Nr do Item na NFe da Compra': [compra_row['Nr do Item na Nfe da Compra']],
                'Código Interno do Produto na NFe Compra': [compra_row['Codigo do Produto']],
                'BCST Unitária': [compra_row['BCST Unitaria']],
                'Diferença': [diferenca_valores],
                'Valor do ICMS A Restituir ou Complementar': [guardar_calculo_icmsst],
                'Período de Escrituração da NFe de Compra AAAAMM': ['201906']
            })

            resultado_df = pd.concat([resultado_df, nova_linha], ignore_index=True, sort=False)

            # Incrementa o sequencial da linha
            sequencial_linha += 1

            # Salva o DataFrame resultado_df em um arquivo CSV
            resultado_df.to_csv('resultado.csv', index=False, sep=';', decimal=',', encoding='utf-8')

        # Se tudo ocorreu bem
        barra_progresso["value"] = 100
        messagebox.showinfo("Sucesso", "O cálculo foi realizado com sucesso e o arquivo resultado.csv foi criado.")
        time.sleep(0.5)
        barra_progresso["value"] = 0
        return True

    except FileNotFoundError as e:
        messagebox.showerror("Erro", "Arquivo não encontrado. Verifique se as planilhas estão presentes.")
        return False
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")
        return False



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


# Função para criar a aba Comparar Dados
def criar_aba_comparar_dados():
    aba = ttk.Frame(tab_control)
    tab_control.add(aba, text='Calcular Restituição ICMS-ST')
    # Criar a barra de progresso global
    barra_progresso = ttk.Progressbar(aba, orient="horizontal", length=300, mode="determinate")
    btn_comparar_dados = tk.Button(
        aba, text="Calcular Restituição ICMS-ST", command=lambda: calculo_ICMS(barra_progresso))
    barra_progresso.pack(pady=10)
    btn_comparar_dados.pack(pady=20)


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
criar_aba_comparar_dados()

# Iniciar o loop principal
tab_control.pack(expand=1, fill='both')
root.mainloop()
