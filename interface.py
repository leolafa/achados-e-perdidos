import tkinter as tk
from tkinter import ttk, messagebox
from banco_de_dados import session, Usuario, Objeto
from datetime import datetime


usuario_logado=None


class screen:
    def __init__(self,root):
        self.root= root
        self.root.title("Central de Achados e Perdidos - UFRPE")
        self.root.geometry("500x400")  
        self.root.configure(bg="lightblue")  
        self.criar_tela_login()  # Mostra a primeira tela (login)

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()    
    
    def get_user_by_email(self,email):
        return session.query(Usuario).filter_by(email=email).first()
    
    def login_user(self,email,senha):
        user= session.query(Usuario).filter_by(email=email).first()
        if not user:
            return None
        if user.senha==senha:
            return user
        else:
            return None

    def create_user(self, nome, email, senha):
        if "@ufrpe.br" not in email:
            raise ValueError("Email deve conter @ufrpe.br")
        if self.get_user_by_email(email):
            raise ValueError("Email já cadastrado")
        
        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        session.add(novo_usuario)
        session.commit()
        return self.get_user_by_email(email)  

    def adicionar_postagem(self, objeto, localidade, data, telefone, usuario_logado):
        if not all([objeto, localidade, data, telefone, usuario_logado]): #verifica se todos os dados foram preenchidos
            raise ValueError("Todos os campos devem ser preenchidos.")

        nova_postagem = Objeto(nome_objeto=objeto, localidade=localidade, data=data, telefone=telefone,user_id=usuario_logado.id
)
        # Salvar no banco
        session.add(nova_postagem)
        session.commit()

    def criar_tela_login(self):
        self.limpar_tela()

        tk.Label(self.root, text="Central de achados UFRPE", font=('Arial', 16), bg="lightblue").pack(pady=10)
        tk.Label(self.root, text="Nome:", bg="lightblue").pack() 
        self.nome_entry= tk.Entry(self.root, width=30)
        self.nome_entry.pack()

        
        
        tk.Label(self.root, text="Email:", bg="lightblue").pack() 
        self.email_entry= tk.Entry(self.root, width=30)
        self.email_entry.pack()

        tk.Label(self.root, text="Senha:", bg="lightblue").pack()
        self.senha_entry = tk.Entry(self.root, show="*", width=30)  
        self.senha_entry.pack()     


        tk.Button(self.root,text="Entrar", command=self.login).pack(pady=10)
        tk.Button(self.root,text="Criar conta", command=self.criar_usuario).pack()
        tk.Button(self.root, text="Atualizar Senha", command=self.atualizar_senha).pack(pady=5)
        tk.Button(self.root, text="Buscar Usuário", command=self.buscar_usuario).pack()
        tk.Button(self.root, text="Deletar Usuário", command=self.deletar_usuario).pack(pady=5)




    def login(self):
     global usuario_logado #global usuario_logado permite compartilhar o estado do usuário logado entre todas as telas do programa    
    
     email= self.email_entry.get()
     senha= self.senha_entry.get()

     if not email or not senha:
            messagebox.showerror("Erro", "Por favor, preencha email e senha")
            return
     try:
         usuario_logado= self.login_user(email,senha)
         if usuario_logado:
             self.criar_tela_principal()
         else:
            messagebox.showerror("Erro", "Email ou senha incorretos")
     except Exception as e:
          messagebox.showerror("Erro", f"Erro no login: {str(e)}")       


    def criar_usuario(self):
        global usuario_logado
        nome=self.nome_entry.get()
        email= self.email_entry.get()
        senha= self.senha_entry.get()
        
        if not all([nome, email, senha]):
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos")
            return
        try:
            usuario_logado = self.create_user(nome, email, senha)
            messagebox.showinfo("Sucesso", "Usuário criado com sucesso!")
            self.criar_tela_principal()
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
        except Exception as e:
            session.rollback()
            messagebox.showerror("Erro", f"Não foi possível criar usuário: {str(e)}")

    def atualizar_senha(self):
        email = self.email_entry.get()
        if not email:
            messagebox.showerror("Erro", "Por favor, digite o email")
            return
        usuario = session.query(Usuario).filter_by(email=email).first()
        if usuario:
            self.janela_atualizar_senha(usuario)
        else:
            messagebox.showerror("Erro", "Usuário não encontrado") 

    def janela_atualizar_senha(self, usuario):
        janela = tk.Toplevel(self.root)
        janela.title("Atualizar Senha")
        janela.geometry("300x200")
        janela.configure(bg="lightblue")
        
        tk.Label(janela, text="Nova Senha:", bg="lightblue").pack(pady=5)
        nova_senha_entry = tk.Entry(janela, show="*", width=30)
        nova_senha_entry.pack(pady=5)
        
        tk.Label(janela, text="Confirmar Senha:", bg="lightblue").pack(pady=5)
        confirma_senha_entry = tk.Entry(janela, show="*", width=30)
        confirma_senha_entry.pack(pady=5)
        
        def salvar_senha():
            nova_senha = nova_senha_entry.get()
            confirma_senha = confirma_senha_entry.get()
            
            if nova_senha != confirma_senha:
                messagebox.showerror("Erro", "Senhas não coincidem")
                return
            
            if not nova_senha:
                messagebox.showerror("Erro", "Por favor, digite uma senha")
                return
            
            try:
                usuario.senha = nova_senha
                session.commit()
                messagebox.showinfo("Sucesso", "Senha atualizada com sucesso!")
                janela.destroy()
            except Exception as e:
                session.rollback()
                messagebox.showerror("Erro", f"Erro ao atualizar senha: {str(e)}")
        
        tk.Button(janela, text="Salvar", command=salvar_senha).pack(pady=10)
        tk.Button(janela, text="Cancelar", command=janela.destroy).pack()
        


    def criar_tela_principal(self):
        self.limpar_tela()    
        tk.Label(self.root, text=f'Bem-vindo, {usuario_logado.nome}', font=("Arial",14), bg= "lightblue").pack(pady=10) 
        tk.Button(self.root, text="Cadastrar postagem", width=25, command= self.cadastrar_objeto).pack(pady=5) 
        tk.Button(self.root, text="Listar Postagens", width=25, command=self.listar_objetos).pack(pady=5)
        tk.Button(self.root, text="Pesquisar Objeto", width=25, command=self.pesquisar_objeto).pack(pady=5)
        tk.Button(self.root, text="Sair", width=25, command=self.criar_tela_login).pack(pady=10) 

    def cadastrar_objeto(self):
        self.limpar_tela()

        tk.Label(self.root, text="Cadastro de Objeto", font=("Arial", 14), bg="lightblue").pack(pady=10)
        campos = ["Nome do Objeto", "Localidade", "Data (dd/mm/aaaa)", "Telefone"]
        self.entries = {}
        for campo in campos:
            tk.Label(self.root, text=campo, bg="lightblue").pack()
            self.entries[campo] = tk.Entry(self.root, width=40)
            self.entries[campo].pack()

        tk.Button(self.root, text="Salvar", command=self.salvar_objeto).pack(pady=10)
        tk.Button(self.root, text="Voltar", command=self.criar_tela_principal).pack()

    def salvar_objeto(self):
        try:
            nome= self.entries["Nome do objeto"].get()
            localidade=self.entries["Localidade"].get()
            data=self.entries["Data (dd/mm/aaaa)"]
            telefone= self.entries["Telefone"]

            if not all([nome, localidade, data, telefone]):
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos")
                return

            self.adicionar_postagem(nome, localidade, data, telefone, usuario_logado)
            messagebox.showinfo("Sucesso", "Objeto cadastrado com sucesso!")
            self.criar_tela_principal()
        except Exception as erro:
            messagebox.showerror(f"ERRO ao cadastrar:{erro}")

    def listar_objetos(self):
        self.limpar_tela()
        tk.Label(self.root, text="Lista de Objetos", font=("Arial", 14), bg="lightblue").pack(pady=10)

        lista = tk.Text(self.root, height=15, width=60)
        lista.pack()


        for obj in session.query(blog.__class__.__bases__[0]).all():
            lista.insert(tk.END,f"{obj.nome_objeto} - {obj.localidade} - {obj.data} - {obj.telefone}")
        tk.Button(self.root, text="Voltar", command=self.criar_tela_principal).pack(pady=5)

    def pesquisar_objeto(self):
        self.limpar_tela()
        tk.Label(self.root, text="Pesquisar por Palavra-chave", font=("Arial", 14), bg="lightblue").pack(pady=10)

        tk.Label(self.root, text="Digite a palavra-chave:", bg="lightblue").pack()
        palavra_entry = tk.Entry(self.root, width=30)
        palavra_entry.pack()   

        resultado_box= tk.Text(self.root, height=15, width=60)
        resultado_box.pack(pady=10)

        def buscar():
            resultado_box.delete("1.0", tk.END)
            termo = palavra_entry.get()

            objetos = session.query(blog.__class__.__bases__[0]).filter(
            blog.__class__.__bases__[0].nome_objeto.like(f"%{termo}%")
            ).all()

            if objetos:
                for obj in objetos:
                    texto= f'{obj.nome_objeto} - {obj.localidade} - {obj.data} - {obj.telefone}'
                    resultado_box.insert(tk.END, texto)
            else:
                resultado_box.insert(tk.END, "Nenhum resultado encontrado")       
        tk.Button(self.root, text="Buscar", command=buscar).pack()
        tk.Button(self.root, text="Voltar", command=self.criar_tela_principal).pack(pady=5)
    

    def buscar_usuario(self):
        email= self.email_entry.get()
        if not email:
            messagebox.showerror("Erro", "Por favor, digite o email")
            return
        usuario= self.get_user_by_email(email)
        
        if usuario:
            messagebox.showinfo("Usuário encontrado", f"Nome: {usuario.nome} Email: {usuario.email}")
        else:
             messagebox.showinfo("Resultado", "Usuário não encontrado.")
    def deletar_usuario(self):
        email= self.email_entry.get()
        if not email:
            messagebox.showerror("Erro", "Por favor, digite o email")
            return
        usuario= self.get_user_by_email(email)

        
        if usuario:
            confirmar= messagebox.askyesno("Tem certeza que deseja deletar o usuario?")

            if confirmar:
                try:
                    session.delete(usuario)
                    session.commit()
                    messagebox.showinfo("Usuario deletado com sucesso")
                    self.criar_tela_login
                except Exception as e:
                    session.rollback()
                    messagebox.showerror("Erro", f"Não foi possível deletar usuário: {str(e)}")    
        else:
            messagebox.showinfo("Usuario nao encontrado")        


    



if __name__ == "__main__":
    root = tk.Tk()  
    app = screen(root)  
    root.mainloop()                  

            
            


                

              

