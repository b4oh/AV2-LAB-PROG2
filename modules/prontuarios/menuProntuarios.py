prontuarios = []  

def menuProntuarios():
    print("\n--- MENU ---")
    print("1 - Cadastrar Prontuário")
    print("2 -Exibir Prontuários")
    print("3 - Editar Prontuário")
    print("4 - Excluir Prontuário")
    print("5 - Sair")
    print("6 - Cadastrar Novo Usuário")
    return input("Escolha uma opção: ")



def cadastroProntuarios():
    while True:
        nome = input("Digite o nome do paciente: ")
        if not nome.strip():
            print("Nome não pode ser vazio. Tente novamente.")
            continue
        while True:
            idade = input("Digite a idade do paciente: ")
            if not idade.isdigit(): 
                print("Idade deve ser um número inteiro. Tente novamente.")
                continue
            idade = int(idade)  
            break

        diagnostico = input("Digite o diagnóstico do paciente: ")
        if not diagnostico.strip():
            print("Diagnóstico não pode ser vazio. Tente novamente.")
            continue
        
        prontuarios.append({
            'nome': nome,
            'idade': idade,
            'diagnostico': diagnostico
        })
        print(f"Prontuário de {nome} cadastrado com sucesso!")
        break  


def exibirProntuarios():
    if prontuarios:
        print("\n=== PRONTUÁRIOS ===")
        for i, prontuario in enumerate(prontuarios, 1):
            print(f"{i}. {prontuario['nome']} - {prontuario['idade']} anos - Diagnóstico: {prontuario['diagnostico']}")
    else:
        print("Nenhum prontuário cadastrado.")


def editarProntuarios():
    exibirProntuarios()
    if prontuarios:
        try:
            escolha = int(input("Escolha o número do prontuário para editar: ")) - 1
            if 0 <= escolha < len(prontuarios):
                while True:
                    nome = input("Novo nome do paciente: ")
                    if not nome.strip():
                        print("Nome não pode ser vazio. Tente novamente.")
                        continue
                    break

                
                while True:
                    idade = input("Nova idade do paciente: ")
                    if not idade.isdigit():  
                        print("Idade deve ser um número inteiro. Tente novamente.")
                        continue
                    idade = int(idade)  
                    break

                while True:
                    diagnostico = input("Novo diagnóstico do paciente: ")
                    if not diagnostico.strip():
                        print("Diagnóstico não pode ser vazio. Tente novamente.")
                        continue
                    break

                
                prontuarios[escolha] = {
                    'nome': nome,
                    'idade': idade,
                    'diagnostico': diagnostico
                }
                print("Prontuário editado com sucesso!")
            else:
                print("Prontuário inválido.")
        except ValueError:
            print("Opção inválida.")


def excluirProntuarios():
    exibirProntuarios()
    if prontuarios:
        try:
            escolha = input("Escolha o número do prontuário para excluir: ")
            if escolha.strip() == '':  
                print("Escolha inválida. Tente novamente.")
                return
            
            escolha = int(escolha) - 1
            if 0 <= escolha < len(prontuarios):
                prontuario = prontuarios.pop(escolha)
                print(f"Prontuário de {prontuario['nome']} excluído com sucesso!")
            else:
                print("Prontuário inválido.")
        except ValueError:
            print("Opção inválida.")
