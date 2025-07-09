import banco_de_dados
from banco_de_dados import Objeto, Session, session, Usuario
from datetime import datetime
from sqlalchemy.orm import joinedload

#responsável por gerenciar todas as operações relacionadas aos objetos
class Item:
     #Construtor que inicializa uma lista vazia de postagens
    def __init__(self):
       self.postagens = [] 

  

   ###Valida o formato da data###
    def validar_data(self, data: str) -> None:

        try:
            # Tenta converter string para objeto datetime
            # Se falhar, significa que formato está incorreto
            datetime.strptime(data, '%d/%m/%Y')
        except ValueError:
            raise ValueError("Data deve estar no formato dd/mm/aaaa")

    

#Adicionar postagens
    def adicionar_postagem(self, nome_objeto, localidade, data, telefone, usuario_logado, status, categoria):
        if not all([nome_objeto, localidade, data, telefone, usuario_logado, categoria]): #verifica se todos os dados foram preenchidos
            raise ValueError("Todos os campos devem ser preenchidos.")
        self.validar_data(data)
        nova_postagem = Objeto(nome_objeto=nome_objeto, data=data,localidade=localidade, telefone=telefone,user_id=usuario_logado.id, status=status, categoria=categoria)
        
        # Salvar no banco
        session.add(nova_postagem)
        session.commit()



#Lista de postagens cadastradas
    def listar_postagens(self):
        # Consulta todos os objetos e carrega o relacionamento 'usuario' para evitar multiplas consultas no banco
        objetos = session.query(Objeto).all()

        if not objetos:
            print("Objeto não cadastrado")
        else:
            print("--- LISTA DE POSTAGENS ---")
            # Liste os objetos
            for obj in objetos:
                # Acessa o nome do usuário através do relacionamento 'usuario'
                nome_usuario = obj.usuario.nome if obj.usuario else "Usuário Desconhecido"
                print(f"Objeto: {obj.nome_objeto}, Localidade: {obj.localidade}, Data: {obj.data}, Telefone: {obj.telefone}, Categoria: {obj.categoria}")
                
    #Exibe e permite gerenciar as postagens do usuário logado
    def minhas_postagens(self, user):
        objetos = session.query(Objeto).filter(Objeto.user_id == user.id).all()
        for obj in objetos:
           nome_usuario = obj.usuario.nome if obj.usuario else "Usuário Desconhecido"
           #print(f"Objeto: {obj.nome_objeto}, Localidade: {obj.localidade}, Data: {obj.data}, Telefone: {obj.telefone}, Categoria: {obj.categoria}")
        
        for i, obj in enumerate(objetos, 1):
            nome_usuario = obj.usuario.nome if obj.usuario else "Usuário Desconhecido"
            # Converte status boolean para texto legível
            status_texto = "ACHADO" if obj.status else "PERDIDO"
            print(f"{i}. [ID: {obj.id}] Objeto: {obj.nome_objeto}")
            print(f"   Localidade: {obj.localidade}, Data: {obj.data}, Telefone: {obj.telefone}, Categoria: {obj.categoria}")
            print(f"   Status: {status_texto}")
            print("-" * 40)
        
        if not objetos:
            print(f"{user.nome}, você ainda não tem objetos cadastrados.")
            return
        escolha=input("Digite o ID do objeto que deseja alterar o status:")
        self.atualizar_status_objeto(escolha)
        
        if not escolha:
            return
    
           
        
     
    def atualizar_status_objeto(self, objeto_id):
        try:
            objeto = session.query(Objeto).filter(Objeto.id == objeto_id).one_or_none()
            objeto = session.get(Objeto, objeto_id)
            objeto.status= True
            session.commit()
            
            print(f"Status do objeto '{objeto.nome_objeto}' alterado para ACHADO!")
           
            return objeto
        
        except Exception as e:
            print(f"Objeto não encontrado")
           


    
    def pesquisa_palavra_chave(self,palavra_chave):
        try:
           # BUSCA COM FILTRO LIKE
           resultados = session.query(Objeto).filter(Objeto.nome_objeto.like(f"%{palavra_chave}%")).all()
           if not resultados:
               print("Nenhuma postagem encontrada")
               return [] 
           else:
                print(f'------RESULTADOS DA PESQUISA POR {palavra_chave}------')
                for obj in resultados:
                    nome_usuario= obj.usuario.nome if obj.usuario else "Usuario desconhecido"
                    #print(f"OBJETO:{obj.nome_objeto}, LOCALIDADE:{obj.localidade}, DATA:{obj.data}, TELEFONE:{obj.telefone}, USUARIO:{nome_usuario}")
                    print(f"OBJETO: {obj.nome_objeto}")
                    print(f"LOCALIDADE: {obj.localidade}")
                    print(f"DATA: {obj.data}")
                    print(f"TELEFONE: {obj.telefone}")
                    print(f"USUARIO: {nome_usuario}")
                    print(f"CATEGORIA: {obj.categoria}")
                    print("-" * 40)
                return resultados
        except Exception as e:
            print(f"Erro ao realizar pesquisa: {e}")
            return []   
    

    






def main():
    session = Session()
