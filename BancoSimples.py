from datetime import datetime

print("Bem-vindo ao Banco FabrVasconcelos!")

menu = """
Escolha uma das opções:
[1] Depositar
[2] Sacar
[3] Extrato
[9] Sair
=> """

Saldo = 0
Limite = 1000
Extrato = []
NumSaques = 0
LimiteSaques = 3

def Depositar():
    global Saldo, Extrato
    valor_str = input("Informe o valor do depósito: ")
    valor_str = valor_str.replace(',', '.') 
    try:
        valor = float(valor_str)
        if valor > 0:
            Saldo += valor
            Extrato.append((datetime.now(), "Depósito", valor))
        else:
            print("Operação falhou! O valor informado é inválido.")
    except ValueError:
        print("Operação falhou! Valor inválido.")

def Sacar():
    global Saldo, Extrato, NumSaques
    valor_str = input("Informe o valor do saque: ")
    valor_str = valor_str.replace(',', '.')
    try:
        valor = float(valor_str)
        if valor > Saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
        elif valor > Limite:
            print("Operação falhou! O valor do saque excede o limite.")
        elif NumSaques >= LimiteSaques:
            print("Operação falhou! Número máximo de saques excedido.")
        elif valor > 0:
            Saldo -= valor
            Extrato.append((datetime.now(), "Saque", -valor))
            NumSaques += 1
        else:
            print("Operação falhou! O valor informado é inválido.")
    except ValueError:
        print("Operação falhou! Valor inválido.")

def VerExtrato():
    print("\n================ EXTRATO ================")
    if not Extrato:
        print("Não foram realizadas movimentações.")
    else:
        for data, descricao, valor in Extrato:
            print(f"{data.strftime('%d/%m/%Y %H:%M:%S')} - {descricao}: R$ {valor:.2f}")
    print(f"\nSaldo: R$ {Saldo:.2f}")
    print("==========================================")

while True:
    opcao = input(menu)
    if opcao == "1":
        Depositar()
    elif opcao == "2":
        Sacar()
    elif opcao == "3":
        VerExtrato()
    elif opcao == "9":
        print("Agradecemos sua visita!")
        break
    else:
        print("Operação inválida, Por favor selecione novamente a operação desejada.")