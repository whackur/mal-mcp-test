import logging
import sys
import os
import requests
import copy
from bs4 import BeautifulSoup, SoupStrainer, XMLParsedAsHTMLWarning
import warnings
from mcp.server.fastmcp import FastMCP

# XMLParsedAsHTMLWarning 경고를 무시하도록 설정합니다.
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

# 로그 디렉토리 생성
os.makedirs("logs", exist_ok=True)

# 파일 기반 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="logs/scanner_server.log",
    filemode="w",
    encoding="utf-8",
)

# 콘솔(stderr) 로깅 추가
console_handler = logging.StreamHandler(sys.stderr)
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

logging.info("Server script started")

try:
    # FastMCP 서버 인스턴스 생성
    mcp = FastMCP("link-scanner")
    logging.info("FastMCP instance created successfully")

    @mcp.tool(
        name="scan_links",
        description="주어진 도메인의 하이퍼링크를 스캔하여 찾은 링크 목록을 반환합니다.",
    )
    def scan_links(target_domain: str) -> str:
        """주어진 도메인의 하이퍼링크를 스캔합니다."""
        results = set()

        def check_target_domain(domain: str) -> str:
            # 도메인 끝에 붙은 '/'를 제거합니다.
            if domain.endswith("/"):
                return domain[:-1]
            return domain

        def discover_directory(url: str, target: str):
            # 주어진 URL에서 하이퍼링크를 찾습니다.
            hrefs = set()
            try:
                # 타임아웃을 설정하여 무한정 기다리는 것을 방지합니다.
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
                }
                content = requests.get(url, headers=headers, timeout=5).content
                logging.info(f"Successfully fetched content from {url}")
            except requests.exceptions.RequestException as e:
                logging.error(f"Request error for {url}: {e}")
                return

            for link in BeautifulSoup(
                content, features="html.parser", parse_only=SoupStrainer("a")
            ):
                if hasattr(link, "href"):
                    try:
                        path = link["href"]
                        # 유효하지 않거나 불필요한 링크는 건너뜁니다.
                        if (
                            not path
                            or path.startswith("#")
                            or path.startswith("javascript:")
                            or path.lower().endswith(
                                (
                                    ".jpg",
                                    ".png",
                                    ".css",
                                    ".js",
                                    ".gif",
                                    ".svg",
                                    ".zip",
                                    ".pdf",
                                )
                            )
                        ):
                            continue
                        elif path.startswith("/") or path.startswith("?"):
                            hrefs.add(f"{target}{path}")
                        elif target not in path and path.startswith("http"):
                            # 외부 도메인 링크는 건너뜁니다.
                            continue
                        elif target not in path and not path.startswith("http"):
                            hrefs.add(f"{target}/{path}")
                        else:
                            hrefs.add(path)
                    except KeyError:
                        pass
                    except Exception as e:
                        logging.error(f"Error when parsing link: {e}")

            for href in hrefs:
                # 최종 결과에 대상 도메인으로 시작하는 링크만 추가합니다.
                if href.startswith(target):
                    results.add(href)

        try:
            logging.info(f"Starting scan for domain: {target_domain}")
            checked_target_domain = check_target_domain(target_domain)

            # 스캔을 시작합니다.
            discover_directory(checked_target_domain, checked_target_domain)

            links_to_scan = copy.deepcopy(results)
            scanned_links = {checked_target_domain}

            # 찾은 링크들을 순회하며 재귀적으로 스캔합니다.
            while links_to_scan:
                link = links_to_scan.pop()
                if link in scanned_links:
                    continue

                logging.info(f"Searching on ... {link}")
                scanned_links.add(link)
                discover_directory(link, checked_target_domain)

                # 새로 발견된 링크를 스캔 대상에 추가합니다.
                new_links = results - scanned_links - links_to_scan
                links_to_scan.update(new_links)

            logging.info(f"Found {len(results)} links.")
            if not results:
                return "하이퍼링크를 찾을 수 없습니다."

            # 결과를 정렬하여 반환합니다.
            return "\n".join(sorted(list(results)))

        except Exception as e:
            error_message = f"An error occurred during scanning: {e}"
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
