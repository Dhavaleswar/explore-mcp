import asyncio
import os
import json
from fastmcp import Client

if "OPENAI_API_KEY" not in os.environ:
    from utils.helpers import get_api_key
    os.environ["OPENAI_API_KEY"] = get_api_key()

from openai import AsyncOpenAI

# --- 1. Client Setup ---
LLM_PROVIDER_CLIENT = AsyncOpenAI()  # Or use Anthropic, Gemini, local Ollama client, etc.
MCP_SERVER_URL = "http://127.0.0.1:8000/mcp"


async def orchestrate_llm_agent(user_prompt: str):
    async with Client(MCP_SERVER_URL) as mcp_client:

        # --- 2. Tool Discovery & Translation ---
        mcp_tools = await mcp_client.list_tools()

        # Convert MCP Tool schema (JSON Schema) to OpenAI's Function Calling format
        llm_tools = []
        for tool in mcp_tools:
            llm_tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,  # FastMCP provides the JSON Schema
                }
            })

        messages = [{"role": "user", "content": user_prompt}]

        # --- 3. Orchestration Loop ---
        while True:
            # 1. Send query and tools to the LLM
            response = await LLM_PROVIDER_CLIENT.chat.completions.create(
                model="gpt-5",
                messages=messages,
                tools=llm_tools
            )

            tool_calls = response.choices[0].message.tool_calls

            if not tool_calls:
                # LLM decided it has the final answer (or cannot use tools)
                return response.choices[0].message.content

            # 2. LLM requests a tool call: Execute the tool using the FastMCP client
            messages.append(response.choices[0].message)  # Add tool call request to history

            for call in tool_calls:
                tool_name = call.function.name
                arguments = json.loads(call.function.arguments)

                print(f"Agent called tool: {tool_name} with arguments: {arguments}")

                # Execute the tool via the FastMCP client!
                mcp_result = await mcp_client.call_tool(tool_name, arguments)

                # Get the raw data from the result object
                tool_output = mcp_result.data

                # 3. Send the tool result back to the LLM
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "name": tool_name,
                    "content": str(tool_output),  # Send the output as a string for the LLM to read
                })

# Example run
print(asyncio.run(orchestrate_llm_agent("Add two numbers 23 and 45")))