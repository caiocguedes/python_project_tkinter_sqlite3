import sqlite3
import os
from tkinter import *
from tkinter import ttk

class ProductsRegisterScreen:
    def __init__(self, db_file_path):
        self.connection = sqlite3.connect(db_file_path)
        self.cursor = self.connection.cursor()
        self.connection.execute("SELECT * FROM Produtos")

        print("Conectado")

        def connect_database():
            script_dir = os.path.dirname(os.path.abspath(__file__))
            db_file_path = os.path.join(script_dir, "Projeto_Compras.db")
            
            connection = sqlite3.connect(db_file_path)
            cursor = connection.cursor()
            connection.execute("SELECT * FROM Produtos")
            
            return connection, cursor

        def list_data():
            for i in treeview.get_children():
                treeview.delete(i)
            
            self.cursor.execute("SELECT * FROM Produtos")
            
            values = self.cursor.fetchall()
            
            for value in values:
                treeview.insert("", "end", values=(value[0], value[1], value[2], value[3],))

        self.screen = Tk()
        self.screen.title("Cadastro de Produtos")

        self.screen.configure(bg="#F5F5F5")
        self.screen.attributes("-fullscreen", True)

        Label(self.screen, text="Nome do Produto: ", font="Calibri 16", bg="#F5F5F5").grid(row=0, column=2, padx=10, pady=10)
        product_name_field = Entry(self.screen, font="Calibri 16")
        product_name_field.grid(row=0, column=3, padx=10, pady=10)

        Label(self.screen, text="Descrição do Produto: ", font="Calibri 16", bg="#F5F5F5").grid(row=0, column=5, padx=10, pady=10)
        product_description_field = Entry(self.screen, font="Calibri 16")
        product_description_field.grid(row=0, column=6, padx=10, pady=10)

        def cadastrar():
            register_screen = Toplevel(self.screen)
            register_screen.title("Cadastrar Produto")
            
            register_screen.configure(bg="#FFFFFF")
            screen_width = 450
            screen_height = 230

            monitor_width = register_screen.winfo_screenwidth()
            monitor_height = register_screen.winfo_screenheight()

            pos_x = (monitor_width//2) - (screen_width//2)
            pos_y = (monitor_height//2) - (screen_height//2)

            register_screen.geometry('{}x{}+{}+{}'.format(screen_width, screen_height, pos_x, pos_y))
            
            for i in range(5):
                register_screen.grid_rowconfigure(i, weight=1)

            for i in range(2):
                register_screen.grid_columnconfigure(i, weight=1)
            
            border_style = {"borderwidth":2, "relief":"groove"}
            
            Label(register_screen, text="Nome do produto:", font="Calibri 12", bg="#FFFFFF").grid(row=0, column=0, padx=10, pady=10, stick="W")
            product_name = Entry(register_screen, font="Calibri 12", **border_style)
            product_name.grid(row=0, column=1, padx=10, pady=10, stick="W")
            
            Label(register_screen, text="Descrição do produto:", font="Calibri 12", bg="#FFFFFF").grid(row=1, column=0, padx=10, pady=10, stick="W")
            product_description = Entry(register_screen, font="Calibri 12", **border_style)
            product_description.grid(row=1, column=1, padx=10, pady=10, stick="W")
            
            Label(register_screen, text="Preço do produto:", font="Calibri 12", bg="#FFFFFF").grid(row=2, column=0, padx=10, pady=10, stick="W")
            product_price = Entry(register_screen, font="Calibri 12", **border_style)
            product_price.grid(row=2, column=1, padx=10, pady=10, stick="W")
            
            def save_data():
                new_product = (product_name.get(), product_description.get(), product_price.get())
                
                self.cursor.execute("INSERT INTO Produtos (NomeProduto, Descricao, Preco) VALUES (?, ?, ?)", new_product)
                self.connection.commit()

                print("Dados cadastrados com sucesso")      
                
                register_screen.destroy()
                
                list_data()
            
            save_button = Button(register_screen, text="Salvar", font="Calibri 12", command=save_data)
            save_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, stick="NSEW")
            
            cancel_button = Button(register_screen, text="Cancelar", font="Calibri 12", command=register_screen.destroy)
            cancel_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, stick="NSEW")

        save_button = Button(self.screen, text="Novo", command=cadastrar, font="Calibri 26")
        save_button.grid(row=4, column=0, columnspan=4, stick="NSEW", pady=20, padx=20)

        style = ttk.Style(self.screen)
        treeview = ttk.Treeview(self.screen, style="mystyle.Treeview")
        style.theme_use("default")
        style.configure("mystyle.Treeview", font="Calibri 14")

        treeview = ttk.Treeview(self.screen, style="mystyle.Treeview", columns=("ID", "NomeProduto", "Descricao", "Preco"), show="headings", height=20)
        treeview.heading("ID", text="ID")
        treeview.heading("NomeProduto", text="Nome do Produto")
        treeview.heading("Descricao", text="Descrição do Produto")
        treeview.heading("Preco", text="Preço do Produto")
        treeview.column("#0", width=0, stretch=NO)
        treeview.column("ID", width=100, stretch=NO)
        treeview.column("NomeProduto", width=300, stretch=NO)
        treeview.column("Descricao", width=500, stretch=NO)
        treeview.column("Preco", width=200, stretch=NO)

        treeview.grid(row=3, column=0, columnspan=10, stick="NSEW")

        list_data()

        def edit_data(event):
            selected_item = treeview.selection()[0]
            selected_values = treeview.item(selected_item)['values']
            
            edit_screen = Toplevel(self.screen)
            edit_screen.title("Editar Produto")
            
            edit_screen.configure(bg="#FFFFFF")
            screen_width = 500
            screen_height = 200

            monitor_width = edit_screen.winfo_screenwidth()
            monitor_height = edit_screen.winfo_screenheight()

            pos_x = (monitor_width//2) - (screen_width//2)
            pos_y = (monitor_height//2) - (screen_height//2)

            edit_screen.geometry('{}x{}+{}+{}'.format(screen_width, screen_height, pos_x, pos_y))
            
            for i in range(5):
                edit_screen.grid_rowconfigure(i, weight=1)

            for i in range(2):
                edit_screen.grid_columnconfigure(i, weight=1)
            
            border_style = {"borderwidth":2, "relief":"groove"}
            
            Label(edit_screen, text="Nome do produto:", font="Calibri 16", bg="#FFFFFF").grid(row=0, column=0, padx=10, pady=10, stick="W")
            edit_product_name = Entry(edit_screen, font="Calibri 16", **border_style, bg="#FFFFFF", textvariable=StringVar(value=selected_values[1]))
            edit_product_name.grid(row=0, column=1, padx=10, pady=10, stick="W")
            
            Label(edit_screen, text="Descrição do produto:", font="Calibri 12", bg="#FFFFFF").grid(row=1, column=0, padx=10, pady=10, stick="W")
            edit_product_description = Entry(edit_screen, font="Calibri 16", **border_style, bg="#FFFFFF", textvariable=StringVar(value=selected_values[2]))
            edit_product_description.grid(row=1, column=1, padx=10, pady=10, stick="W")
            
            Label(edit_screen, text="Preço do produto:", font="Calibri 12", bg="#FFFFFF").grid(row=2, column=0, padx=10, pady=10, stick="W")
            edit_product_price = Entry(edit_screen, font="Calibri 16", **border_style, bg="#FFFFFF", textvariable=StringVar(value=selected_values[3]))
            edit_product_price.grid(row=2, column=1, padx=10, pady=10, stick="W")
            
            def save_edit_data():
                new_product_name = edit_product_name.get() 
                new_product_description = edit_product_description.get()
                new_product_price = edit_product_price.get()
                
                treeview.item(selected_item, values=(selected_values[0], new_product_name, new_product_description, new_product_price))
                
                self.cursor.execute("UPDATE Produtos SET NomeProduto = ?, Descricao = ?, Preco = ? WHERE ID = ?",
                                    (new_product_name, new_product_description, new_product_price, selected_values[0]))
                self.connection.commit()

                print("Dados alterados com sucesso")      
                
                edit_screen.destroy()
                
                list_data()
            
            def delete_data():
                if treeview.selection():
                    selected_item = treeview.selection()[0]
                    id = treeview.item(selected_item)['values'][0]

                    print(f"Deleting item with ID: {id}")

                    self.cursor.execute("DELETE FROM Produtos WHERE id = ?", (id,))
                    self.connection.commit()

                    list_data()

            edit_save_button = Button(edit_screen, text="Alterar", font="Calibri 16", bg="#008000", fg="#FFFFFF", command=save_edit_data)
            edit_save_button.grid(row=4, column=0, padx=20, pady=20)
            
            edit_delete_button = Button(edit_screen, text="Deletar", font="Calibri 16", bg="#FF0000", fg="#FFFFFF", command=delete_data)
            edit_delete_button.grid(row=4, column=1, padx=20, pady=20)

        def delete():
            selected_item = treeview.selection()[0]
            id = treeview.item(selected_item)['values'][0]
            
            self.cursor.execute("DELETE FROM Produtos WHERE id = ?", (id,))
            
            self.connection.commit()
            
            list_data()

        treeview.bind("<Double-1>", edit_data)    

        menu = Menu(self.screen)
        self.screen.configure(menu=menu)

        file_menu = Menu(menu, tearoff=0) 
        menu.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Cadastrar", command=cadastrar)
        file_menu.add_command(label="Sair", command=self.screen.destroy)

        def cleanData():
            for i in treeview.get_children():
                treeview.delete(i)

        def filter_data(product_name_field, product_description_field):
            if not product_name_field.get() and not product_description_field.get():
                list_data()
                return
            sql = "SELECT * FROM Produtos"
            
            params = []
            
            if product_name_field.get():
                sql += " WHERE NomeProduto LIKE ?"
                params.append('%' + product_name_field.get() + '%')
                
            if product_description_field.get():
                if product_name_field.get():
                    sql += " AND"
                else:
                    sql += " WHERE "
                sql += " Descricao LIKE ?"
                params.append('%' + product_description_field.get() + '%')
                
            self.cursor.execute(sql, tuple(params))
            products = self.cursor.fetchall()
                
            cleanData()
                
            for data in products:
                treeview.insert('', 'end', values=(data[0], data[1], data[2], data[3]))    
                
        product_name_field.bind('<KeyRelease>', lambda e: filter_data(product_name_field, product_description_field))
        product_description_field.bind('<KeyRelease>', lambda e: filter_data(product_name_field, product_description_field))

        delete_button = Button(self.screen, text="Deletar", command=delete, font="Calibri 26")
        delete_button.grid(row=4, column=4,  columnspan=4, stick="NSEW", padx=20, pady=20)

    def run(self):
        self.screen.mainloop()    
        
        self.screen.mainloop()
        self.cursor.close()
        self.connection.close()