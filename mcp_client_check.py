from fastmcp.client import Client
# from fastmcp.c
import asyncio

url = "http://127.0.0.1:8000/mcp"

client = Client(url)

async def main():
    async with client:
        await client.ping()

        tools = await client.list_tools()

        print(tools)

asyncio.run(main())