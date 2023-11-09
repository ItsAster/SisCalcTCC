from tkinter import *
from tkinter import ttk, messagebox
import csv
import hashlib
import re
import subprocess


# Função para alternar entre os frames
def show_frame(frame):
    frame.tkraise()

# Função para atualizar a lista de usuários no frame de edição
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

# Função para atualizar a lista de usuários no frame de exclusão
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

# Função para registrar um novo usuário
def register():
    try:
        username = register_username_entry.get()
        password = register_password_entry.get()

        # Validar entrada
        if not (username and password):
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        # Validar senha forte
        if not is_strong_password(password):
            messagebox.showwarning(
                "Aviso", "A senha deve ter pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas, números e caracteres especiais.")
            return

        # Verificar se o usuário já existe
        if user_exists(username):
            messagebox.showwarning(
                "Aviso", "Este nome de usuário já está em uso. Escolha outro.")
            return

        # Criptografar a senha
        hashed_password = hash_password(password)

        # Registrar usuário
        with open("users.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([username, hashed_password])

        messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")
        register_username_entry.delete(0, END)
        register_password_entry.delete(0, END)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao registrar usuário: {str(e)}")

# Função para realizar o login
def login():
    try:
        username = login_username_entry.get()
        password = login_password_entry.get()

        # Validar entrada
        if not (username and password):
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        # Verificar se o usuário é administrador
        if username == admin_username and password == admin_password:
            show_admin_features()
            return

        # Verificar credenciais do usuário
        if validate_user_credentials(username, password):
            login_username_entry.delete(0, END)
            login_password_entry.delete(0, END)
            login_label.config(text="Login bem-sucedido!")

            # Chamar a função para abrir outro script Python
            open_another_script()

            return

        login_username_entry.delete(0, END)
        login_password_entry.delete(0, END)
        login_label.config(text="Falha no login. Tente novamente.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao fazer login: {str(e)}")

def open_another_script():
    try:
        # Substitua "path/to/your/script.py" pelo caminho do seu script Python
        subprocess.Popen(["python", "C:\\Users\\Edu_a\\Desktop\\SisCalc\\SisCalcEstoque.py"])
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao abrir outro script: {str(e)}")        


# Função para exibir funcionalidades específicas do administrador
def show_admin_features():
    try:
        notebook.tab(2, state="normal")  # Mostrar a guia "Edit"
        notebook.tab(3, state="normal")  # Mostrar a guia "Delete"
        messagebox.showinfo("Informação", "Logado como administrador")
        # Adicione aqui as funcionalidades específicas do administrador
    except Exception as e:
        messagebox.showerror(
            "Erro", f"Erro ao exibir funcionalidades do administrador: {str(e)}")

# Função para editar um usuário
def edit():
    try:
        selected_user = edit_listbox.get(ACTIVE)
        new_username = edit_username_entry.get()
        new_password = edit_password_entry.get()

        # Validar entrada
        if not (selected_user and new_username and new_password):
            messagebox.showwarning(
                "Aviso", "Selecione um usuário e preencha todos os campos.")
            return

        # Validar senha forte
        if not is_strong_password(new_password):
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
                        [new_username, hash_password(new_password)])
                else:
                    writer.writerow(row)

        edit_username_entry.delete(0, END)
        edit_password_entry.delete(0, END)
        update_edit_listbox()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao editar usuário: {str(e)}")

# Função para excluir um usuário
def delete():
    try:
        selected_user = delete_listbox.get(ACTIVE)

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

        update_delete_listbox()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao excluir usuário: {str(e)}")

# Função para fazer o logout
def logout():
    try:
        notebook.tab(2, state="hidden")  # Ocultar a guia "Edit"
        notebook.tab(3, state="hidden")  # Ocultar a guia "Delete"
        show_frame(login_frame)
        messagebox.showinfo("Sucesso", "Deslogado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro ao fazer logout", str(e))

# Função para fechar o aplicativo
def exit_application():
    try:
        resposta = messagebox.askyesno("Confirmação", "Você deseja sair?")
        if resposta:
            root.destroy()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao fechar aplicativo: {str(e)}")

# Função para verificar se a senha é forte
def is_strong_password(password):
    # Validar se a senha é forte (pelo menos 8 caracteres, letras maiúsculas, minúsculas, números e caracteres especiais)
    return (
        len(password) >= 8 and
        re.search("[a-z]", password) and
        re.search("[A-Z]", password) and
        re.search("[0-9]", password) and
        re.search("[!@#$%^&*(),.?\":{}|<>]", password)
    )

