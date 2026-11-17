import mysql.connector
import sys
from datetime import datetime

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

def cadastrar_agendamento():

    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)
    
    print("\n--- NOVO AGENDAMENTO ---")
    

    cursor.execute("SELECT id_animal, nome FROM animal")
    animais = cursor.fetchall()
    
    if not animais:
        print("Nenhum animal encontrado. Cadastre um primeiro.")
        cursor.close()
        conexao.close()
        return
        
    print("Animais Disponíveis:")
    for an in animais:
        print(f"ID: {an['id_animal']} | Nome: {an['nome']}")
        
    try:
        id_animal = int(input("\nDigite o ID do Animal: "))
    except ValueError:
        print("ID inválido. Digite apenas números.")
        cursor.close()
        conexao.close()
        return

    entrada = input("Data e Hora (DD-MM-AAAA HH:MM): ").strip()
    try:
        data_agendamento = datetime.strptime(entrada, "%d-%m-%Y %H:%M")
    except ValueError:
        print("Data inválida. Use o formato DD-MM-AAAA HH:MM.")
        cursor.close()
        conexao.close()
        return

    motivo_servico = input("Serviço (Ex: Banho, Tosa): ").strip()
    
    query = """
        INSERT INTO agendamento (data_agendamento, motivo_servico, id_animal) 
        VALUES (%s, %s, %s)
    """
    
    try:
        cursor.execute(query, (data_agendamento, motivo_servico, id_animal))
        conexao.commit()
        print("\nAgendamento cadastrado com sucesso.")
    except mysql.connector.Error as err:
        print(f"\nNão foi possível agendar: {err}")
    finally:
        cursor.close()
        conexao.close()

def listar_agendamentos():

    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)
    
    print("\n--- LISTA DE AGENDAMENTOS ---")
    

    query = """
        SELECT 
            a.id_agendamento, 
            a.data_agendamento, 
            a.motivo_servico,
            an.nome AS animal_nome,
            c.nome AS cliente_nome,
            c.telefone AS cliente_telefone
        FROM agendamento a
        INNER JOIN animal an ON a.id_animal = an.id_animal
        INNER JOIN cliente c ON an.id_cliente = c.id_cliente
        ORDER BY YEAR(a.data_agendamento) ASC
    """
    
    cursor.execute(query)
    agendamentos = cursor.fetchall()
    
    if not agendamentos:
        print("Nenhum agendamento encontrado.")
    else:
        for a in agendamentos:
            data_formatada = a['data_agendamento'].strftime('%d-%m-%Y %H:%M')
            print(f"ID: {a['id_agendamento']} | Data: {data_formatada} | Serviço: {a['motivo_servico']}")
            print(f"    -> Animal: {a['animal_nome']}")
            print(f"    -> Cliente (Dono): {a['cliente_nome']} | Tel: {a['cliente_telefone']}")
            print("-" * 50)
            
    cursor.close()
    conexao.close()

def atualizar_data_agendamento():

    print("\n--- REAGENDAR ---")
    listar_agendamentos()
    
    try:
        id_agendamento = int(input("\nDigite o ID do agendamento que deseja alterar: "))
    except ValueError:
        print("ID inválido. Digite apenas números.")
        return
        
    entrada = input("Nova Data (DD-MM-AAAA) ou Data e Hora (DD-MM-AAAA HH:MM): ").strip()
    
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    try:
        nova_data = datetime.strptime(entrada, "%d-%m-%Y %H:%M")
    except ValueError:
        try:
        
            somente_data = datetime.strptime(entrada, "%d-%m-%Y")
        except ValueError:
            print("Data inválida. Use DD-MM-AAAA ou DD-MM-AAAA HH:MM.")
            cursor.close()
            conexao.close()
            return
        cursor.execute("SELECT data_agendamento FROM agendamento WHERE id_agendamento = %s", (id_agendamento,))
        atual = cursor.fetchone()
        if not atual:
            print("\nNenhum agendamento encontrado com esse ID.")
            cursor.close()
            conexao.close()
            return
        nova_data = somente_data.replace(hour=atual[0].hour, minute=atual[0].minute)
    
    query = "UPDATE agendamento SET data_agendamento = %s WHERE id_agendamento = %s"
    
    try:
        cursor.execute(query, (nova_data, id_agendamento))
        conexao.commit()
        if cursor.rowcount > 0:
            print("\nData do agendamento atualizada.")
        else:
            print("\nNenhum agendamento encontrado com esse ID.")
    except mysql.connector.Error as err:
        print(f"\nNão foi possível atualizar a data: {err}")
    finally:
        cursor.close()
        conexao.close()

def excluir_agendamento():
    
    print("\n--- EXCLUIR AGENDAMENTO ---")
    listar_agendamentos()

    try:
        id_agendamento = int(input("\nDigite o ID do agendamento que deseja excluir: "))
    except ValueError:
        print("ID inválido. Digite apenas números.")
        return

    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT id_agendamento, data_agendamento, motivo_servico FROM agendamento WHERE id_agendamento = %s",
            (id_agendamento,)
        )
        agendamento = cursor.fetchone()

        if not agendamento:
            print("\nNenhum agendamento encontrado com esse ID.")
            return

        data_formatada = agendamento['data_agendamento'].strftime('%d-%m-%Y %H:%M')
        confirmacao = input(
            f"Confirma a exclusão do agendamento de {data_formatada} ({agendamento['motivo_servico']})? (S/N): "
        ).strip().upper()
        if confirmacao != 'S':
            print("\nExclusão cancelada.")
            return

        cursor.execute("DELETE FROM agendamento WHERE id_agendamento = %s", (id_agendamento,))
        conexao.commit()
        print("\nAgendamento excluído.")
    except mysql.connector.Error as err:
        conexao.rollback()
        print(f"\nNão foi possível excluir o agendamento: {err}")
    finally:
        cursor.close()
        conexao.close()

def iniciar_modulo():
    """Menu principal do módulo de agendamentos."""
    while True:
        print("\n" + "="*45)
        print("   MÓDULO DE AGENDAMENTOS")
        print("="*45)
        print("1. Cadastrar Novo Agendamento")
        print("2. Listar Todos os Agendamentos")
        print("3. Atualizar Data do Agendamento")
        print("4. Excluir Agendamento")
        print("5. Voltar ao Painel Principal")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == '1':
            cadastrar_agendamento()
        elif opcao == '2':
            listar_agendamentos()
        elif opcao == '3':
            atualizar_data_agendamento()
        elif opcao == '4':
            excluir_agendamento()
        elif opcao == '5':
            print("\nVoltando...")
            break
        else:
            print("\nOpção inválida. Tente novamente.")

if __name__ == "__main__":
    iniciar_modulo()
