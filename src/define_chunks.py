from envparse import Env

env = Env()
env.read_envfile()
CHUNKS = env.int("CHUNKS", default = 64)

with open("db/cpfs.txt", "r") as f:
    cpfs = f.readlines()
    buffer = [[] for _ in range(CHUNKS)]
    for cpf in cpfs:
        buffer[int(cpf) % CHUNKS - 1].append(cpf)
    for chunk in range(CHUNKS):
        with open("db/chunk" + str(chunk) + ".txt", "w+") as c:
            c.write("".join(str(e) for e in buffer[chunk - 1]))
            c.close()
    f.close()

