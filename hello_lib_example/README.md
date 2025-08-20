# MCP Hello 라이브러리 예제

이 예제는 `mcp` 라이브러리(SDK)를 사용하여 MCP 서버와 클라이언트를 구현하는 방법을 보여줍니다. `hello_example`과 달리, 이 예제는 라이브러리가 제공하는 추상화된 기능을 활용하여 코드를 더 간결하게 작성합니다.

## 주요 파일

- `hello_lib_server.py`: `mcp.server.fastmcp`를 사용하여 MCP 서버를 구현합니다. `@mcp.tool` 데코레이터를 사용하여 간단하게 도구를 정의할 수 있습니다.
- `hello_lib_client.py`: `mcp.client.stdio`와 `mcp.ClientSession`을 사용하여 서버와 비동기적으로 통신하는 클라이언트입니다.

## 실행 방법

먼저 `requirements.txt`에 명시된 `mcp` 라이브러리를 설치해야 합니다.

```shell
pip install -r requirements.txt
```

가상 환경이 활성화된 상태에서 아래 명령어를 실행하여 클라이언트를 실행할 수 있습니다.

```shell
python ./hello_lib_example/hello_lib_client.py
```

## 동작 방식

1. `hello_lib_client.py`가 `stdio_client`를 사용하여 `hello_lib_server.py`를 서브프로세스로 실행하고 통신 채널을 설정합니다.
2. `ClientSession`을 통해 서버와 초기화(handshake) 과정을 거칩니다.
3. 클라이언트는 `session.list_tools()`와 `session.call_tool()` 같은 라이브러리 함수를 사용하여 서버와 상호작용합니다.
4. 서버는 `FastMCP` 인스턴스가 요청을 자동으로 처리하고, 등록된 도구 함수를 실행하여 응답합니다.

이 예제는 `mcp` 라이브러리를 사용하여 얼마나 쉽고 효율적으로 MCP 서버와 클라이언트를 개발할 수 있는지를 보여줍니다.
