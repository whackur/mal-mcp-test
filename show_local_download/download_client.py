import asyncio
import mcp.types as types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """MCP 클라이언트를 사용하여 다운로드 서버와 상호 작용합니다."""
    server_params = StdioServerParameters(
        command="python",
        args=["show_local_download/download_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 1. 도구 목록 출력
            print("--- 사용 가능한 도구 ---")
            tools_response = await session.list_tools()
            for tool in tools_response.tools:
                print(f"- {tool.name}: {tool.description}")

            # 2. list_download_files 도구 호출
            print("\n--- 'list_download_files' 도구 호출 중... ---")
            tool_name = "list_download_files"

            result = await session.call_tool(tool_name)

            if result.content:
                content_block = result.content[0]
                if isinstance(content_block, types.TextContent):
                    print("\n--- 다운로드 폴더 파일 목록 ---")
                    print(content_block.text)
                    print("--------------------------")


if __name__ == "__main__":
    asyncio.run(main())
