import sys
import cliente
import animal
import agenda

def exibir_painel_principal(sessao_ativa): #parametro pra ver se ta logado
   

   
    if not sessao_ativa or not sessao_ativa.get("id_usuario"):
        print("\nAcesso negado. Faça login para continuar.")
        return

    while True:
        print("\n" + "-"*45)
        print("   SISTEMA DE PETSHOP - SAEP   ")
        print("-"*45)
        print(f" Usuário Logado: {sessao_ativa.get('nome')}")
        print("-" * 45)
        print("1. Clientes ")
        print("2. Animais ")
        print("3. Agenda ")
        print("4. Sair ")
        print("-"*45)
        opcao = input("O que você deseja fazer? ").strip()
        
        if opcao == '1':
            print("\nAbrindo o módulo de Clientes...")
            cliente.iniciar_modulo()
            
        elif opcao == '2':
            print("\nAbrindo o módulo de Animais...")
            animal.iniciar_modulo()
            
        elif opcao == '3':
            print("\nAbrindo o módulo de Agendamentos...")
            agenda.iniciar_modulo()
            
        elif opcao == '4':
            print(f"\nAté logo, {sessao_ativa.get('nome')}!")
            
           
            sessao_ativa.clear()
            print("Você saiu do sistema.")
            break
            
        else:
            print("\nOpção inválida. Escolha um número de 1 a 4.")

if __name__ == "__main__":
    exibir_painel_principal()
