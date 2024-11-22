import argparse
import asyncio
from envparse import Env
from kademlia.network import Server

server = Server()

env = Env()
env.read_envfile()
CHUNKS = env.int("CHUNKS", default = 64)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Populate dht")

    # Port argument (always needed)
    parser.add_argument(
        "-p", "--port", 
        required=True, 
        type=int, 
        help="Port number for the local node (for listening)."
    )

    # IP argument (only needed when connecting to a node)
    parser.add_argument(
        "-i", "--ip", 
        type=str, 
        help="IP address of the bootstrap node."
    )

    # Remote port argument (only needed when connecting to a node)
    parser.add_argument(
        "-r", "--remote-port", 
        type=int, 
        help="Port number of the bootstrap node."
    )

    return parser.parse_args()

async def connect_to_bootstrap_node(ip: str, remote_port: int, local_port: int):
    await server.listen(local_port)
    bootstrap_node = (ip, remote_port)
    await server.bootstrap([bootstrap_node])

    await populate()

    server.stop()

async def populate():
    for chunk in range(CHUNKS):
        print(f"Chunk {chunk} started.")
        with open("db/chunk" + str(chunk) + ".txt", "r") as c:
            cpfs = c.readlines()
            for cpf in cpfs:
                await server.set(cpf,chunk)
            c.close()
        print(f"Chunk {chunk} finichad.")

async def main():
    args = parse_arguments()

    if not args.ip or not args.remote_port or not args.port:
        raise argparse.ArgumentTypeError("'--ip' and '--remote-port' and '--port' are required for connecting to a node.")
    await connect_to_bootstrap_node(args.ip, args.remote_port, args.port)

if __name__ == "__main__":
    asyncio.run(main())
