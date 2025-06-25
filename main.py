from banco_de_dados import session, Usuario, Objeto
from usuario import create_user, deletar_usuario, login_user, buscar_usuario, atualizar_usuario
from objeto import Blog
import time
import interface

def user_menu(usuario_logado):
    blog = Blog()
    while True:
        print("Bem-vindo ao sistema de achados e perdidos")
        print("1. Cadastrar nova postagem")
        print("2. Listar postagens")
        print("3. Sair")
        print("4. Pesquisar por palavra chave")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            titulo = input("Digite o nome e a descrição do objeto: ")
            conteudo = input("Digite onde foi encontrado: ")
            data = input("Digite a data que foi achado: ")
            telefone= input("Digite o número para contato: ")
            try:
                blog.adicionar_postagem(titulo, conteudo, data,telefone, usuario_logado)
                print("Postagem cadastrada com sucesso")
            except ValueError as e:
                print(f"Erro ao cadastrar: {e}")


        elif opcao == '2':
            blog.listar_postagens()

        elif opcao == '3':
            print("Saindo do sistema...")
            break

        elif opcao=='4':
            palavra= input("Digite o objeto que deseja encontrar:")
            blog.pesquisa_palavra_chave(palavra)
        else:
            print("Opção inválida. Tente novamente.")




#MENU incial
def first_menu():
    parar = False
    while not parar:
        print("******************************INICIO*********************************")
        print("Escolha uma opção:")
        print("1 - Criar usuário")
        print("2 - Buscar usuário")
        print("3 - Deletar usuário")
        print("4- Login")
        print("5- Sair")
        print("6-Atulizar senha")

        opcao = input("Digite sua opção: ")
        time.sleep(1)

        if opcao == '1':
            usuario_logado = create_user()  # Captura o usuário criado
            if usuario_logado:
                user_menu(usuario_logado)  # Passa o usuário logado para o menu


        elif opcao == '2':
            buscar_usuario()
        elif opcao == '3':
            nome= input("Digite o email de usuário a ser deletado:")
            deletar_usuario(nome)
        elif opcao == '4':
            user= input("Digite seu email:")
            time.sleep(1)
            senha= input("Digite sua senha:")
            usuario_logado = login_user(user, senha)  # Captura o objeto do usuário logado
            if usuario_logado:
                user_menu(usuario_logado)  # Passa o objeto do usuário logado para user_menu
            else:
                print("Login falhou. Tente novamente.")
        elif opcao == '5':
            parar = True
        elif opcao=="6":
            email_cadastrado= input("Digite seu email cadastrado: ")
            usuario = session.query(Usuario).filter_by(email=email_cadastrado).first()
            if usuario:
                atualizar_usuario(usuario)
            else:
                print("Usuário não encontrado")
        else:
            print("Opção inválida. Tente novamente.")






if __name__ == "__main__":
    first_menu()

