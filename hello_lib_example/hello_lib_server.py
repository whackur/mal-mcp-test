import logging
import sys
from mcp.server.fastmcp import FastMCP

# 파일 기반 로깅 설정
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="hello_lib_server.log",
    filemode="w",
    encoding="utf-8",  # 명시적으로 인코딩 설정
)

# 콘솔(stderr) 로깅 추가
console_handler = logging.StreamHandler(sys.stderr)
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

logging.info("Server script started")

try:
    # FastMCP 서버 인스턴스 생성
    mcp = FastMCP("python-hello-lib-server")
    logging.info("FastMCP instance created successfully")

    @mcp.tool(
        name="hello_python_lib",
        description="A tool that returns a simple greeting from the Python MCP library.",
    )
    def hello_python_lib(name: str) -> str:
        """간단한 인사말을 반환합니다."""
        logging.info(f"'hello_python_lib' tool called with name={name}")
        result = f"Hello, {name}! This is a greeting from the Python MCP library."
        logging.info(f"Returning result: {result}")
        return result

    if __name__ == "__main__":
        logging.info("Server ready to run (mcp.run())")
        # stdio를 통해 서버 실행
        mcp.run()
        logging.info("Server execution finished")

except Exception as e:
    logging.error(f"Exception during server initialization: {e}", exc_info=True)
    raise
