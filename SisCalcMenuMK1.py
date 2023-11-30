import os
import csv
import hashlib
import re
from tkinter import *
from tkinter import ttk, messagebox
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import xml.etree.ElementTree as ET
import pandas as pd
import time
from datetime import datetime



# Função que representa uma segunda tela
def funcao_segundo_script():



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


    def exibir_resultado(texto_resultado, texto_resultado_final):
        janela_resultado = tk.Toplevel(root)
        janela_resultado.title("Resultado do Cálculo ICMS-ST")
        
        text_widget = tk.Text(janela_resultado, height=20, width=80)
        text_widget.pack(padx=20, pady=20)
        
        text_widget.insert(tk.END, texto_resultado)
        text_widget.insert(tk.END, texto_resultado_final)
        text_widget.config(state=tk.DISABLED)  # Torna o widget somente leitura


    def calculo_ICMS(barra_progresso):
        try:
            # Carregando os dados das planilhas
            compras_df = pd.read_csv('Planilha_FINAL_COMPRA.csv', sep=';', decimal=',', thousands='.', encoding='latin1')
            vendas_df = pd.read_csv('Planilha_FINAL_VENDA.csv', sep=';', decimal=',', thousands='.', encoding='latin1')

            # Removendo "R$" do campo "BCST Unitaria" e substituindo ',' por '.'
            compras_df['BCST Unitaria'] = pd.to_numeric(compras_df['BCST Unitaria'].replace('[^\d.,]', '', regex=True).str.replace(',', '.'), errors='coerce')
            vendas_df['Valor Unitario da Venda'] = pd.to_numeric(vendas_df['Valor Unitario da Venda'].replace('[^\d.,]', '', regex=True).str.replace(',', '.'), errors='coerce')

            # Inicializando a variável de ramificação
            ramificacao = 0

            
            # Criar um DataFrame para armazenar os resultados
            data_atual = datetime.now()
            data_formatada = data_atual.strftime("%Y%m%d")
            line1 =  [
                'A', 'CNPJ RE', '201906', data_formatada,
                1, 1
             ]

            resultado_df_line1 = pd.DataFrame([line1])

            resultado_df_line1.to_csv('resultado.csv', index=False, header=False, sep=';', decimal=',', encoding='utf-8', mode='w')
            


            # Variável para sequenciar as linhas
            sequencial_linha = 1
            x = 0

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


                dados_calculo = [ 
                        'D',
                        sequencial_linha,
                        venda_row['Chave de Acesso da NF Venda'],
                        venda_row['Nr do Item na NFe da Venda'],
                        1,
                        venda_row['Valor Unitario da Venda'],
                        venda_row['Quantidade Vendida'],
                        compra_row['Chave de Acesso da Compra'],
                        compra_row['Nr do Item na Nfe da Compra'],
                        compra_row['Codigo do Produto'],
                        compra_row['BCST Unitaria'],
                        diferenca_valores,
                        guardar_calculo_icmsst,
                        '201906'
                    ]

                nova_linha = pd.DataFrame([dados_calculo])
                #resultado_df = pd.concat([resultado_df, nova_linha], ignore_index=True, sort=False)

                # Incrementa o sequencial da linha
                sequencial_linha += 1

                # Salva o DataFrame resultado_df em um arquivo CSV
                nova_linha.to_csv('resultado.csv', index=False, header=False, sep=';', decimal=',', encoding='utf-8', mode='a')

                x = round(guardar_calculo_icmsst + x, 2)


            line3 =  [
                'E', (sequencial_linha - 1), x
            ]

            resultado_df_line3 = pd.DataFrame([line3])

            resultado_df_line3.to_csv('resultado.csv', index=False, header=False, sep=';', decimal=',', encoding='utf-8', mode='a')


            # Se tudo ocorreu bem
            barra_progresso["value"] = 100
            

            messagebox.showinfo("Sucesso", "O cálculo foi realizado com sucesso e o arquivo resultado.csv foi criado.")
            time.sleep(0.5)
            
            if x > 0:
                messagebox.showinfo("Valor", f"Valor a receber {x}")
                texto_resultado_final = f"Valor a receber: {x}\n"
                time.sleep(0.5)
            else:
                x = x * -1
                messagebox.showinfo("Valor", f"Valor a pagar {x}")
                texto_resultado_final = f"Valor a pagar: {x}\n"
                time.sleep(0.5)
            barra_progresso["value"] = 0
            
            resultado_texto = f"Relatório do cálculo ICMS-ST:\nTotal a receber/pagar: {x}\nOutros resultados desejados...\n"
            exibir_resultado(resultado_texto, texto_resultado_final)

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

