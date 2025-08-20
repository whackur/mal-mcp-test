import json
import sys
import subprocess
import threading

# Force stdout/stderr/stdin to be UTF-8
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
sys.stdin.reconfigure(encoding="utf-8")


def send_request(process, method, params, request_id):
    """Sends a JSON-RPC request to the specified process."""
    request = {"jsonrpc": "2.0", "id": request_id, "method": method, "params": params}
    message = json.dumps(request, ensure_ascii=False) + "\n"
    process.stdin.write(message.encode("utf-8"))
    process.stdin.flush()
    print(f"Client -> Server: {message.strip()}", file=sys.stderr)


def read_responses(process):
    """Reads and prints responses from the server."""
    for line in iter(process.stdout.readline, b""):
        print(f"Server -> Client: {line.decode('utf-8').strip()}", file=sys.stderr)

    for line in iter(process.stderr.readline, b""):
        print(f"Server (stderr): {line.decode('utf-8').strip()}", file=sys.stderr)


if __name__ == "__main__":
    # Start the MCP server process
    server_command = [sys.executable, "hello_example/hello_server.py"]
    server_process = subprocess.Popen(
        server_command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Start a separate thread to read server responses
    response_thread = threading.Thread(target=read_responses, args=(server_process,))
    response_thread.daemon = True
    response_thread.start()

    # Send requests to the server
    try:
        # 1. Initialize request
        send_request(server_process, "initialize", {"protocolVersion": "2.0.0"}, 1)

        # 2. tools/list request
        send_request(server_process, "tools/list", {}, 2)

        # 3. tools/call request
        send_request(
            server_process,
            "tools/call",
            {"name": "hello_python", "arguments": {"name": "Test User"}},
            3,
        )

        # 4. Initialized notification
        send_request(server_process, "notifications/initialized", {}, 4)

    finally:
        # Wait for the server process to terminate
        server_process.stdin.close()
        server_process.wait(timeout=5)
        response_thread.join(timeout=2)

    print("\nTest complete.", file=sys.stderr)
