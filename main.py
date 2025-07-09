from banco_de_dados import session, Usuario, Objeto
from usuario import UsuarioService
from objeto import Item

import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.align import Align
from rich import box
from rich.progress import track
import os


#inicia o rich
console = Console()   #Instância do Rich Console para saída formatada

usuario_service = UsuarioService()
#Função para limpar a tela
def clear_screen():
    
    os.system('cls' if os.name == 'nt' else 'clear')

# Mostra um cabeçalho estilizado no topo da tela
#sempre que chamado monta um cabeçalho
def show_header(title):
   # Coloca tudo numa caixa com borda dupla azul
    header = Panel(
        Align.center(Text(title, style="bold blue")),  # Texto centralizado e azul
        style="blue",                                  # Borda azul
        box=box.DOUBLE                                # Borda dupla (mais chamativa)
    )
    console.print(header)
    console.print()  # Linha em branco após o cabeçalho



def user_menu(usuario_logado):
    blog = Item()
    while True:
        clear_screen()
        welcome_text = (f"Bem-vindo, {usuario_logado.nome}!")
        show_header("🔍 Central de achados UFRPE 🔍  ")
        #boas vindas
        welcome_panel = Panel(
            Align.center(Text(welcome_text, style="bold cyan")),  # Texto ciano centralizado
            style="cyan",                                         # Borda ciano
            title="Usuário Logado",                           # Título do painel
            box=box.ROUNDED                                      # Bordas arredondadas
        )
        console.print(welcome_panel)
        console.print()

        menu_table = Table(show_header=False, box=box.SIMPLE)  # Tabela sem cabeçalho
        menu_table.add_column("Opção", style="bold magenta", width=8)    # Coluna números
        menu_table.add_column("Descrição", style="white")               # Coluna descrições
        
        # Adicionando as opções do menu
        menu_table.add_row("1", "📩 Cadastrar nova postagem")
        menu_table.add_row("2", "📋 Listar todas as postagens")
        menu_table.add_row("3", "🛑 Sair do sistema")
        menu_table.add_row("4", "🔍 Pesquisar por palavra-chave")
        menu_table.add_row("5", "⚙️  Gerenciar minhas postagens")
        
        # Colocando a tabela dentro de um painel
        menu_panel = Panel(
            menu_table,
            title="💻 Menu Principal",
            style="blue",
            box=box.ROUNDED
        )
        console.print(menu_panel)

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            clear_screen()
            show_header("📝 CADASTRAR NOVA POSTAGEM")
            
            # Coletando dados do usuário
            titulo = Prompt.ask("📦 Digite o nome e descrição do objeto")
            conteudo = Prompt.ask("📍 Digite onde foi encontrado")
            data = Prompt.ask("📅 Digite a data que foi achado (dd/mm/aaaa)")
            telefone = Prompt.ask("📞 Digite o número para contato")
            
            Categoria= ["roupas", "tecnologicos", "documentos", "pessoais", "bolsas"]
            while True:
                Categoria= ["roupas", "tecnologicos", "documentos", "pessoais", "bolsas"]
                categoria= Prompt.ask(f"📁 Digite a categoria do objeto:")
                if categoria in Categoria:
                    break
                else:
                    console.print(f"A categoria digitada nao se enquadra nas categorias permitidas({Categoria})")
                       
            # Status com opções limitadas e valor padrão
            status_input = Prompt.ask(
                "Status do objeto", 
                choices=["a", "p"],  # a=achado, p=perdido
                default="p"         # padrão é perdido
            )
            
            objeto_status = True if status_input == 'a' else False  # Converte para boolean
            
            # SIMULAÇÃO DE PROCESSAMENTO
            # ================================================================
            with console.status("[bold green]Cadastrando postagem...") as status_bar: 
                time.sleep(1)  # Simula tempo de processamento
                try:
                    # Tenta cadastrar a postagem
                    blog.adicionar_postagem(titulo, conteudo, data, telefone, usuario_logado, objeto_status, categoria)
                    print("✔ Postagem cadastrada com sucesso!")
                except ValueError as e:
                    # Se der erro de validação, mostra mensagem
                    print(f" Erro ao cadastrar: {e}")
            
            Prompt.ask("Pressione Enter para continuar")  # Pausa para usuário ler
          

        elif opcao == '2':
            
           clear_screen()
           show_header("📋 LISTA DE POSTAGENS")
           blog.listar_postagens()  # Chama método que lista objetos
           Prompt.ask("Pressione Enter para continuar")

        elif opcao == '3':
            print("👋 Saindo do sistema...")
            time.sleep(1)
            break

        elif opcao=='4':
            
            clear_screen()
            show_header("🔍 PESQUISAR OBJETOS")
            palavra = Prompt.ask("🔎 Digite o objeto que deseja encontrar")
            blog.pesquisa_palavra_chave(palavra)  # Chama método de pesquisa
            Prompt.ask("Pressione Enter para continuar")
        elif opcao== '5':
            clear_screen()
            show_header("⚙️ GERENCIAR MINHAS POSTAGENS")
            blog.minhas_postagens(usuario_logado)  # Mostra postagens do usuário
            Prompt.ask("Pressione Enter para continuar")
            continue
            

        else:
            print("Opção inválida. Tente novamente.")