# Classe principal que gerencia usuários
class UserManager:

    def __init__(self, root):
        self.root = root
        self.root.title("SysCalc")
        self.root.geometry("450x500")
        self.bg_color = "#f0f0f0"
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.root.configure(bg=self.bg_color)
        self.other_screens = [] # Lista para armazenar instâncias de "Outra Tela"
        self.notebook = ttk.Notebook(root)
        self.admin_logged_in = False



        # Frames para diferentes operações (Login, Registro, Edição, Exclusão)
        self.login_frame = self.create_frame("Login", self.bg_color)
        self.register_frame = self.create_frame("Register", self.bg_color)
        self.edit_frame = self.create_frame("Edit", self.bg_color)
        self.delete_frame = self.create_frame("Delete", self.bg_color)

        # Adicionar frames ao Notebook
        self.notebook.add(self.login_frame, text="Login")
        self.notebook.add(self.register_frame, text="Registro")
        self.notebook.add(self.edit_frame, text="Editar")
        self.notebook.add(self.delete_frame, text="Deletar")

        self.notebook.pack(expand=True, fill="both")
        
        # Criar widgets para cada frame
        self.create_widgets_login()
        self.create_widgets_register()
        self.create_widgets_edit()
        self.create_widgets_delete()
        
        # Inicialmente, ocultar as guias de "Editar" e "Deletar"
        self.notebook.tab(2, state="hidden")
        self.notebook.tab(3, state="hidden")

        # Criar o arquivo users.csv se não existir
        self.create_users_file()


    # Função para criar e retornar um frame com o título e cor de fundo fornecidos
    def create_frame(self, title, bg_color):
        frame = Frame(self.notebook, bg=bg_color)
        return frame


    # Função para criar widgets relacionados ao frame de login
    def create_widgets_login(self):
        login_username_label = Label(
            self.login_frame, text="Nome de usuário:", bg=self.bg_color)
        self.login_username_entry = Entry(self.login_frame)
        login_password_label = Label(
            self.login_frame, text="Senha:", bg=self.bg_color)
        self.login_password_entry = Entry(self.login_frame, show="*")
        login_submit_button = ttk.Button(
            self.login_frame, text="Login", command=self.login)
        login_label = Label(self.login_frame, bg=self.bg_color)

        login_username_label.pack(pady=5)
        self.login_username_entry.pack(pady=5)
        login_password_label.pack(pady=5)
        self.login_password_entry.pack(pady=5)
        login_submit_button.pack(pady=10)
        login_label.pack()


    # Função para criar widgets relacionados ao frame de registro
    def create_widgets_register(self):
        register_username_label = Label(
            self.register_frame, text="Nome de usuário:", bg=self.bg_color)
        self.register_username_entry = Entry(self.register_frame)
        register_password_label = Label(
            self.register_frame, text="Senha:", bg=self.bg_color)
        self.register_password_entry = Entry(
            self.register_frame, show="*")
        register_submit_button = ttk.Button(
            self.register_frame, text="Registrar", command=self.register)

        register_username_label.pack(pady=5)
        self.register_username_entry.pack(pady=5)
        register_password_label.pack(pady=5)
        self.register_password_entry.pack(pady=5)
        register_submit_button.pack(pady=10)


    # Função para criar widgets relacionados ao frame de edição
    def create_widgets_edit(self):
        self.edit_listbox = Listbox(self.edit_frame)
        edit_listbox_update_button = ttk.Button(
            self.edit_frame, text="Atualizar lista", command=self.update_edit_listbox)
        self.edit_username_label = Label(
            self.edit_frame, text="Novo nome de usuário:", bg=self.bg_color)
        self.edit_username_entry = Entry(self.edit_frame)
        self.edit_password_label = Label(
            self.edit_frame, text="Nova senha:", bg=self.bg_color)
        self.edit_password_entry = Entry(
            self.edit_frame, show="*")
        edit_submit_button = ttk.Button(
            self.edit_frame, text="Editar", command=self.edit)

        self.edit_listbox.pack(pady=5)
        edit_listbox_update_button.pack(pady=5)
        self.edit_username_label.pack(pady=5)
        self.edit_username_entry.pack(pady=5)
        self.edit_password_label.pack(pady=5)
        self.edit_password_entry.pack(pady=5)
        edit_submit_button.pack(pady=10)


    # Função para criar widgets relacionados ao frame de exclusão
    def create_widgets_delete(self):
        self.delete_listbox = Listbox(self.delete_frame)
        delete_listbox_update_button = ttk.Button(
            self.delete_frame, text="Atualizar lista", command=self.update_delete_listbox)
        delete_submit_button = ttk.Button(
            self.delete_frame, text="Excluir", command=self.delete)

        self.delete_listbox.pack(pady=5)
        delete_listbox_update_button.pack(pady=5)
        delete_submit_button.pack(pady=10)


    # Função para criar o arquivo users.csv se não existir
    def create_users_file(self):
        if not os.path.exists("users.csv"):
            with open("users.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Username", "Password"])
            
    # Função para processar a operação de login
    def login(self):
        try:
            username = self.login_username_entry.get()
            password = self.login_password_entry.get()

            # Validar entrada
            if not (username and password):
                messagebox.showwarning("Aviso", "Preencha todos os campos.")
                return

            # Verificar se o usuário é administrador
            if username == admin_username and password == admin_password:
                self.show_admin_features()
                self.admin_logged_in = True
                return

            # Verificar credenciais do usuário
            if self.validate_user_credentials(username, password):
                self.login_username_entry.delete(0, END)
                self.login_password_entry.delete(0, END)
                messagebox.showinfo("Sucesso", "Login bem-sucedido!")

                # Abra a nova tela após o login
                funcao_segundo_script()
                return

            self.login_username_entry.delete(0, END)
            self.login_password_entry.delete(0, END)
            messagebox.showwarning("Aviso", "Falha no login. Tente novamente.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao fazer login: {str(e)}")


    # Função para processar a operação de registro
    def register(self):
        try:
            username = self.register_username_entry.get()
            password = self.register_password_entry.get()

            # Validar entrada
            if not (username and password):
                messagebox.showwarning("Aviso", "Preencha todos os campos.")
                return

            # Validar senha forte
            if not self.is_strong_password(password):
                messagebox.showwarning(
                    "Aviso", "A senha deve ter pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas, números e caracteres especiais.")
                return

            # Verificar se o usuário já existe
            if self.user_exists(username):
                messagebox.showwarning(
                    "Aviso", "Este nome de usuário já está em uso. Escolha outro.")
                return

            # Criptografar a senha
            hashed_password = self.hash_password(password)

            # Registrar usuário
            with open("users.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([username, hashed_password])

            messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")
            self.register_username_entry.delete(0, END)
            self.register_password_entry.delete(0, END)
        except Exception as e:
            messagebox.showerror(
                "Erro", f"Erro ao registrar usuário: {str(e)}")

    # Função para atualizar a caixa de listagem no frame de edição
    def update_edit_listbox(self):
        try:
            self.edit_listbox.delete(0, END)
            with open("users.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:
                        self.edit_listbox.insert(END, row[0])
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar lista: {str(e)}")

    # Função para atualizar a caixa de listagem no frame de exclusão
    def update_delete_listbox(self):
        try:
            self.delete_listbox.delete(0, END)
            with open("users.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:
                        self.delete_listbox.insert(END, row[0])
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar lista: {str(e)}")

    # Função para processar a operação de edição
    def edit(self):
        try:
            selected_user = self.edit_listbox.get(ACTIVE)
            new_username = self.edit_username_entry.get()
            new_password = self.edit_password_entry.get()

            # Validar entrada
            if not (selected_user and new_username and new_password):
                messagebox.showwarning(
                    "Aviso", "Selecione um usuário e preencha todos os campos.")
                return

            # Validar senha forte
            if not self.is_strong_password(new_password):
                messagebox.showwarning(
                    "Aviso", "A nova senha deve ter pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas, números e caracteres especiais.")
                return

            with open("users.csv", "r") as file:
                reader = csv.reader(file)
                rows = list(reader)

            with open("users.csv", "w", newline="") as file:
                writer = csv.writer(file)
                for row in rows:
                    if row and row[0] == selected_user:
                        writer.writerow(
                            [new_username, self.hash_password(new_password)])
                    else:
                        writer.writerow(row)

            self.edit_username_entry.delete(0, END)
            self.edit_password_entry.delete(0, END)
            self.update_edit_listbox()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao editar usuário: {str(e)}")
    
    # Função para processar a operação de exclusão
    def delete(self):
        try:
            selected_user = self.delete_listbox.get(ACTIVE)

            # Validar entrada
            if not selected_user:
                messagebox.showwarning("Aviso", "Selecione um usuário.")
                return

            with open("users.csv", "r") as file:
                reader = csv.reader(file)
                rows = list(reader)

            with open("users.csv", "w", newline="") as file:
                writer = csv.writer(file)
                for row in rows:
                    if row and row[0] != selected_user:
                        writer.writerow(row)

            self.update_delete_listbox()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir usuário: {str(e)}")

    # Função para exibir recursos específicos do administrador
    def show_admin_features(self):
        try:
            current_tab_index = self.notebook.index(self.notebook.select())
            self.notebook.tab(2, state="normal")  # Mostrar a guia "Edit"
            self.notebook.tab(3, state="normal")  # Mostrar a guia "Delete"
            self.notebook.select(current_tab_index)  # Manter a guia ativa
            messagebox.showinfo("Informação", "Logado como administrador")
            # Adicione aqui as funcionalidades específicas do administrador
        except Exception as e:
            messagebox.showerror(
                "Erro", f"Erro ao exibir funcionalidades do administrador: {str(e)}")

    # Função para efetuar logout
    def logout(self):
        try:
            # Verificar se o usuário está realmente logado
            if not self.admin_logged_in:
                messagebox.showinfo("Aviso", "Você não está logado.")
                return

            self.notebook.tab(2, state="hidden")
            self.notebook.tab(3, state="hidden")
            self.show_frame(self.login_frame)
            messagebox.showinfo("Sucesso", "Deslogado com sucesso!")
            self.admin_logged_in = False  # Atualizar o status de login do administrador
        except Exception as e:
            messagebox.showerror("Erro ao fazer logout", str(e))

    # Função para fechar a aplicação
    def exit_application(self):
            try:
                if self.root and self.root.winfo_exists():  # Verifica se a janela principal ainda existe
                    # Remover instâncias de "Outra Tela" que foram fechadas
                    self.remove_closed_screens()

                    # Fechar todas as janelas abertas, incluindo "Outra Tela"
                    for window in self.root.winfo_children():
                        if window and window.winfo_exists():  # Verifica se a janela ainda existe
                            window.destroy()

                    # Fechar instâncias de "Outra Tela" que podem ter sido abertas novamente
                    for other_screen in self.other_screens:
                        if other_screen and other_screen.winfo_exists():  # Verifica se a janela ainda existe
                            other_screen.destroy()

                    resposta = messagebox.askyesno("Confirmação", "Você deseja sair?")
                    if resposta and self.root and self.root.winfo_exists():  # Verifica se a janela principal ainda existe
                        self.root.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao fechar aplicativo: {str(e)}")

# ... (restante do código)



    # Função chamada ao fechar a instância de "Outra Tela"
    def on_close_other_screen(self, other_screen):
        self.other_screens.remove(other_screen)
        other_screen.destroy()

    # Função para remover instâncias de "Outra Tela" que foram fechadas
    def remove_closed_screens(self):
        closed_screens = [screen for screen in self.other_screens if not screen.winfo_exists()]
        for closed_screen in closed_screens:
            self.other_screens.remove(closed_screen)

    # Função para mostrar um determinado frame no Notebook
    def show_frame(self, frame):
        frame.tkraise()

    # Função para verificar se uma senha é forte
    def is_strong_password(self, password):
        return (
            len(password) >= 8 and
            re.search("[a-z]", password) and
            re.search("[A-Z]", password) and
            re.search("[0-9]", password) and
            re.search("[!@#$%^&*(),.?\":{}|<>]", password)
        )

    # Função para gerar o hash de uma senha usando o algoritmo SHA-256
    def hash_password(self, password):
        sha256 = hashlib.sha256()
        sha256.update(password.encode("utf-8"))
        return sha256.hexdigest()

    # Função para verificar se um usuário já existe no arquivo users.csv
    def user_exists(self, username):
        with open("users.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == username:
                    return True
        return False

    # Função para validar as credenciais de um usuário durante o login
    def validate_user_credentials(self, username, password):
        with open("users.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == username and row[1] == self.hash_password(password):
                    return True
        return False


# Ponto de entrada do programa
if __name__ == "__main__":
    admin_username = "admin"
    admin_password = "admin123"

    root = Tk()
    userManager = UserManager(root)

    # Adicione botões de "Sair" e "Deslogar"
    logout_button = ttk.Button(
        root, text="Deslogar", command=userManager.logout)
    logout_button.pack(side=LEFT, pady=5)

    exit_button = ttk.Button(
        root, text="Sair", command=userManager.exit_application)
    exit_button.pack(side=RIGHT, pady=5)

    # Configurar tratamento de erro para fechar aplicativo
    root.protocol("WM_DELETE_WINDOW", userManager.exit_application)

    root.mainloop()
