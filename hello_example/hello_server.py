import sys
import json
import logging

# stdout/stderr/stdin을 UTF-8로 강제합니다.
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
sys.stdin.reconfigure(encoding="utf-8")

# stderr에 로깅을 구성합니다.
logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def send_response(response_id, result):
    """stdout으로 JSON-RPC 응답을 보냅니다."""
    response = {"jsonrpc": "2.0", "id": response_id, "result": result}
    message = json.dumps(response, ensure_ascii=False)
    sys.stdout.write(f"{message}\n")
    sys.stdout.flush()
    logging.info(f"Sent response: {message}")


def send_error(response_id, code, message):
    """stdout으로 JSON-RPC 오류 응답을 보냅니다."""
    response = {
        "jsonrpc": "2.0",
        "id": response_id,
        "error": {"code": code, "message": message},
    }
    message = json.dumps(response, ensure_ascii=False)
    sys.stdout.write(f"{message}\n")
    sys.stdout.flush()
    logging.info(f"Sent error: {message}")


def handle_list_tools():
    """listTools 요청을 처리합니다."""
    return {
        "tools": [
            {
                "name": "hello_python",
                "description": "A tool that returns a simple greeting from the Python MCP server.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "The name to greet."}
                    },
                    "required": ["name"],
                },
            }
        ]
    }


def handle_call_tool(params):
    """callTool 요청을 처리합니다."""
    tool_name = params.get("name")
    if tool_name != "hello_python":
        raise ValueError(f"Unknown tool: {tool_name}")

    args = params.get("arguments", {})
    user_name = args.get("name")

    if not user_name:
        raise ValueError("Missing required argument: name")

    return {
        "content": [
            {
                "type": "text",
                "text": f"Hello, {user_name}! This is a greeting from the Python MCP server.",
            }
        ]
    }


def main_loop():
    """서버의 메인 이벤트 루프입니다."""
    logging.info("Python MCP server started. Listening on stdin.")
    for line in sys.stdin:
        try:
            line = line.strip()
            if not line:
                continue

            logging.info(f"Received message: {line}")
            request = json.loads(line)
            request_id = request.get("id")
            method = request.get("method")
            params = request.get("params", {})

            if method == "initialize":
                client_protocol_version = params.get("protocolVersion")
                result = {
                    "protocolVersion": client_protocol_version,
                    "serverInfo": {"name": "python-hello-server", "version": "0.1.0"},
                    "capabilities": {"resources": {}, "tools": {}},
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
                # 초기화 완료 알림으로, 응답이 필요 없습니다.
                logging.info("Initialized notification received, ignoring.")
                continue
            else:
                send_error(request_id, -32601, "Method not found")

        except json.JSONDecodeError:
            logging.error("Failed to decode JSON from stdin.")
            send_error(None, -32700, "Parse error")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            send_error(request.get("id"), -32603, f"Internal error: {e}")


if __name__ == "__main__":
    main_loop()
