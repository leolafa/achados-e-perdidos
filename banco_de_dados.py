#Importações necessarias
#Usando sqlalchemy como banco de dados
from sqlalchemy import create_engine, Column, Integer, Boolean, String, ForeignKey, text
from sqlalchemy.orm import sessionmaker, declarative_base,relationship
from sqlalchemy import select


#configuraçoes do banco de dados
db = create_engine("sqlite:///meubanco.db")

Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

# Tabela para agrupar os usuarios
class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    email = Column(String, unique=True)
    senha = Column(String)
    
    objetos = relationship("Objeto", back_populates="usuario")

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha
      
#Tabelas para agrupar os objetos
class Objeto(Base):
    __tablename__ = 'objetos'
    id = Column(Integer, primary_key=True,  autoincrement=True)
    nome_objeto = Column(String)
    data = Column(String)
    localidade=Column(String)
    telefone= Column(String)
    user_id = Column(Integer, ForeignKey('usuarios.id'))  # Chave estrangeira para o ID do usuário
    usuario = relationship("Usuario", back_populates="objetos")  # Relacionamento com a tabela Usuario
    status= Column(Boolean, default=False)
    categoria= Column(String)
    def __init__(self, nome_objeto, localidade, data, telefone, user_id, status, categoria):
        self.nome_objeto = nome_objeto
        self.localidade = localidade
        self.data = data
        self.telefone= telefone
        self.user_id = user_id
        self.status=status
        self.categoria=categoria


Base.metadata.create_all(db)