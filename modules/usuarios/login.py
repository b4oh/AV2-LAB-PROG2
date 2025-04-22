from modules.usuarios.cadastro import usuarios

def login():
    print("\n--- LOGIN ---")
    usuario = input("Usuário: ")
    senha = input("Senha: ")

    if usuario in usuarios:
        if usuarios[usuario] == senha:
            print("Entrando no sistema!")
            return True
        else:
            print("Senha incorreta!")
    else:
        print("Usuário não existe!")
    
    return False
