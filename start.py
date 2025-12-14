import asyncio
from fastmcp import Client, FastMCP

from mcp_server import mcp

client = Client(mcp)


async def main():
    async with client:
        await client.ping()

        #list available tools
        tools = await client.list_tools()
        print("Available tools:", tools)

        resources = await client.list_resources()
        print("Available resources:", resources)

        prompts = await client.list_prompts()
        print("Available prompts:", prompts)

        result = await client.call_tool("add", {"a": 5, "b": 7})
        print("Result of add(5, 7):", result.content[0].text)

asyncio.run(main())