import asyncio
import argparse

from kademlia.network import Server

def parse_arguments():
    parser = argparse.ArgumentParser(description="Set ")

    parser.add_argument(
        "-p", "--port", 
        required=True, 
        type=int, 
        help="Port number for the local node (for listening)."
    )

    parser.add_argument(
        "-i", "--ip", 
        required=True, 
        type=str, 
        help="IP address of the bootstrap node."
    )

    parser.add_argument(
        "-r", "--remote-port", 
        required=True, 
        type=int, 
        help="Port number of the bootstrap node."
    )

    parser.add_argument(
        "-k", "--key",
        required=True, 
        help="Key to set."
    )

    return parser.parse_args()

async def run(ip, remote_port, local_port, key):
    server = Server()
    await server.listen((local_port))
    bootstrap_node = (ip, remote_port)
    await server.bootstrap([bootstrap_node])

    try:
        result = await server.get(key)
        if result == None:
            print(f"Unknown key {key}")
        else:
            print("Get result:", result)
    except Exception as e:
        print("Error retrieving the key:", e)

    server.stop()

async def main():
    args = parse_arguments()

    if not args.ip or not args.remote_port or not args.port or not args.key:
        raise argparse.ArgumentTypeError("'--ip', '--remote-port', '--port' and '--key' are required for connecting to a node.")
    await run(args.ip, int(args.remote_port), int(args.port), args.key)

if __name__ == "__main__":
    asyncio.run(main())