# Função para criptografar a senha
def hash_password(password):
    # Criptografar a senha antes de armazenar
    sha256 = hashlib.sha256()
    sha256.update(password.encode("utf-8"))
    return sha256.hexdigest()

# Função para verificar se o usuário já existe
def user_exists(username):
    # Verificar se o usuário já existe
    with open("users.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == username:
                return True
    return False

# Função para validar as credenciais do usuário
def validate_user_credentials(username, password):
    # Verificar se as credenciais do usuário são válidas
    with open("users.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == username and row[1] == hash_password(password):
                return True
    return False


# Nome de usuário e senha do administrador (ajuste conforme necessário)
admin_username = "admin"
admin_password = "admin123"

# Configuração da janela principal
root = Tk()
root.title("SysCalc")
root.geometry("450x500")
style = ttk.Style()

style.theme_use("clam")  # Use um tema de sua escolha

# Cor de fundo
bg_color = "#f0f0f0"
root.configure(bg=bg_color)

# Criar notebook
notebook = ttk.Notebook(root)

# Criar frames
login_frame = Frame(notebook, bg=bg_color)
register_frame = Frame(notebook, bg=bg_color)
edit_frame = Frame(notebook, bg=bg_color)
delete_frame = Frame(notebook, bg=bg_color)

# Adicionar frames ao notebook
notebook.add(login_frame, text="Login")
notebook.add(register_frame, text="Register")
notebook.add(edit_frame, text="Edit")
notebook.add(delete_frame, text="Delete")

notebook.pack(expand=True, fill="both")

# Colocar widgets na tela - Frame Login
login_username_label = Label(login_frame, text="Nome de usuário:", bg=bg_color)
login_username_entry = Entry(login_frame)
login_password_label = Label(login_frame, text="Senha:", bg=bg_color)
login_password_entry = Entry(login_frame, show="*")
login_submit_button = ttk.Button(login_frame, text="Login", command=login)
login_label = Label(login_frame, bg=bg_color)

login_username_label.pack(pady=5)
login_username_entry.pack(pady=5)
login_password_label.pack(pady=5)
login_password_entry.pack(pady=5)
login_submit_button.pack(pady=10)
login_label.pack()

# Colocar widgets na tela - Frame Register
register_username_label = Label(
    register_frame, text="Nome de usuário:", bg=bg_color)
register_username_entry = Entry(register_frame)
register_password_label = Label(register_frame, text="Senha:", bg=bg_color)
register_password_entry = Entry(register_frame, show="*")
register_submit_button = ttk.Button(
    register_frame, text="Registrar", command=register)

register_username_label.pack(pady=5)
register_username_entry.pack(pady=5)
register_password_label.pack(pady=5)
register_password_entry.pack(pady=5)
register_submit_button.pack(pady=10)

# Colocar widgets na tela - Frame Edit
edit_listbox = Listbox(edit_frame)
edit_listbox_update_button = ttk.Button(
    edit_frame, text="Atualizar lista", command=update_edit_listbox)
edit_username_label = Label(
    edit_frame, text="Novo nome de usuário:", bg=bg_color)
edit_username_entry = Entry(edit_frame)
edit_password_label = Label(edit_frame, text="Nova senha:", bg=bg_color)
edit_password_entry = Entry(edit_frame, show="*")
edit_submit_button = ttk.Button(edit_frame, text="Editar", command=edit)

edit_listbox.pack(pady=5)
edit_listbox_update_button.pack(pady=5)
edit_username_label.pack(pady=5)
edit_username_entry.pack(pady=5)
edit_password_label.pack(pady=5)
edit_password_entry.pack(pady=5)
edit_submit_button.pack(pady=10)

# Colocar widgets na tela - Frame Delete
delete_listbox = Listbox(delete_frame)
delete_listbox_update_button = ttk.Button(
    delete_frame, text="Atualizar lista", command=update_delete_listbox)
delete_submit_button = ttk.Button(delete_frame, text="Excluir", command=delete)

delete_listbox.pack(pady=5)
delete_listbox_update_button.pack(pady=5)
delete_submit_button.pack(pady=10)

# Adicionar botões de logout e sair
logout_button = ttk.Button(root, text="Deslogar", command=logout)
logout_button.pack(side=LEFT, pady=5)
exit_button = ttk.Button(root, text="Sair", command=exit_application)
exit_button.pack(side=RIGHT, pady=5)

# Configurar tratamento de erro para fechar aplicativo
root.protocol("WM_DELETE_WINDOW", exit_application)

# Ocultar as guias "Edit" e "Delete" inicialmente
notebook.tab(2, state="hidden")
notebook.tab(3, state="hidden")

# Iniciar o loop principal
root.mainloop()
