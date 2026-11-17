import mysql.connector
import base64
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

def criptografar_dado(dado):

    return base64.b64encode(dado.encode('utf-8')).decode('utf-8')

def descriptografar_dado(dado_criptografado):

    try:
        return base64.b64decode(dado_criptografado).decode('utf-8')
    except Exception:
        return dado_criptografado

def solicitar_cpf(prompt):
    while True:
        cpf = input(prompt)
        if not cpf.isascii() or not cpf.isdigit():
            print("Ops, digite o CPF usando apenas números, por favor.")
        elif len(cpf) != 11:
            print("Ops, esse CPF não parece válido. Digite exatamente os 11 números, beleza?")
        else:
            return cpf

def solicitar_telefone(prompt):
    while True:
        telefone = input(prompt)
        if not telefone.isascii() or not telefone.isdigit() or len(telefone) not in (10, 11):
            print("Ops, esse telefone ficou fora do formato esperado. Digite somente 10 ou 11 números, incluindo o DDD, beleza?")
        else:
            return telefone

def solicitar_email(prompt):
    while True:
        email = input(prompt).strip()
        if '@' not in email or '.' not in email.split('@', 1)[1]:
            print("Ops, esse e-mail não parece válido. Confira se ele tem um '@' e um ponto depois dele, por favor.")
        else:
            return email

def cpf_ja_cadastrado(cursor, cpf_criptografado, id_cliente=None):
    query = "SELECT id_cliente FROM cliente WHERE cpf = %s"
    valores = (cpf_criptografado,)
    if id_cliente is not None:
        query += " AND id_cliente <> %s"
        valores += (id_cliente,)
    cursor.execute(query, valores)
    return cursor.fetchone() is not None

def listar_clientes(termo_busca=""):

    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)
    
    print("\n--- LISTA DE CLIENTES ---")
    
    if termo_busca:

        query = "SELECT * FROM cliente WHERE nome LIKE %s OR email LIKE %s"
        cursor.execute(query, (f"%{termo_busca}%", f"%{termo_busca}%"))
    else:

        query = "SELECT * FROM cliente"
        cursor.execute(query)
        
    clientes = cursor.fetchall()
    
    if not clientes:
        print("Nenhum cliente encontrado.")
    else:
        for c in clientes:
            cpf_mascarado = descriptografar_dado(c['cpf'])
            print(f"ID: {c['id_cliente']} | Nome: {c['nome']} | CPF: {cpf_mascarado} | Tel: {c['telefone']} | E-mail: {c['email']}")
            
    cursor.close()
    conexao.close()

def cadastrar_cliente():

    print("\n--- CADASTRAR NOVO CLIENTE ---")
    nome = input("Nome: ").strip()
    cpf = solicitar_cpf("CPF (somente números): ")
    telefone = solicitar_telefone("Telefone: ")
    email = solicitar_email("E-mail: ")
    
    cpf_criptografado = criptografar_dado(cpf)
    
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    query = "INSERT INTO cliente (nome, cpf, telefone, email) VALUES (%s, %s, %s, %s)"
    valores = (nome, cpf_criptografado, telefone, email)
    
    try:
        if cpf_ja_cadastrado(cursor, cpf_criptografado):
            print("\nOps, já existe um cliente com esse CPF. Confira os números e tente novamente.")
            return
        cursor.execute(query, valores)
        conexao.commit()
        print("\nCliente cadastrado com sucesso.")
    except mysql.connector.Error as err:
        if getattr(err, "errno", None) == 1062:
            print("\nOps, já existe um cliente com esse CPF. Confira os números e tente novamente.")
        else:
            print(f"\nNão foi possível cadastrar: {err}")
    finally:
        cursor.close()
        conexao.close()

def editar_cliente():

    print("\n--- ATUALIZAR CLIENTE ---")
    listar_clientes()
    
    try:
        id_cliente = int(input("\nDigite o ID do cliente que deseja editar: "))
    except ValueError:
        print("ID inválido. Digite apenas números.")
        return
        
    nome = input("Novo Nome: ").strip()
    cpf = solicitar_cpf("Novo CPF (somente números): ")
    telefone = solicitar_telefone("Novo Telefone: ")
    email = solicitar_email("Novo E-mail: ")
    
    cpf_criptografado = criptografar_dado(cpf)
    
    conexao = conectar_banco()
    cursor = conexao.cursor()   
    
    query = "UPDATE cliente SET nome = %s, cpf = %s, telefone = %s, email = %s WHERE id_cliente = %s"
    valores = (nome, cpf_criptografado, telefone, email, id_cliente)
    
    try:
        if cpf_ja_cadastrado(cursor, cpf_criptografado, id_cliente):
            print("\nOps, outro cliente já está cadastrado com esse CPF. Confira os números e tente novamente.")
            return
        cursor.execute(query, valores)
        conexao.commit()
        if cursor.rowcount > 0:
            print("\nDados do cliente atualizados.")
        else:
            print("\nNenhum cliente encontrado com esse ID.")
    except mysql.connector.Error as err:
        if getattr(err, "errno", None) == 1062:
            print("\nOps, outro cliente já está cadastrado com esse CPF. Confira os números e tente novamente.")
        else:
            print(f"\nNão foi possível atualizar: {err}")
    finally:
        cursor.close()
        conexao.close()

def excluir_cliente():

    print("\n--- EXCLUIR CLIENTE ---")
    listar_clientes()
    
    try:
        id_cliente = int(input("\nDigite o ID do cliente que deseja excluir: "))
    except ValueError:
        print("ID inválido. Digite apenas números.")
        return
        
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    query = "DELETE FROM cliente WHERE id_cliente = %s"
    
    try:
        cursor.execute(query, (id_cliente,))
        conexao.commit()
        if cursor.rowcount > 0:
            print("\nCliente excluído.")
        else:
            print("\nNenhum cliente encontrado com esse ID.")
    except mysql.connector.Error as err:
        print(f"\nNão foi possível excluir. Verifique se o cliente tem animais cadastrados.")
    finally:
        cursor.close()
        conexao.close()

def iniciar_modulo():
    """Menu principal do módulo de clientes."""
    while True:
        print("\n" + "="*40)
        print("   MÓDULO DE CLIENTES   ")
        print("-"*40)
        print("1. Cadastrar Cliente")
        print("2. Listar Clientes")
        print("3. Buscar Cliente")
        print("4. Editar Cliente")
        print("5. Excluir Cliente")
        print("6. Voltar ao Painel Principal")
        print("="*40)
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == '1':
            cadastrar_cliente()
        elif opcao == '2':
            listar_clientes()
        elif opcao == '3':
            termo = input("\nDigite o nome ou e-mail para buscar: ").strip()
            listar_clientes(termo_busca=termo)
        elif opcao == '4':
            editar_cliente()
        elif opcao == '5':
            excluir_cliente()
        elif opcao == '6':
            print("\nVoltando...")
            break
        else:
            print("\nOpção inválida. Tente novamente.")

if __name__ == "__main__":
    iniciar_modulo()
