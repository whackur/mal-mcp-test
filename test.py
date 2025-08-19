import json
import sys
import subprocess
import threading

# 표준 입출력 인코딩을 UTF-8로 강제합니다.
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')

def send_request(process, method, params, request_id):
    """지정된 프로세스에 JSON-RPC 요청을 보냅니다."""
    request = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method,
        "params": params
    }
    message = json.dumps(request, ensure_ascii=False) + '\n'
    process.stdin.write(message.encode('utf-8'))
    process.stdin.flush()
    print(f"클라이언트 -> 서버: {message.strip()}", file=sys.stderr)

def read_responses(process):
    """서버로부터의 응답을 읽고 출력합니다."""
    for line in iter(process.stdout.readline, b''):
        print(f"서버 -> 클라이언트: {line.decode('utf-8').strip()}", file=sys.stderr)
    
    for line in iter(process.stderr.readline, b''):
        print(f"서버 (stderr): {line.decode('utf-8').strip()}", file=sys.stderr)


if __name__ == "__main__":
    # MCP 서버 프로세스를 시작합니다.
    server_command = [sys.executable, 'python_hello_server/server.py']
    server_process = subprocess.Popen(
        server_command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # 서버 응답을 읽기 위한 별도의 스레드를 시작합니다.
    response_thread = threading.Thread(target=read_responses, args=(server_process,))
    response_thread.daemon = True
    response_thread.start()

    # 서버에 요청을 보냅니다.
    try:
        # 1. Initialize 요청
        send_request(server_process, "initialize", {"protocolVersion": "2.0.0"}, 1)
        
        # 2. tools/list 요청
        send_request(server_process, "tools/list", {}, 2)

        # 3. tools/call 요청
        send_request(
            server_process,
            "tools/call",
            {
                "name": "hello_python",
                "arguments": {"name": "테스트 사용자"}
            },
            3
        )
        
        # 4. 초기화 완료 알림
        send_request(server_process, "notifications/initialized", {}, 4)

    finally:
        # 서버 프로세스가 종료될 때까지 잠시 기다립니다.
        server_process.stdin.close()
        server_process.wait(timeout=5)
        response_thread.join(timeout=2)

    print("\n테스트 완료.", file=sys.stderr)
