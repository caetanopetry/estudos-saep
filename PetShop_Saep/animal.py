import mysql.connector
from datetime import datetime
import sys

def conectar_banco():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="saep_db"
        )
    except mysql.connector.Error as err:
        print(f"Não foi possível conectar ao banco de dados: {err}")
        sys.exit(1)

def listar_clientes_disponiveis(cursor):

    cursor.execute("SELECT id_cliente, nome FROM cliente")
    clientes = cursor.fetchall()
    
    if not clientes:
        print("Nenhum cliente encontrado. Cadastre um cliente primeiro.")
        return False
        
    print("\n--- CLIENTES DISPONÍVEIS ---")
    for c in clientes:
        print(f"ID: {c['id_cliente']} | Nome: {c['nome']}")
    print("-" * 38)
    return True

def cadastrar_animal():

    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)
    
    print("\n--- CADASTRAR NOVO ANIMAL ---")
    

    if not listar_clientes_disponiveis(cursor):
        cursor.close()
        conexao.close()
        return

    try:
        id_cliente = int(input("\nDigite o ID do cliente dono do animal: "))
    except ValueError:
        print("ID inválido. Digite apenas números.")
        cursor.close()
        conexao.close()
        return

    nome = input("Nome do Animal: ").strip()
    responsavel = input("Responsável (ex: Dono, Cuidador): ").strip()
    observacao = input("Observação (ex: Pelo longo, tem medo de secador): ").strip()
    entrada = input("Data de Nascimento (DD-MM-AAAA): ").strip()
    try:
        data_nascimento = datetime.strptime(entrada, "%d-%m-%Y").date()
    except ValueError:
        print("Data inválida. Use o formato DD-MM-AAAA.")
        cursor.close()
        conexao.close()
        return
    
    query = """
        INSERT INTO animal (nome, responsavel, observacao, data_nascimento, id_cliente) 
        VALUES (%s, %s, %s, %s, %s)
    """
    valores = (nome, responsavel, observacao, data_nascimento, id_cliente)
    
    try:
        cursor.execute(query, valores)
        conexao.commit()
        print("\nAnimal cadastrado e vinculado ao cliente com sucesso.")
    except mysql.connector.Error as err:
        print(f"\nNão foi possível cadastrar. Verifique se o ID do cliente existe. Detalhes: {err}")
    finally:
        cursor.close()
        conexao.close()

def listar_animais():

    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)
    
    print("\n--- LISTA DE ANIMAIS ---")
    
    query = """
        SELECT an.id_animal, an.nome AS animal, an.responsavel, 
               an.data_nascimento, c.nome AS dono 
        FROM animal an
        INNER JOIN cliente c ON an.id_cliente = c.id_cliente
    """
    cursor.execute(query)
    animais = cursor.fetchall()
    
    if not animais:
        print("Nenhum animal encontrado.")
    else:
        for an in animais:
            nascimento = an['data_nascimento'].strftime('%d-%m-%Y') if an['data_nascimento'] else '-'
            print(f"ID: {an['id_animal']} | Nome: {an['animal']} | Responsável: {an['responsavel']} | Nascimento: {nascimento} | Dono: {an['dono']}")
            
    cursor.close()
    conexao.close()

def excluir_animal():
    print("\n--- EXCLUIR ANIMAL ---")
    listar_animais()

    try:
        id_animal = int(input("\nDigite o ID do animal a ser excluído: "))
    except ValueError:
        print("ID inválido. Digite apenas números.")
        return

    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute("SELECT id_animal, nome FROM animal WHERE id_animal = %s", (id_animal,))
        animal = cursor.fetchone()

        if not animal:
            print("\nAnimal não encontrado.")
            return

        confirmacao = input(f"Confirma a exclusão de '{animal['nome']}'? (S/N): ").strip().upper()
        if confirmacao != 'S':
            print("\nExclusão cancelada.")
            return

        cursor.execute("DELETE FROM animal WHERE id_animal = %s", (id_animal,))
        conexao.commit()
        print("\nAnimal excluído.")
    except mysql.connector.Error as err:
        conexao.rollback()
        print(f"\nNão foi possível excluir. O animal está vinculado a um agendamento.")
    finally:
        cursor.close()
        conexao.close()

def iniciar_modulo():

    while True:
        print("\n" + "="*45)
        print("   MÓDULO DE ANIMAIS ")
        print("="*45)
        print("1. Cadastrar Animal")
        print("2. Listar Animais")
        print("3. Excluir Animal")
        print("4. Voltar ao Painel Principal")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == '1':
            cadastrar_animal()
        elif opcao == '2':
            listar_animais()
        elif opcao == '3':
            excluir_animal()
        elif opcao == '4':
            print("\nVoltando...")
            break
        else:
            print("\nOpção inválida. Tente novamente.")

if __name__ == "__main__":
    iniciar_modulo()