#MENU incial
def first_menu():
    parar = False
    while not parar:
        clear_screen()
        main_table = Table(show_header=False, box=box.SIMPLE)
        main_table.add_column("Opção", style="bold magenta", width=8)
        main_table.add_column("Descrição", style="white")
        
        # Opções do menu inicial
        main_table.add_row("1", "👤 Criar usuário")
        main_table.add_row("2", "🔍 Buscar usuário")
        main_table.add_row("3", "🗑️  Deletar usuário")
        main_table.add_row("4", "🔐 Login")
        main_table.add_row("5", "🛑 Sair")
        main_table.add_row("6", "🔑 Atualizar senha")
        
        # Painel contendo a tabela
        main_panel = Panel(
            main_table,
            title="🔍 Central de achados UFRPE 🔍  ",
            style="green",
            box=box.ROUNDED
        )
        console.print(main_panel)

        opcao = input("Digite sua opção: ")
        time.sleep(1)

        if opcao == '1':
            clear_screen()
            show_header("👤 CRIAR USUÁRIO")
            usuario_logado = usuario_service.create_user()  # Chama serviço de criação
            if usuario_logado:  # Se usuário foi criado com sucesso
                console.print("Usuário criado com sucesso! Redirecionando...")
                time.sleep(1)
                user_menu(usuario_logado)  # Vai direto para menu do usuár


        elif opcao == '2':
            clear_screen()
            show_header("🔍 BUSCAR USUÁRIO")
            usuario_service.buscar_usuario()
            Prompt.ask("Pressione Enter para continuar")
        
        elif opcao == '3':
            clear_screen()
            show_header("🗑️ DELETAR USUÁRIO")
            nome = Prompt.ask("📧 Digite o email do usuário a ser deletado")
            # Confirmação adicional para ação destrutiva
            #cria pergunta sim/não
            if Confirm.ask(f"⚠️ Tem certeza que deseja deletar o usuário {nome}?"):
                usuario_service.deletar_usuario(nome)
            Prompt.ask("Pressione Enter para continuar")
        
        elif opcao == '4':
            clear_screen()
            show_header("🔐 LOGIN")
            user = Prompt.ask("📧 Digite seu email")
            senha = Prompt.ask("🔑 Digite sua senha")  
            
            # Simulação de verificação com status
            with console.status("[bold green]Verificando credenciais...") as status:
                time.sleep(1)
                usuario_logado = usuario_service.login_user(user, senha)
                
            if usuario_logado:  # Login bem-sucedido
                console.print("Login realizado com sucesso!")
                time.sleep(1)
                user_menu(usuario_logado)  # Vai para menu do usuário
            else:  # Login falhou
                console.print("Login falhou. Verifique suas credenciais.")
                Prompt.ask("Pressione Enter para continuar")
        elif opcao == '5':
            console.print("👋 Obrigado por usar o sistema!", style="bold green")
            parar = True  # Sai do loop principal

        elif opcao=="6":
            clear_screen()
            show_header("🔑 ATUALIZAR SENHA")
            email_cadastrado = Prompt.ask("📧 Digite seu email cadastrado")
            # Busca usuário no banco de dados
            usuario = session.query(Usuario).filter_by(email=email_cadastrado).first()
            if usuario:
                usuario_service.atualizar_usuario(usuario)
            else:
                console.print("Usuário não encontrado")
            return
        else:
            console.print("Opção inválida. Tente novamente.")






if __name__ == "__main__":
    first_menu()

