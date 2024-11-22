import argparse
import asyncio
import logging
from kademlia.network import Server

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.DEBUG)

server = Server()

def parse_arguments():
    parser = argparse.ArgumentParser(description="Kademlia Node Operations")
    
    # Node type argument (required)
    parser.add_argument(
        "-t", "--type", 
        choices=['n', 'c'], 
        required=True, 
        help="'n' creates a new node, 'c' connects to an existing node."
    )
    
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
        help="IP address of the bootstrap node (required for 'c')."
    )
    
    # Remote port argument (only needed when connecting to a node)
    parser.add_argument(
        "-r", "--remote-port", 
        type=int, 
        help="Port number of the bootstrap node (required for 'c')."
    )
    
    return parser.parse_args()

async def handle_user_input():
    while True:
        command = input(">> ").strip().lower()

        if command.startswith("get"):
            try:
                _, key = command.split(maxsplit=1)
                value = await server.get(key)
                if value is None:
                    print(f"No value found for key: {key}")
                else:
                    print(f"Value for key '{key}': {value}")
            except ValueError:
                print("Usage: get <key>")
            except Exception as e:
                print(f"Error while retrieving value: {e}")

        elif command.startswith("set"):
            try:
                _, key, value = command.split(maxsplit=2)
                await server.set(key, value)
                print(f"Key '{key}' set to value '{value}'.")
            except ValueError:
                print("Usage: set <key> <value>")
            except Exception as e:
                print(f"Error while setting value: {e}")

        elif command == "who":
            peers = server.bootstrappable_neighbors()
            if not peers:
                print("No peers connected.")
            else:
                print("Connected peers:")
                for peer in peers:
                    print(peer)

        elif command == "exit":
            print("Exiting...")
            server.stop()
            break
        
        else:
            print(f"Unknown command: {command}")

def connect_to_bootstrap_node(ip: str, remote_port: int, local_port: int):
    loop = asyncio.get_event_loop()

    loop.run_until_complete(server.listen(local_port))
    bootstrap_node = (ip, remote_port)
    loop.run_until_complete(server.bootstrap([bootstrap_node]))

    try:
        print(f"Connected to bootstrap node at {ip}:{remote_port}. Listening on port {local_port}.")
        loop.run_forever()
    except KeyboardInterrupt:
        print("Shutting down the node.")
    finally:
        server.stop()
        loop.close()

async def create_bootstrap_node(port: int):
    await server.listen(port)
    print(f"Bootstrap node started and listening on port {port}. Type 'who' to list connected peers, 'get <key>' to get a key if the network has it, 'set <key> <value>' to set the given string key to the given value in the network, 'exit' to quit.")

    await handle_user_input()

def old_create_bootstrap_node(port):
    loop = asyncio.get_event_loop()
    loop.set_debug(True)

    loop.run_until_complete(server.listen(port))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
        loop.close()

def main():
    args = parse_arguments()

    if args.type == 'n':
        # Creating a new bootstrap node
        if args.ip or args.remote_port:
            raise argparse.ArgumentTypeError("'--ip' and '--remote-port' should not be provided for creating a new node.")
        # loop = asyncio.get_event_loop()
        # loop.set_debug(True)
        # try:
        #     loop.run_until_complete(create_bootstrap_node(args.port))
        # except KeyboardInterrupt:
        #     print("Shutting down the node.")
        # finally:
        #     server.stop()
        #     loop.close()
        old_create_bootstrap_node(args.port)

    elif args.type == 'c':
        # Connecting to an existing node
        if not args.ip or not args.remote_port:
            raise argparse.ArgumentTypeError("'--ip' and '--remote-port' are required for connecting to a node.")
        connect_to_bootstrap_node(args.ip, args.remote_port, args.port)

if __name__ == "__main__":
    main()
