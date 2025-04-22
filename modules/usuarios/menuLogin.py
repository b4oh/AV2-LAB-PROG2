from modules.usuarios.login import login
from modules.usuarios.cadastro import cadastroUsuarios

def menuLogin():
    while True:
        print("\n--- MENU LOGIN ---")
        print("1 - Fazer Login")
        print("2 - Cadastrar Novo Usuário")
        print("3 - Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            if login():
                return True
        elif escolha == '2':
            cadastroUsuarios()
        elif escolha == '3':
            print("Saindo!")
            return False
        else:
            print("Opção inválida!")