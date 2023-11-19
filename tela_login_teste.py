import sqlite3
import os
from tkinter import Tk, Label, Entry, Button
from cadastro_produtos_teste import ProductsRegisterScreen

script_dir = os.path.dirname(os.path.abspath(__file__))
db_file_path = os.path.join(script_dir, "Projeto_Compras.db")
print(db_file_path)


class LoginScreen:
    def __init__(self, db_file_path):
        self.screen = Tk()
        self.screen.title("Tela de Login")
        self.screen.configure(bg="#F5F5F5")  # cor de fundo
        self.screen_width = 450
        self.screen_height = 300

        # obtem a largura e altura da tela do computador
        monitor_width = self.screen.winfo_screenwidth()
        monitor_height = self.screen.winfo_screenheight()

        # calcula a posição da janela para centraliza-la na tela
        pos_x = (monitor_width // 2) - (self.screen_width // 2)
        pos_y = (monitor_height // 2) - (self.screen_height // 2)

        self.screen.geometry('{}x{}+{}+{}'.format(self.screen_width, self.screen_height, pos_x, pos_y))

        self.db_file_path = db_file_path

        self.username_entry = Entry(self.screen, font="Calibri 12")
        self.username_entry.grid(row=1, column=1, padx=10)

        self.password_entry = Entry(self.screen, show="*", font="Calibri 12")
        self.password_entry.grid(row=2, column=1, padx=10)

        title_lbl = Label(self.screen, text="Tela de Login", font="Calibri 24", fg="blue", bg="#F5F5F5")
        title_lbl.grid(row=0, column=0, columnspan=2, pady=20)  # pady = espaço em relação ao eixo y (altura)

        username_lbl = Label(self.screen, text="Nome de usuário", font="Calibri 14 bold", bg="#F5F5F5")
        username_lbl.grid(row=1, column=0, stick="E")

        password_lbl = Label(self.screen, text="Senha", font="Calibri 14 bold", bg="#F5F5F5")
        password_lbl.grid(row=2, column=0, stick="E")

        login_btn = Button(self.screen, text="Entrar", font="Calibri 14", command=self.verify_credentials)
        login_btn.grid(row=4, column=0, columnspan=2, padx=20, pady=10, stick="NSEW")

        logout_btn = Button(self.screen, text="Sair", font="Calibri 14", command=self.screen.destroy)
        logout_btn.grid(row=5, column=0, columnspan=2, padx=20, pady=10, stick="NSEW")

        for i in range(5):
            self.screen.grid_rowconfigure(i, weight=1)

        for i in range(2):
            self.screen.grid_columnconfigure(i, weight=1)

    def verify_credentials(self):
        conexao = sqlite3.connect(self.db_file_path)
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM Usuarios WHERE Nome = ? AND Senha = ?", (self.username_entry.get(), self.password_entry.get()))

        user = cursor.fetchone()

        if user:
            self.screen.destroy()
            self.show_products_register_screen()
        else:
            message_lbl = Label(self.screen, text="Nome de usuário ou senha incorretos", font="Calibri 14", fg="red")
            message_lbl.grid(row=3, column=0, columnspan=2)
    
    def show_products_register_screen(self):
        productsScreen = ProductsRegisterScreen(self.db_file_path)
        productsScreen.run()
        
    def run(self):
        self.screen.mainloop()

if __name__ == "__main__":
    login_screen = LoginScreen("Projeto_Compras.db")
    login_screen.run()
