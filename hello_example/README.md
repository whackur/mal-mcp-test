# MCP Hello 예제

이 예제는 MCP(Model Context Protocol)를 사용하여 Python으로 간단한 "Hello, World!" 스타일의 서버와 클라이언트를 구현한 것입니다. MCP 라이브러리(SDK)를 사용하지 않고, 표준 입출력(stdin/stdout)을 통해 직접 JSON-RPC 메시지를 주고받는 방식을 보여줍니다.

## 주요 파일

- `hello_server.py`: MCP 서버 역할을 하는 스크립트입니다. 클라이언트로부터 요청을 받아 처리하고 응답을 보냅니다.
- `hello_client.py`: MCP 클라이언트 역할을 하는 스크립트입니다. 서버에 요청을 보내고 응답을 받아 출력합니다.

## 실행 방법

가상 환경이 활성화된 상태에서 아래 명령어를 실행하여 클라이언트를 실행할 수 있습니다. 클라이언트는 내부적으로 서버를 실행하고 통신합니다.

```shell
python ./hello_example/hello_client.py
```

## 동작 방식

1. `hello_client.py`가 `hello_server.py`를 서브프로세스로 실행합니다.
2. 클라이언트는 서버의 표준 입력(stdin)으로 JSON-RPC 요청을 보냅니다.
3. 서버는 표준 출력(stdout)으로 JSON-RPC 응답을 보냅니다.
4. 클라이언트는 별도의 스레드에서 서버의 응답을 지속적으로 읽어 화면에 출력합니다.

이 예제는 MCP의 기본적인 통신 방식을 이해하는 데 도움을 줍니다.
