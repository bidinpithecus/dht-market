import random
import os
from envparse import Env
from multiprocessing import Pool
from tqdm import tqdm

env = Env()
env.read_envfile()
USERS = env.int("USERS", default=10000000)

os.makedirs("db", exist_ok=True)

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

def gerar_cpf(_):
    cpf_base = ''.join([str(random.randint(0, 9)) for _ in range(9)])
    dv = calcular_dv(cpf_base)
    return cpf_base + dv

def gerar_cpfs(quantidade):
    with Pool() as pool:
        with tqdm(total=quantidade, desc="Gerando CPFs válidos") as pbar:
            cpfs = set()
            for cpf in pool.imap_unordered(gerar_cpf, range(quantidade)):
                cpfs.add(cpf)
                pbar.update(1)
    return cpfs

def salvar_cpfs(cpfs, filename="db/cpfs.txt"):
    with open(filename, "w+") as f:
        for cpf in cpfs:
            f.write(cpf + "\n")

cpfs = gerar_cpfs(USERS)
salvar_cpfs(cpfs)
print(f"{USERS} CPFs válidos foram gerados e salvos em 'db/cpfs.txt'.")
