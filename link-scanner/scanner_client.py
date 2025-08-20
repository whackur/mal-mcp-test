import asyncio
import sys
import mcp.types as types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """MCP 클라이언트를 사용하여 서버와 통신하고 링크 스캔을 요청합니다."""
    # 서버 실행을 위한 파라미터를 설정합니다.
    # sys.executable을 사용하여 현재 파이썬 환경에서 서버를 실행합니다.
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["link-scanner/scanner_server.py"],
    )

    # stdio_client를 사용하여 서버와 세션을 시작합니다.
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            try:
                # 세션을 초기화합니다.
                await session.initialize()
                print("MCP 클라이언트가 시작되었습니다. 서버에 연결 중...")

                # 사용자로부터 스캔할 도메인을 입력받습니다.
                target_domain = input(
                    "스캔할 도메인을 입력하세요 (예: https://www.example.com): "
                )
                if not target_domain:
                    print("도메인이 입력되지 않았습니다. 프로그램을 종료합니다.")
                    return

                print(f"'{target_domain}' 도메인의 링크 스캔을 요청합니다...")

                # 'scan_links' 도구를 호출합니다.
                result = await session.call_tool(
                    "scan_links", {"target_domain": target_domain}
                )

                # 결과를 처리하고 출력합니다.
                if result.content:
                    content_block = result.content[0]
                    if isinstance(content_block, types.TextContent):
                        print("\n--- 스캔 결과 ---")
                        print(content_block.text)
                        print("-----------------")

                print("\n링크 스캔이 완료되었습니다.")

            except Exception as e:
                print(f"오류가 발생했습니다: {e}")
            finally:
                print("MCP 클라이언트가 종료되었습니다.")


if __name__ == "__main__":
    # 비동기 main 함수를 실행합니다.
    asyncio.run(main())
