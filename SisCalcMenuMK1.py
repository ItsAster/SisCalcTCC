import os
import csv
import hashlib
import re
from tkinter import *
from tkinter import ttk, messagebox

class OtherScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Outra Tela")
        self.master.geometry("300x200")

        label = Label(master, text="Esta é outra tela.")
        label.pack(pady=20)

class UserManager:

    def __init__(self, root):
        self.root = root
        self.root.title("SysCalc")
        self.root.geometry("450x500")
        self.bg_color = "#f0f0f0"
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.root.configure(bg=self.bg_color)
        self.other_screens = []

        

        self.notebook = ttk.Notebook(root)

        self.login_frame = self.create_frame("Login", self.bg_color)
        self.register_frame = self.create_frame("Register", self.bg_color)
        self.edit_frame = self.create_frame("Edit", self.bg_color)
        self.delete_frame = self.create_frame("Delete", self.bg_color)

        self.notebook.add(self.login_frame, text="Login")
        self.notebook.add(self.register_frame, text="Registro")
        self.notebook.add(self.edit_frame, text="Editar")
        self.notebook.add(self.delete_frame, text="Deletar")

        self.notebook.pack(expand=True, fill="both")

        self.create_widgets_login()
        self.create_widgets_register()
        self.create_widgets_edit()
        self.create_widgets_delete()

        self.notebook.tab(2, state="hidden")
        self.notebook.tab(3, state="hidden")

        # Criar o arquivo users.csv se não existir
        self.create_users_file()

    def create_frame(self, title, bg_color):
        frame = Frame(self.notebook, bg=bg_color)
        return frame

    def create_widgets_login(self):
        login_username_label = Label(self.login_frame, text="Nome de usuário:", bg=self.bg_color)
        self.login_username_entry = Entry(self.login_frame)
        login_password_label = Label(self.login_frame, text="Senha:", bg=self.bg_color)
        self.login_password_entry = Entry(self.login_frame, show="*")
        login_submit_button = ttk.Button(self.login_frame, text="Login", command=self.login)
        login_label = Label(self.login_frame, bg=self.bg_color)

        login_username_label.pack(pady=5)
        self.login_username_entry.pack(pady=5)
        login_password_label.pack(pady=5)
        self.login_password_entry.pack(pady=5)
        login_submit_button.pack(pady=10)
        login_label.pack()

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

    def create_widgets_delete(self):
        self.delete_listbox = Listbox(self.delete_frame)
        delete_listbox_update_button = ttk.Button(
            self.delete_frame, text="Atualizar lista", command=self.update_delete_listbox)
        delete_submit_button = ttk.Button(
            self.delete_frame, text="Excluir", command=self.delete)

        self.delete_listbox.pack(pady=5)
        delete_listbox_update_button.pack(pady=5)
        delete_submit_button.pack(pady=10)

    def create_users_file(self):
        if not os.path.exists("users.csv"):
            with open("users.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Username", "Password"])

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
                return

            # Verificar credenciais do usuário
            if self.validate_user_credentials(username, password):
                self.login_username_entry.delete(0, END)
                self.login_password_entry.delete(0, END)
                messagebox.showinfo("Sucesso", "Login bem-sucedido!")

                # Abra a nova tela após o login
                self.open_other_screen()
                return

            self.login_username_entry.delete(0, END)
            self.login_password_entry.delete(0, END)
            messagebox.showwarning("Aviso", "Falha no login. Tente novamente.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao fazer login: {str(e)}")

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
            messagebox.showerror("Erro", f"Erro ao registrar usuário: {str(e)}")

    def open_other_screen(self):
        other_screen = Tk()
        other_screen_instance = OtherScreen(other_screen)
        self.other_screens.append(other_screen)  # Adiciona instância à lista
        other_screen.protocol("WM_DELETE_WINDOW", other_screen.destroy)  # Adiciona tratamento de fechamento
        other_screen.mainloop()


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

    def show_admin_features(self):
        try:
            self.notebook.tab(2, state="normal")  # Mostrar a guia "Edit"
            self.notebook.tab(3, state="normal")  # Mostrar a guia "Delete"
            messagebox.showinfo("Informação", "Logado como administrador")
            # Adicione aqui as funcionalidades específicas do administrador
        except Exception as e:
            messagebox.showerror(
                "Erro", f"Erro ao exibir funcionalidades do administrador: {str(e)}")

    def logout(self):
        try:
            self.notebook.tab(2, state="hidden")  # Ocultar a guia "Edit"
            self.notebook.tab(3, state="hidden")  # Ocultar a guia "Delete"
            self.show_frame(self.login_frame)
            messagebox.showinfo("Sucesso", "Deslogado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro ao fazer logout", str(e))

    def exit_application(self):
        try:
            # Fechar todas as janelas abertas, incluindo "Outra Tela"
            for window in self.root.winfo_children():
                window.destroy()

            # Fechar instâncias de "Outra Tela"
            for other_screen in self.other_screens:
                other_screen.destroy()

            resposta = messagebox.askyesno("Confirmação", "Você deseja sair?")
            if resposta:
                self.root.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao fechar aplicativo: {str(e)}")


    def show_frame(self, frame):
        frame.tkraise()

    def is_strong_password(self, password):
        return (
            len(password) >= 8 and
            re.search("[a-z]", password) and
            re.search("[A-Z]", password) and
            re.search("[0-9]", password) and
            re.search("[!@#$%^&*(),.?\":{}|<>]", password)
        )

    def hash_password(self, password):
        sha256 = hashlib.sha256()
        sha256.update(password.encode("utf-8"))
        return sha256.hexdigest()

    def user_exists(self, username):
        with open("users.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == username:
                    return True
        return False

    def validate_user_credentials(self, username, password):
        with open("users.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == username and row[1] == self.hash_password(password):
                    return True
        return False

if __name__ == "__main__":
    admin_username = "admin"
    admin_password = "admin123"

    root = Tk()
    userManager = UserManager(root)

    # Adicione botões de "Sair" e "Deslogar"
    logout_button = ttk.Button(root, text="Deslogar", command=userManager.logout)
    logout_button.pack(side=LEFT, pady=5)

    exit_button = ttk.Button(root, text="Sair", command=userManager.exit_application)
    exit_button.pack(side=RIGHT, pady=5)

    # Configurar tratamento de erro para fechar aplicativo
    root.protocol("WM_DELETE_WINDOW", userManager.exit_application)

    root.mainloop()
           
