import csv
from tkinter import *

root = Tk()
root.title("Aplicativo de Estoque e Vendas")

# Função para registrar informações de compra
def register_purchase():
    with open("compras.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([purchase_code_entry.get(), purchase_product_code_entry.get(), purchase_value_entry.get(), purchase_quantity_entry.get(), purchase_total_value_label["text"]])
    purchase_code_entry.delete(0, END)
    purchase_product_code_entry.delete(0, END)
    purchase_value_entry.delete(0, END)
    purchase_quantity_entry.delete(0, END)

# Função para registrar informações de venda
def register_sale():
    with open("vendas.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([sale_code_entry.get(), sale_product_code_entry.get(), sale_value_entry.get(), sale_quantity_entry.get(), sale_total_value_label["text"]])
    sale_code_entry.delete(0, END)
    sale_product_code_entry.delete(0, END)
    sale_value_entry.delete(0, END)
    sale_quantity_entry.delete(0, END)

# Função para calcular o valor total da compra
def calculate_purchase_total_value(*args):
    try:
        value = float(purchase_value_var.get())
        quantity = float(purchase_quantity_var.get())
        total_value = value * quantity
        purchase_total_value_label.config(text=f"{total_value:.2f}")
    except:
        purchase_total_value_label.config(text="")

# Função para calcular o valor total da venda
def calculate_sale_total_value(*args):
    try:
        value = float(sale_value_var.get())
        quantity = float(sale_quantity_var.get())
        total_value = value * quantity
        sale_total_value_label.config(text=f"{total_value:.2f}")
    except:
        sale_total_value_label.config(text="")

# Função para atualizar a lista de compras na tela de comparação
def update_compare_purchase_listbox():
    compare_purchase_listbox.delete(0, END)
    with open("compras.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                compare_purchase_listbox.insert(END, f"{row[0]} - {row[4]}")

# Função para atualizar a lista de vendas na tela de comparação
def update_compare_sale_listbox():
    compare_sale_listbox.delete(0, END)
    with open("vendas.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                compare_sale_listbox.insert(END, f"{row[0]} - {row[4]}")

# Função para comparar uma venda selecionada com uma compra selecionada purchase_product_code_entry
def compare():
    selected_purchase = compare_purchase_listbox.get(ACTIVE)
    selected_sale = compare_sale_listbox.get(ACTIVE)

    if not selected_purchase or not selected_sale:
        compare_result_label.config(text="Selecione uma compra e uma venda para comparar.")
        return

    purchase_values = selected_purchase.split(" - ")
    sale_values = selected_sale.split(" - ")

    if len(purchase_values) < 2 or len(sale_values) < 2:
        compare_result_label.config(text="Formato inválido para compra ou venda.")
        return

    purchase_product_number, purchase_value = purchase_values[0], float(purchase_values[1])
    sale_product_number, sale_value = sale_values[0], float(sale_values[1])

    if purchase_product_number == sale_product_number:
        difference = sale_value - purchase_value
        compare_result_label.config(text=f"Diferença para o Produto {purchase_product_number}: {difference:.2f}")
    else:
        compare_result_label.config(text="Números de produto diferentes, não é possível comparar.")



# Criar variáveis ​​StringVar para entradas de valor e quantidade
purchase_value_var = StringVar()
purchase_quantity_var = StringVar()
sale_value_var = StringVar()
sale_quantity_var = StringVar()

# Rastrear alterações nas entradas de valor e quantidade
purchase_value_var.trace_add("write", calculate_purchase_total_value)
purchase_quantity_var.trace_add("write", calculate_purchase_total_value)
sale_value_var.trace_add("write", calculate_sale_total_value)
sale_quantity_var.trace_add("write", calculate_sale_total_value)

# Criar widgets
purchase_label = Label(root, text="Registrar Compra")
purchase_code_label = Label(root, text="Código Nota:")
purchase_code_entry = Entry(root)
purchase_product_code_label = Label(root, text="Código Produto:")
purchase_product_code_entry = Entry(root)
purchase_value_label = Label(root, text="Valor por unidade:")
purchase_value_entry = Entry(root, textvariable=purchase_value_var)
purchase_quantity_label = Label(root, text="Quantidade:")
purchase_quantity_entry = Entry(root, textvariable=purchase_quantity_var)
purchase_total_value_label = Label(root, text="")
register_purchase_button = Button(root, text="Registrar Compra", command=register_purchase)

sale_label = Label(root, text="Registrar Venda")
sale_code_label = Label(root, text="Código Nota:")
sale_code_entry = Entry(root)
sale_product_code_label = Label(root, text="Código Produto:")
sale_product_code_entry = Entry(root)
sale_value_label = Label(root, text="Valor por unidade:")
sale_value_entry = Entry(root, textvariable=sale_value_var)
sale_quantity_label = Label(root, text="Quantidade:")
sale_quantity_entry = Entry(root, textvariable=sale_quantity_var)
sale_total_value_label = Label(root, text="")
register_sale_button = Button(root, text="Registrar Venda", command=register_sale)

compare_label = Label(root, text="Comparar")
compare_purchase_listbox = Listbox(root)
compare_purchase_listbox_update_button = Button(root, text="Atualizar lista de compras", command=update_compare_purchase_listbox)
compare_sale_listbox = Listbox(root)
compare_sale_listbox_update_button = Button(root, text="Atualizar lista de vendas", command=update_compare_sale_listbox)
compare_button = Button(root, text="Comparar", command=compare)
compare_result_label = Label(root)

# Colocar widgets na tela
purchase_label.grid(row=0,column=0,columnspan=2)
purchase_code_label.grid(row=1,column=0)
purchase_code_entry.grid(row=1,column=1)
purchase_product_code_label.grid(row=2,column=0)
purchase_product_code_entry.grid(row=2,column=1)
purchase_value_label.grid(row=3,column=0)
purchase_value_entry.grid(row=3,column=1)
purchase_quantity_label.grid(row=4,column=0)
purchase_quantity_entry.grid(row=4,column=1)
purchase_total_value_label.grid(row=5,column=0,columnspan=2)
register_purchase_button.grid(row=6,column=0,columnspan=2)

sale_label.grid(row=7,column=0,columnspan=2)
sale_code_label.grid(row=8,column=0)
sale_code_entry.grid(row=8,column=1)
sale_product_code_label.grid(row=9,column=0)
sale_product_code_entry.grid(row=9,column=1)
sale_value_label.grid(row=10,column=0)
sale_value_entry.grid(row=10,column=1)
sale_quantity_label.grid(row=11,column=0)
sale_quantity_entry.grid(row=11,column=1)
sale_total_value_label.grid(row=12,column=0,columnspan=2)
register_sale_button.grid(row=13,column=0,columnspan=2)

compare_label.grid(row=14,column=0,columnspan=2)
compare_purchase_listbox.grid(row=15,column=0,columnspan=2)
compare_purchase_listbox_update_button.grid(row=16,column=0,columnspan=2)
compare_sale_listbox.grid(row=17,column=0,columnspan=2)
compare_sale_listbox_update_button.grid(row=18,column=0,columnspan=2)
compare_button.grid(row=19,column=0,columnspan=2)
compare_result_label.grid(row=20,column=0,columnspan=2)

root.mainloop()
