from datetime import datetime

usuarios = {}
contas_corrente = {}
prox_numero_conta = 1

class Usuario:
    def __init__(self, nome, data_nascimento, cpf, endereco, senha):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco
        self.senha = senha

class ContaCorrente:
    def __init__(self, agencia, numero_conta, usuario):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.usuario = usuario
        self.saldo = 0
        self.extrato = []

def validar_cpf(cpf):
    cpf = cpf.replace(".", "").replace("-", "")
    if not cpf.isdigit() or len(cpf) != 11:
        return False
    return True

def validar_data(data):
    try:
        datetime.strptime(data, '%d/%m/%Y')
        return True
    except ValueError:
        return False

def validar_nome(nome):
    return nome.isalpha() and len(nome) > 3

def validar_senha(senha):
    return senha.isdigit()

def criar_usuario():
    nome = input("Informe o nome do usuário: ")
    if not validar_nome(nome):
        print("Nome inválido. Deve conter apenas letras e ter mais de 3 caracteres.")
        return None

    data_nascimento = input("Informe a data de nascimento (DD/MM/AAAA): ")
    if not validar_data(data_nascimento):
        print("Data de nascimento inválida. Utilize o formato DD/MM/AAAA.")
        return None

    cpf = input("Informe o CPF do usuário: ")
    if not validar_cpf(cpf):
        print("CPF inválido. Deve conter 11 dígitos numéricos.")
        return None

    endereco = input("Informe o endereço completo (Logradouro, número, bairro, cidade, estado): ")
    senha = input("Defina uma senha para acesso (somente números): ")
    if not validar_senha(senha):
        print("Senha inválida. Deve conter apenas números.")
        return None

    if cpf in usuarios:
        print("CPF já cadastrado. Não é permitido cadastrar o mesmo CPF novamente.")
        return None

    usuarios[cpf] = Usuario(nome, data_nascimento, cpf, endereco, senha)
    print("Usuário cadastrado com sucesso.")
    return usuarios[cpf]

def criar_conta_corrente(usuario):
    global prox_numero_conta
    global contas_corrente

    numero_conta = prox_numero_conta
    agencia = "0001"
    conta = ContaCorrente(agencia, numero_conta, usuario)
    contas_corrente[numero_conta] = conta

    prox_numero_conta += 1

    print("Conta corrente criada com sucesso.")
    return conta

def listar_usuarios_contas():
    print("\n======= CLIENTES E SUAS CONTAS =======")
    for cpf, usuario in usuarios.items():
        print(f"Nome: {usuario.nome}")
        print(f"CPF: {usuario.cpf}")
        print("Endereço:", usuario.endereco)
        print("Contas:")
        for numero_conta, conta in contas_corrente.items():
            if conta.usuario == usuario:
                print(f"    - Agência: {conta.agencia}, Conta: {conta.numero_conta}")
        print("=======================================")

def acessar_conta():
    cpf = input("Informe o CPF do Cliente para acessar a conta: ")
    if cpf in usuarios:
        senha = input("Informe a senha: ")
        if senha == usuarios[cpf].senha:
            usuario = usuarios[cpf]
            for conta in contas_corrente.values():
                if conta.usuario == usuario:
                    return conta
            print("Cliente não possui conta corrente.")
        else:
            print("Senha incorreta.")
    else:
        print("Cliente não encontrado.")
    return None

def depositar(conta):
    valor_str = input("Informe o valor do depósito: ")
    valor_str = valor_str.replace(',', '.') 
    try:
        valor = float(valor_str)
        if valor > 0:
            conta.saldo += valor
            conta.extrato.append((datetime.now(), "Depósito", valor, conta.usuario))
            print("Depósito realizado com sucesso.")
        else:
            print("Operação falhou! O valor informado é inválido.")
    except ValueError:
        print("Operação falhou! Valor inválido.")

def sacar(conta):
    valor_str = input("Informe o valor do saque: ")
    valor_str = valor_str.replace(',', '.')
    try:
        valor = float(valor_str)
        if valor > conta.saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
        elif valor > 0:
            conta.saldo -= valor
            conta.extrato.append((datetime.now(), "Saque", -valor, conta.usuario))
            print("Saque realizado com sucesso.")
        else:
            print("Operação falhou! O valor informado é inválido.")
    except ValueError:
        print("Operação falhou! Valor inválido.")

def ver_extrato(conta):
    print("\n================ EXTRATO ================")
    if not conta.extrato:
        print("Não foram realizadas movimentações.")
    else:
        for data, descricao, valor, usuario in conta.extrato:
            print(f"{data.strftime('%d/%m/%Y %H:%M:%S')} - {descricao}: R$ {valor:.2f} - Cliente: {usuario.nome}")
    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("==========================================")

## UI Back
def main():
    print("Bem-vindo ao Banco FabrVasconcelos!")

    while True:
        opcao = input("""
Escolha uma das opções:
[1] Criar Usuário
[2] Criar Conta Corrente
[3] Listar Clientes e Contas
[4] Acessar Conta
[5] Depositar
[6] Sacar
[7] Extrato
[9] Sair
=> """)

        if opcao == "1":
            criar_usuario()
        elif opcao == "2":
            cpf = input("Informe o CPF do Cliente para criar a conta corrente: ")
            if cpf in usuarios:
                criar_conta_corrente(usuarios[cpf])
            else:
                print("Cliente não encontrado.")
        elif opcao == "3":
            listar_usuarios_contas()
        elif opcao == "4":
            conta = acessar_conta()
            if conta:
                print(f"Conta acessada com sucesso. Agência: {conta.agencia}, Conta: {conta.numero_conta}")
        elif opcao == "5":
            conta = acessar_conta()
            if conta:
                depositar(conta)
        elif opcao == "6":
            conta = acessar_conta()
            if conta:
                sacar(conta)
        elif opcao == "7":
            conta = acessar_conta()
            if conta:
                ver_extrato(conta)
        elif opcao == "9":
            print("Agradecemos sua visita!")
            break
        else:
            print("Operação inválida. Por favor, selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()