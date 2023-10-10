import csv
from tkinter import *
from tkinter import ttk, messagebox

root = Tk()
root.title("SysCalc")
root.geometry("450x500")
style = ttk.Style()
style.theme_use("default")

# Função para mostrar a tela de login
def show_login():
    register_frame.pack_forget()
    edit_frame.pack_forget()
    delete_frame.pack_forget()
    login_frame.pack()

# Função para mostrar a tela de registro
def show_register():
    login_frame.pack_forget()
    edit_frame.pack_forget()
    delete_frame.pack_forget()
    register_frame.pack()

# Função para mostrar a tela de edição
def show_edit():
    login_frame.pack_forget()
    register_frame.pack_forget()
    delete_frame.pack_forget()
    update_edit_listbox()
    edit_frame.pack()

# Função para mostrar a tela de exclusão
def show_delete():
    login_frame.pack_forget()
    register_frame.pack_forget()
    edit_frame.pack_forget()
    update_delete_listbox()
    delete_frame.pack()

# Função para atualizar a lista de usuários na tela de edição
def update_edit_listbox():
    edit_listbox.delete(0, END)
    with open("users.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                edit_listbox.insert(END, row[0])

# Função para atualizar a lista de usuários na tela de exclusão
def update_delete_listbox():
    delete_listbox.delete(0, END)
    with open("users.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                delete_listbox.insert(END, row[0])

# Função para registrar um novo usuário
def register():
    with open("users.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([register_username_entry.get(), register_password_entry.get()])
    register_username_entry.delete(0, END)
    register_password_entry.delete(0, END)

# Função para fazer login de um usuário existente
def login():
    with open("users.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == login_username_entry.get() and row[1] == login_password_entry.get():
                login_username_entry.delete(0, END)
                login_password_entry.delete(0, END)
                login_label.config(text="Login bem-sucedido!")
                return
    login_username_entry.delete(0, END)
    login_password_entry.delete(0, END)
    login_label.config(text="Falha no login. Tente novamente.")

# Função para editar as informações de um usuário existente
def edit():
    selected_user = edit_listbox.get(ACTIVE)
    with open("users.csv", "r") as file:
        reader = csv.reader(file)
        rows = list(reader)
    with open("users.csv", "w", newline="") as file:
        writer = csv.writer(file)
        for row in rows:
            if row and row[0] == selected_user:
                writer.writerow([edit_username_entry.get(), edit_password_entry.get()])
            else:
                writer.writerow(row)
    edit_username_entry.delete(0, END)
    edit_password_entry.delete(0, END)

# Função para excluir um usuário existente
def delete():
    selected_user = delete_listbox.get(ACTIVE)
    with open("users.csv", "r") as file:
        reader = csv.reader(file)
        rows = list(reader)
    with open("users.csv", "w", newline="") as file:
        writer = csv.writer(file)
        for row in rows:
            if row and row[0] != selected_user:
                writer.writerow(row)

# Função para fechar o aplicativo com confirmação
def fechar_aplicativo():
    resposta = messagebox.askyesno("Confirmação", "Você deseja sair?")
    if resposta:
        root.destroy()

# Criar widgets
main_frame = Frame(root)
login_button = ttk.Button(main_frame, text="Login", command=show_login)
register_button = ttk.Button(main_frame, text="Registrar", command=show_register)
edit_button = ttk.Button(main_frame, text="Editar", command=show_edit)
delete_button = ttk.Button(main_frame, text="Excluir", command=show_delete)
sair_button = ttk.Button(main_frame, text="Sair", command=fechar_aplicativo)

login_frame = Frame(root)
login_username_label = Label(login_frame, text="Nome de usuário:")
login_username_entry = Entry(login_frame)
login_password_label = Label(login_frame, text="Senha:")
login_password_entry = Entry(login_frame, show="*")
login_submit_button = ttk.Button(login_frame, text="Login", command=login)
login_label = Label(login_frame)

register_frame = Frame(root)
register_username_label = Label(register_frame, text="Nome de usuário:")
register_username_entry = Entry(register_frame)
register_password_label = Label(register_frame, text="Senha:")
register_password_entry = Entry(register_frame, show="*")
register_submit_button = ttk.Button(register_frame, text="Registrar", command=register)

edit_frame = Frame(root)
edit_listbox = Listbox(edit_frame)
edit_listbox_update_button = ttk.Button(edit_frame, text="Atualizar lista", command=update_edit_listbox)
edit_username_label = Label(edit_frame, text="Novo nome de usuário:")
edit_username_entry = Entry(edit_frame)
edit_password_label = Label(edit_frame, text="Nova senha:")
edit_password_entry = Entry(edit_frame, show="*")
edit_submit_button = ttk.Button(edit_frame, text="Editar", command=edit)

delete_frame = Frame(root)
delete_listbox = Listbox(delete_frame)
delete_listbox_update_button = ttk.Button(delete_frame, text="Atualizar lista", command=update_delete_listbox)
delete_submit_button = ttk.Button(delete_frame, text="Excluir", command=delete)

# Colocar widgets na tela
main_frame.pack()
login_button.pack()
register_button.pack()
edit_button.pack()
delete_button.pack()
sair_button.pack()

login_username_label.pack()
login_username_entry.pack()
login_password_label.pack()
login_password_entry.pack()
login_submit_button.pack()
login_label.pack()

register_username_label.pack()
register_username_entry.pack()
register_password_label.pack()
register_password_entry.pack()
register_submit_button.pack()

edit_listbox.pack()
edit_listbox_update_button.pack()
edit_username_label.pack()
edit_username_entry.pack()
edit_password_label.pack()
edit_password_entry.pack()
edit_submit_button.pack()

delete_listbox.pack()
delete_listbox_update_button.pack()
delete_submit_button.pack()

root.mainloop()