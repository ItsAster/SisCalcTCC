from tkinter import *
from tkinter import ttk, messagebox
import csv

def show_frame(frame):
    frame.tkraise()

def update_edit_listbox():
    try:
        edit_listbox.delete(0, END)
        with open("users.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    edit_listbox.insert(END, row[0])
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao atualizar lista: {str(e)}")

def update_delete_listbox():
    try:
        delete_listbox.delete(0, END)
        with open("users.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    delete_listbox.insert(END, row[0])
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao atualizar lista: {str(e)}")

def register():
    try:
        with open("users.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([register_username_entry.get(), register_password_entry.get()])
        register_username_entry.delete(0, END)
        register_password_entry.delete(0, END)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao registrar usuário: {str(e)}")

def login():
    try:
        username = login_username_entry.get()
        password = login_password_entry.get()

        # Verificar se é o usuário administrador
        if username == admin_username and password == admin_password:
            show_admin_features()
            return

        with open("users.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == username and row[1] == password:
                    login_username_entry.delete(0, END)
                    login_password_entry.delete(0, END)
                    login_label.config(text="Login bem-sucedido!")
                    return
        login_username_entry.delete(0, END)
        login_password_entry.delete(0, END)
        login_label.config(text="Falha no login. Tente novamente.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao fazer login: {str(e)}")

def show_admin_features():
    try:
        notebook.tab(2, state="normal")  # Mostrar a guia "Edit"
        notebook.tab(3, state="normal")  # Mostrar a guia "Delete"
        messagebox.showinfo("Informação", "Logado como administrador")
        # Adicione aqui as funcionalidades específicas do administrador
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao exibir funcionalidades do administrador: {str(e)}")

def edit():
    try:
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
        update_edit_listbox()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao editar usuário: {str(e)}")

def delete():
    try:
        selected_user = delete_listbox.get(ACTIVE)
        with open("users.csv", "r") as file:
            reader = csv.reader(file)
            rows = list(reader)
        with open("users.csv", "w", newline="") as file:
            writer = csv.writer(file)
            for row in rows:
                if row and row[0] != selected_user:
                    writer.writerow(row)
        update_delete_listbox()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao excluir usuário: {str(e)}")

def logout():
    try:
        notebook.tab(2, state="hidden")  # Ocultar a guia "Edit"
        notebook.tab(3, state="hidden")  # Ocultar a guia "Delete"
        show_frame(login_frame)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao fazer logout: {str(e)}")

def exit_application():
    try:
        resposta = messagebox.askyesno("Confirmação", "Você deseja sair?")
        if resposta:
            root.destroy()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao fechar aplicativo: {str(e)}")

# Nome de usuário e senha do administrador (ajuste conforme necessário)
admin_username = "admin"
admin_password = "admin123"

root = Tk()
root.title("SysCalc")
root.geometry("450x500")
style = ttk.Style()
style.theme_use("default")

# Criar notebook
notebook = ttk.Notebook(root)

# Criar frames
login_frame = Frame(notebook)
register_frame = Frame(notebook)
edit_frame = Frame(notebook)
delete_frame = Frame(notebook)

# Adicionar frames ao notebook
notebook.add(login_frame, text="Login")
notebook.add(register_frame, text="Register")
notebook.add(edit_frame, text="Edit")
notebook.add(delete_frame, text="Delete")

notebook.pack(expand=True, fill="both")

# Colocar widgets na tela - Frame Login
login_username_label = Label(login_frame, text="Nome de usuário:")
login_username_entry = Entry(login_frame)
login_password_label = Label(login_frame, text="Senha:")
login_password_entry = Entry(login_frame, show="*")
login_submit_button = ttk.Button(login_frame, text="Login", command=login)
login_label = Label(login_frame)

login_username_label.pack()
login_username_entry.pack()
login_password_label.pack()
login_password_entry.pack()
login_submit_button.pack()
login_label.pack()

# Colocar widgets na tela - Frame Register
register_username_label = Label(register_frame, text="Nome de usuário:")
register_username_entry = Entry(register_frame)
register_password_label = Label(register_frame, text="Senha:")
register_password_entry = Entry(register_frame, show="*")
register_submit_button = ttk.Button(register_frame, text="Registrar", command=register)

register_username_label.pack()
register_username_entry.pack()
register_password_label.pack()
register_password_entry.pack()
register_submit_button.pack()

# Colocar widgets na tela - Frame Edit
edit_listbox = Listbox(edit_frame)
edit_listbox_update_button = ttk.Button(edit_frame, text="Atualizar lista", command=update_edit_listbox)
edit_username_label = Label(edit_frame, text="Novo nome de usuário:")
edit_username_entry = Entry(edit_frame)
edit_password_label = Label(edit_frame, text="Nova senha:")
edit_password_entry = Entry(edit_frame, show="*")
edit_submit_button = ttk.Button(edit_frame, text="Editar", command=edit)

edit_listbox.pack()
edit_listbox_update_button.pack()
edit_username_label.pack()
edit_username_entry.pack()
edit_password_label.pack()
edit_password_entry.pack()
edit_submit_button.pack()

# Colocar widgets na tela - Frame Delete
delete_listbox = Listbox(delete_frame)
delete_listbox_update_button = ttk.Button(delete_frame, text="Atualizar lista", command=update_delete_listbox)
delete_submit_button = ttk.Button(delete_frame, text="Excluir", command=delete)

delete_listbox.pack()
delete_listbox_update_button.pack()
delete_submit_button.pack()

# Adicionar botões de logout e sair
logout_button = ttk.Button(root, text="Deslogar", command=logout)
logout_button.pack(side=LEFT, padx=5)
exit_button = ttk.Button(root, text="Sair", command=exit_application)
exit_button.pack(side=RIGHT, padx=5)

# Configurar tratamento de erro para fechar aplicativo
root.protocol("WM_DELETE_WINDOW", exit_application)

# Ocultar as guias "Edit" e "Delete" inicialmente
notebook.tab(2, state="hidden")
notebook.tab(3, state="hidden")

root.mainloop()
