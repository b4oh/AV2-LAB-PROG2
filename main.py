from modules.prontuarios.menuProntuarios import menuProntuarios, cadastroProntuarios, exibirProntuarios, editarProntuarios, excluirProntuarios
from modules.usuarios.menuLogin import menuLogin

def main():
    if menuLogin():  
        print("Login feito!")

        while True:
            escolha = menuProntuarios()

            if escolha == '1':
                cadastroProntuarios()
            elif escolha == '2':
                exibirProntuarios()
            elif escolha == '3':
                editarProntuarios()
            elif escolha == '4':
                excluirProntuarios()
            elif escolha == '5':
                print("Saindo do sistema!")
                break
            else:
                print("Opção inválida! Tente novamente.")
    else:
        print("Sistema encerrado.")

main()