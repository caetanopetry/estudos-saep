import mysql.connector
import bcrypt   
import sys
import getpass
import main
from datetime import datetime, timedelta


sessao_ativa = {
    "id_usuario": None,
    "nome": None,
    "expira_em": None
}

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

def realizar_login():
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)
    
    while True:
        print("\n--- LOGIN DO PETSHOP ---")
        email_digitado = input("E-mail: ").strip()
        senha_digitada = getpass.getpass("Senha: ").strip()
        
        query = "SELECT id_usuario, nome, senha FROM usuario WHERE email = %s"
        cursor.execute(query, (email_digitado,))
        usuario = cursor.fetchone()
        
  
        if usuario:
          
            try:
                senha_valida = bcrypt.checkpw(senha_digitada.encode('utf-8'), usuario['senha'].encode('utf-8'))
            except ValueError:
                
                senha_valida = False

            if senha_valida:
                
                sessao_ativa["id_usuario"] = usuario["id_usuario"]
                sessao_ativa["nome"] = usuario["nome"]
                sessao_ativa["expira_em"] = datetime.now() + timedelta(minutes=10)
                
                print(f"\nBem-vindo, {usuario['nome']}!")
                main.exibir_painel_principal(sessao_ativa)
                break
            else:
                print("Senha incorreta. Tente novamente.")
        else:
            print("E-mail não encontrado. Tente novamente.")
            
    cursor.close()
    conexao.close()

def verificar_sessao():
    if not sessao_ativa.get("id_usuario"):
        print("Acesso negado. Faça login primeiro.")
        return False
    
    if datetime.now() > sessao_ativa["expira_em"]:
        print("\nSua sessão expirou. Faça login novamente.")
        sessao_ativa["id_usuario"] = None
        sessao_ativa["nome"] = None
        sessao_ativa["expira_em"] = None
        return False
        
    return True

def funcionalidade_principal():
    print(f"\n--- PAINEL PRINCIPAL ---")
    print(f"Usuário Logado: {sessao_ativa['nome']}")
    print(f"Sessão válida até: {sessao_ativa['expira_em'].strftime('%H:%M:%S')}")
    print("1. Acessar Clientes")
    print("2. Sair do Sistema")
    input("Pressione Enter para continuar...")

if __name__ == "__main__":
    realizar_login()
    
    if verificar_sessao():
        funcionalidade_principal()
