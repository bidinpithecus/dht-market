import argparse
import asyncio
from envparse import Env
from kademlia.network import Server

server = Server()

env = Env()
env.read_envfile()
LOJAS = env.int("LOJAS", default=64)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Populate DHT with CPFs")

    parser.add_argument(
        "-p", "--port", 
        required=True, 
        type=int, 
        help="Port number for the local node (for listening)."
    )

    parser.add_argument(
        "-i", "--ip", 
        type=str, 
        help="IP address of the bootstrap node."
    )

    parser.add_argument(
        "-r", "--remote-port", 
        type=int, 
        required=True, 
        help="Port number of the bootstrap node."
    )

    return parser.parse_args()

async def connect_to_bootstrap_node(ip: str, remote_port: int, local_port: int):
    await server.listen(local_port)
    bootstrap_node = (ip, remote_port)

    try:
        await server.bootstrap([bootstrap_node])
        print(f"Connected to bootstrap node at {ip}:{remote_port}")
        await populate()
    except Exception as e:
        print(f"Error connecting to bootstrap node: {e}")
    finally:
        server.stop()

async def populate():
    for chunk in range(LOJAS):
        chunk_filename = f"db/chunk{chunk + 1}.txt"
        try:
            with open(chunk_filename, "r") as c:
                cpfs = c.readlines()
                for cpf in cpfs:
                    cpf = cpf.strip()
                    await server.set(cpf, chunk + 1)
                print(f"Processed chunk {chunk + 1}")
        except FileNotFoundError:
            print(f"File {chunk_filename} not found.")
            continue

    print(f"DHT populated with {LOJAS} chunks.")

async def main():
    args = parse_arguments()

    if not args.ip or not args.remote_port or not args.port:
        raise argparse.ArgumentTypeError("'--ip', '--remote-port', and '--port' are required for connecting to a node.")

    await connect_to_bootstrap_node(args.ip, args.remote_port, args.port)

if __name__ == "__main__":
    asyncio.run(main())
