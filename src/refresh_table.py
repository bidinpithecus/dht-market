import asyncio
import sys

from kademlia.network import Server

if len(sys.argv) != 4:
    print("Usage: python get.py <IP> <remote_port> <local_port>")
    sys.exit(1)

async def run():
    server = Server()
    await server.listen(sys.argv[3])
    bootstrap_node = (sys.argv[1], int(sys.argv[2]))
    await server.bootstrap([bootstrap_node])

    server.refresh_table()
    server.stop()

asyncio.run(run())
