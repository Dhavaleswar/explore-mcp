# python
from utils.helpers import get_api_key
import os
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
from openai import OpenAI

# Ensure the OpenAI API key is available to the OpenAI SDK
os.environ["OPENAI_API_KEY"] = get_api_key()

# Use the base URL; the MCP client will handle any internal MCP pathing.
TOOL_SERVER_URL = "http://localhost:8000/mcp/"

client = OpenAI()

response = client.responses.create(
    model="gpt-4.1",
    input="call ping",
    tools=[
        {
            "type": "mcp",
            "server_label": "local-fastmcp",
            "server_url": TOOL_SERVER_URL,
            "require_approval": "never"
        }
    ],
)

print(response.output_text)
