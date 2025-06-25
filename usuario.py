from banco_de_dados import Usuario, Session, session


def create_user():
    nome = input("Digite seu nome: ")
    email = input("Digite seu email(@ufrpe.br): ")
    senha = input("Digite sua senha: ")

    verify_user= get_user_by_email(session, email)
#verifica se o dominio da rural ta no email
    if "@ufrpe.br" not in email:
        print("email invalido"  )
        return
#verifica se o email ja esta cadastrado no banco
    if verify_user: 
        print("Email já cadastrado, tente a opção de login")
#salva no banco
    else:
        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        # Salvar no banco
        session.add(novo_usuario)
        session.commit()
        # print("Usuário salvo com sucesso!")
        usuario_logado = get_user_by_email(session, email)
        return usuario_logado


#Buscar o usuario pelo email
def get_user_by_email(session, email: str):
    #Retorna o usuário caso ele já esteja cadastrado ou None
    usuario = session.query(Usuario).filter_by(email=email).first()
    return usuario


#Login

def login_user(email, senha):
    session = Session()
    #verifica os dados do usuario
    user = session.query(Usuario).filter_by(email=email).first()
#caso nao seja encontrado o usuario no banco
    if not user:
        print("Usuário não encontrado")
        return None
    if user.senha == senha:
        print(f'Bem vindo, {user.nome}')
        return user
    else:
        print("Senha incorreta")
        return None


#Buscar usuário pelo email, para verificar se um usuario ja se encontra cadastrado
def buscar_usuario():
    email_busca = input("Digite o email do usuário que deseja buscar: ")
    usuario = session.query(Usuario).filter_by(email=email_busca).first()

    if usuario:
        print(f"Usuário encontrado: {usuario.nome} (E-mail: {usuario.email})")
    else:
        print("Usuário não encontrado.")


#UPDATE, atualizar a senha do usuario
def atualizar_usuario(usuario):
    nova_senha= input("Digite a nova senha:")
    confirma_nova_senha = input("Digite novamente a nova senha:")
    if nova_senha == confirma_nova_senha:
        try:
            usuario.senha = nova_senha 
            session.add(usuario)
            session.commit()
            print(f"Usuário '{usuario.nome}' atualizado com sucesso.")
        # Trata possíveis erros na atualização
        except Exception as e:
            session.rollback()
            print(f"Erro ao atualizar usuário: {e}")
        finally:
            session.close()
    else:
        print("Erro ao atualizar senha. Tente novamente")


#DELETAR, apagar o usuario do database
def deletar_usuario(nome_usuario):
    session = Session()
    try:
        usuario = session.query(Usuario).filter_by(email=nome_usuario).first()
        if usuario:
            session.delete(usuario)
            session.commit()
            print(f"Usuário '{nome_usuario}' deletado com sucesso.")
        # Trata possíveis erros na remoção
        else:
            print(f"Usuário '{nome_usuario}' não encontrado.")
    except Exception as e:
        session.rollback()
        print(f"Erro ao deletar usuário: {e}")

