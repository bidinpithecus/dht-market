import os
from envparse import Env
from multiprocessing import Pool
from tqdm import tqdm

env = Env()
env.read_envfile()
LOJAS = env.int("LOJAS", default=64)
USERS = env.int("USERS", default=10000000)

def split_in_chunks(chunk_index, cpfs, chunks):
    buffer = [[] for _ in range(chunks)]

    for cpf in cpfs:
        buffer[int(cpf.strip()) % chunks - 1].append(cpf)

    with open(f"db/chunk{chunk_index + 1}.txt", "w+") as c:
        c.write("".join(str(e) for e in buffer[chunk_index]))

    return chunk_index  # Return index for progress tracking

def process_chunks(chunks):
    with open("db/cpfs.txt", "r") as f:
        cpfs = f.readlines()

    os.makedirs("db", exist_ok=True)

    with Pool() as pool:
        with tqdm(total=chunks, desc="Separating CPFs into chunks") as pbar:
            result = [pool.apply_async(split_in_chunks, (i, cpfs, chunks), callback=lambda _: pbar.update(1)) for i in range(chunks)]
            [r.get() for r in result]

process_chunks(LOJAS)

rangeStr = "{1.." + str(LOJAS) + "}"
print(f"{USERS} CPFs foram separados em {LOJAS} chunks e salvos em db/chunk{rangeStr}.txt'.")
