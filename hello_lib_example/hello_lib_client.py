import asyncio
import mcp.types as types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """Interacts with the MCP server using the MCP client."""
    server_params = StdioServerParameters(
        command="python",
        args=["hello_lib_example/hello_lib_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 1. List tools
            print("--- Available Tools ---")
            tools_response = await session.list_tools()
            for tool in tools_response.tools:
                print(f"- {tool.name}: {tool.description}")

            # 2. Call a tool
            print("\n--- Calling a Tool ---")
            tool_name = "hello_python_lib"
            tool_input = {"name": "Library User"}

            result = await session.call_tool(tool_name, arguments=tool_input)

            if result.content:
                content_block = result.content[0]
                if isinstance(content_block, types.TextContent):
                    print(f"Server response: {content_block.text}")


if __name__ == "__main__":
    asyncio.run(main())
