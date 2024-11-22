import asyncio
import sys

from kademlia.network import Server

if len(sys.argv) != 4:
    print("Usage: python get.py <bootstrap node> <bootstrap port> <key>")
    sys.exit(1)

async def run():
    server = Server()
    await server.listen(8470)
    bootstrap_node = (sys.argv[1], int(sys.argv[2]))
    await server.bootstrap([bootstrap_node])

    result = await server.get(sys.argv[3])
    print("Get result:", result)
    server.stop()

asyncio.run(run())
