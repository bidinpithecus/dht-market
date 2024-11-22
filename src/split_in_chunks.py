from envparse import Env

env = Env()
env.read_envfile()
LOJAS = env.int("LOJAS", default = 64)
USERS = env.int("USERS", default = 64)

def split_in_chunks(chunks):
    with open("db/cpfs.txt", "r") as f:
        cpfs = f.readlines()
        buffer = [[] for _ in range(chunks)]
        for cpf in cpfs:
            buffer[int(cpf) % chunks - 1].append(cpf)
        for chunk in range(chunks):
            with open("db/chunk" + str(chunk + 1) + ".txt", "w+") as c:
                c.write("".join(str(e) for e in buffer[chunk - 1]))
                c.close()
        f.close()

split_in_chunks(LOJAS)

rangeStr = "{1.." + str(LOJAS) + "}"
print(f"{USERS} CPFs foram separados em {LOJAS} chunks e salvo em db/chunk{rangeStr}.txt'.")
