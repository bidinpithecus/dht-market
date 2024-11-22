import random

def calcular_dv(cpf_base):
    def calcular_primeiro_dv(cpf_base):
        soma = 0
        for i in range(9):
            soma += int(cpf_base[i]) * (10 - i)
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    def calcular_segundo_dv(cpf_base, primeiro_dv):
        soma = 0
        for i in range(9):
            soma += int(cpf_base[i]) * (11 - i)
        soma += primeiro_dv * 2
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    primeiro_dv = calcular_primeiro_dv(cpf_base)
    segundo_dv = calcular_segundo_dv(cpf_base, primeiro_dv)
    return str(primeiro_dv) + str(segundo_dv)

def gerar_cpf():
    cpf_base = ''.join([str(random.randint(0, 9)) for _ in range(9)])
    dv = calcular_dv(cpf_base)
    return cpf_base + dv

def gerar_cpfs(quantidade):
    cpfs = set()
    while len(cpfs) < quantidade:
        cpfs.add(gerar_cpf())
    return cpfs

def salvar_cpfs(cpfs, filename="db/cpfs.txt"):
    """
    Salva a lista de CPFs gerados em um arquivo de texto.
    """
    with open(filename, "w+") as f:
        for cpf in cpfs:
            f.write(cpf + "\n")
        f.close()

quantidade = 10
cpfs = gerar_cpfs(quantidade)

salvar_cpfs(cpfs)
print(f"{quantidade} CPFs válidos foram gerados e salvos em 'cpfs.txt'.")
