import logging
import sys
from pathlib import Path
import os
from mcp.server.fastmcp import FastMCP

# 파일 기반 로깅 설정
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="download_server.log",
    filemode="w",
    encoding="utf-8",
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
    mcp = FastMCP("show-local-download")
    logging.info("FastMCP instance created successfully")

    @mcp.tool(
        name="list_download_files",
        description="사용자의 다운로드 폴더에 있는 파일 및 폴더 목록을 반환합니다.",
    )
    def list_download_files() -> str:
        """사용자의 다운로드 폴더에 있는 파일 목록을 반환합니다."""
        try:
            # 여러 운영체제에서 다운로드 폴더 경로를 가져옵니다.
            downloads_path = Path.home() / "Downloads"
            logging.info(f"Accessing downloads path: {downloads_path}")

            if not downloads_path.exists() or not downloads_path.is_dir():
                error_message = f"Downloads directory not found at: {downloads_path}"
                logging.error(error_message)
                return error_message

            # 디렉터리 내의 파일 및 폴더 목록을 가져옵니다.
            file_list = [f.name for f in downloads_path.iterdir()]

            if not file_list:
                return "다운로드 폴더에 파일이 없습니다."

            result = "\n".join(file_list)
            logging.info(f"Found {len(file_list)} files/folders.")
            return result

        except Exception as e:
            error_message = f"An error occurred while listing files: {e}"
            logging.error(error_message, exc_info=True)
            return error_message

    if __name__ == "__main__":
        logging.info("Server ready to run (mcp.run())")
        # stdio를 통해 서버 실행
        mcp.run()
        logging.info("Server execution finished")

except Exception as e:
    logging.error(f"Exception during server initialization: {e}", exc_info=True)
    raise
