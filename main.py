
def menu():
    print("--- Prontuario Eletrônico ---")
    while True:
        print("1 - Fazer login")
        print("2 -  Cadastrar novo usuário")
        print("3 - Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            if login():
                print("Entrando no sistema!")
                break
        elif escolha == "2":
            cadastroUsuario()
        elif escolha == "3":
            print("Saindo.")
        else:
            print("Opção inválida.")

menu()