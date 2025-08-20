import sys
import json
import logging

# Force stdout/stderr/stdin to be UTF-8
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
sys.stdin.reconfigure(encoding="utf-8")

# Configure logging to stderr
logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def send_response(response_id, result):
    """Sends a JSON-RPC response to stdout."""
    response = {"jsonrpc": "2.0", "id": response_id, "result": result}
    message = json.dumps(response, ensure_ascii=False)
    sys.stdout.write(f"{message}\n")
    sys.stdout.flush()
    logging.info(f"Sent response: {message}")


def send_error(response_id, code, message):
    """Sends a JSON-RPC error response to stdout."""
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
    """Handles the listTools request."""
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
    """Handles the callTool request."""
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
    """The main event loop for the server."""
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
                # This server does not provide resources, so return an empty list.
                send_response(request_id, {"resources": []})
            elif method == "notifications/initialized":
                # Initialized notification, no response needed.
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
