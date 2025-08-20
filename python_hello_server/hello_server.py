import sys
import json
import logging

# 표준 입출력 인코딩을 UTF-8로 강제합니다.
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')

# 로깅을 표준 에러(stderr)로 설정합니다.
logging.basicConfig(stream=sys.stderr, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_response(response_id, result):
    """JSON-RPC 응답을 표준 출력(stdout)으로 보냅니다."""
    response = {
        "jsonrpc": "2.0",
        "id": response_id,
        "result": result
    }
    message = json.dumps(response, ensure_ascii=False)
    sys.stdout.write(f"{message}\n")
    sys.stdout.flush()
    logging.info(f"응답 전송: {message}")

def send_error(response_id, code, message):
    """JSON-RPC 에러 응답을 표준 출력(stdout)으로 보냅니다."""
    response = {
        "jsonrpc": "2.0",
        "id": response_id,
        "error": {
            "code": code,
            "message": message
        }
    }
    message = json.dumps(response, ensure_ascii=False)
    sys.stdout.write(f"{message}\n")
    sys.stdout.flush()
    logging.info(f"에러 전송: {message}")

def handle_list_tools():
    """listTools 요청을 처리합니다."""
    return {
        "tools": [
            {
                "name": "hello_python",
                "description": "Python MCP 서버에서 간단한 인사말을 반환하는 도구입니다.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "인사할 이름."
                        }
                    },
                    "required": ["name"]
                }
            }
        ]
    }

def handle_call_tool(params):
    """callTool 요청을 처리합니다."""
    tool_name = params.get("name")
    if tool_name != "hello_python":
        raise ValueError(f"알 수 없는 도구: {tool_name}")

    args = params.get("arguments", {})
    user_name = args.get("name")

    if not user_name:
        raise ValueError("필수 인자 누락: name")

    return {
        "content": [
            {
                "type": "text",
                "text": f"안녕하세요, {user_name}님! Python MCP 서버로부터의 인사입니다."
            }
        ]
    }

def main_loop():
    """서버의 메인 이벤트 루프입니다."""
    logging.info("Python MCP 서버가 시작되었습니다. Stdin에서 수신 대기 중입니다.")
    for line in sys.stdin:
        try:
            line = line.strip()
            if not line:
                continue

            logging.info(f"메시지 수신: {line}")
            request = json.loads(line)
            request_id = request.get("id")
            method = request.get("method")
            params = request.get("params", {})

            if method == "initialize":
                client_protocol_version = params.get("protocolVersion")
                result = {
                    "protocolVersion": client_protocol_version,
                    "serverInfo": {
                        "name": "python-hello-server",
                        "version": "0.1.0"
                    },
                    "capabilities": { "resources": {}, "tools": {} }
                }
                send_response(request_id, result)
            elif method == "tools/list":
                result = handle_list_tools()
                send_response(request_id, result)
            elif method == "tools/call":
                result = handle_call_tool(params)
                send_response(request_id, result)
            elif method in ["resources/list", "resources/templates/list"]:
                # 이 서버는 리소스를 제공하지 않으므로 빈 목록을 반환합니다.
                send_response(request_id, {"resources": []})
            elif method == "notifications/initialized":
                # 초기화 완료 알림, 응답 필요 없음.
                logging.info("Initialized notification received, ignoring.")
                continue
            else:
                send_error(request_id, -32601, "메서드를 찾을 수 없음")

        except json.JSONDecodeError:
            logging.error("Stdin에서 JSON 디코딩 실패.")
            send_error(None, -32700, "파싱 에러")
        except Exception as e:
            logging.error(f"에러 발생: {e}")
            send_error(request.get("id"), -32603, f"내부 에러: {e}")


if __name__ == "__main__":
    main_loop()
