from envparse import Env

env = Env()
env.read_envfile()
LOJAS = env.int("LOJAS", default = 64)
USERS = env.int("USERS", default = 64)

with open("db/cpfs.txt", "r") as f:
    cpfs = f.readlines()
    buffer = [[] for _ in range(LOJAS)]
    for cpf in cpfs:
        buffer[int(cpf) % LOJAS - 1].append(cpf)
    for chunk in range(LOJAS):
        with open("db/chunk" + str(chunk + 1) + ".txt", "w+") as c:
            c.write("".join(str(e) for e in buffer[chunk - 1]))
            c.close()
    f.close()

rangeStr = "{1.." + str(LOJAS) + "}"
print(f"{USERS} CPFs foram separados em {LOJAS} chunks e salvo em db/chunk{rangeStr}.txt'.")
