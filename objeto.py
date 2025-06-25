import banco_de_dados
from banco_de_dados import Objeto, Session, session
from datetime import datetime
from sqlalchemy.orm import joinedload

class Postagem:
    def __init__(self,objeto:str, localidade:str,data:str, telefone:int ):
        self.objeto= objeto
        self.localidade = localidade
        self.validar_data(data)
        self.data= data
        self.telefone= telefone

   ###Valida o formato da data###
    def validar_data(self, data: str) -> None:

        try:
            datetime.strptime(data, '%d/%m/%Y')
        except ValueError:
            raise ValueError("Data deve estar no formato dd/mm/aaaa")

    def __repr__(self):
        return f"Postagem(Objeto='{self.objeto}', localidade='{self.localidade}', data='{self.data}, telefone para contato='{self.telefone})"
#Gerenciar as postagens
class Blog:
    def __init__(self):
        self.postagens = [] #Armazena os objetos
#Adicionar postagens
    def adicionar_postagem(self, objeto, localidade, data, telefone, usuario_logado):
        if not all([objeto, localidade, data, telefone, usuario_logado]): #verifica se todos os dados foram preenchidos
            raise ValueError("Todos os campos devem ser preenchidos.")

        nova_postagem = Objeto(nome_objeto=objeto, localidade=localidade, data=data, telefone=telefone,user_id=usuario_logado.id
)
        # Salvar no banco
        session.add(nova_postagem)
        session.commit()



#Lista de postagens cadastradas
    def listar_postagens(self):
        # Consulta todos os objetos e carrega o relacionamento 'usuario' para evitar multiplas consultas no banco
        objetos = session.query(Objeto).options(joinedload(Objeto.usuario)).all()

        if not objetos:
            print("Objeto não cadastrado")
        else:
            print("--- LISTA DE POSTAGENS ---")
            # Liste os objetos
            for obj in objetos:
                # Acessa o nome do usuário através do relacionamento 'usuario'
                nome_usuario = obj.usuario.nome if obj.usuario else "Usuário Desconhecido"
                print(f"Objeto: {obj.nome_objeto}, Localidade: {obj.localidade}, Data: {obj.data}, Telefone: {obj.telefone}")
    

    def pesquisa_palavra_chave(self,palavra_chave):
        resultados = session.query(Objeto).filter(Objeto.nome_objeto.like(f"%{palavra_chave}%")).all()
        if not resultados:
            print("Nenhuma postagem encontrada")
        else:
            print(f'------RESULTADOS DA PESQUISA POR {palavra_chave}------')
            for obj in resultados:
                nome_usuario= obj.usuario.nome if obj.usuario else "Usuario desconhecido"
                print(f"OBJETO:{obj.nome_objeto}, LOCALIDADE:{obj.localidade}, DATA:{obj.data}, TELEFONE:{obj.telefone}, USUARIO:{nome_usuario}")


def main():
    session = Session()
