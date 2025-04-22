usuarios = {
    "admin": "admin"
}

autorizacao = "101220"

def cadastroUsuarios():
    print("\n--- CADASTRAR USUÁRIO ---")
    codigo = input("Digite o código de autorização: ")
    if codigo != autorizacao:
        print("Código incorreto. Acesso negado.")
        return

    while True:
        novo_usuario = input("Novo nome de usuário: ").strip()
        if not novo_usuario:
            print("Usuário não pode ser vazio!")
            continue
        if novo_usuario in usuarios:
            print("Usuário já existe!")
            continue

        nova_senha = input("Senha: ").strip()
        if not nova_senha:
            print("Senha não pode ser vazia!")
            continue

        usuarios[novo_usuario] = nova_senha
        print(f"Usuário '{novo_usuario}' cadastrado com sucesso!")
        break


