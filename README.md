# Python MCP(Model Context Protocol) 테스트 프로젝트

이 저장소는 Python을 사용하여 MCP(Model Context Protocol) 서버 및 클라이언트를 구현하는 다양한 예제를 포함합니다. MCP는 AI 모델(또는 클라이언트)과 외부 도구(또는 서버) 간의 상호작용을 위한 표준화된 프로토콜입니다.

## 프로젝트 구조

```
.
├── .clinerules/         # Cline 에이전트 동작 규칙 정의
├── .venv/               # Python 가상 환경
├── hello_example/       # MCP 라이브러리 없이 순수 Python으로 구현한 예제
├── hello_lib_example/   # `mcp` 라이브러리를 사용하여 구현한 예제
├── show_local_download/ # 로컬 다운로드 폴더 파일 목록 조회 예제
├── link-scanner/        # 웹사이트의 모든 하이퍼링크를 스캔하는 예제
├── .gitignore
├── README.md            # 현재 파일
└── requirements.txt     # Python 의존성 목록
```

## 시작하기

### 1. 가상 환경 생성 및 활성화

이 프로젝트는 Python 가상 환경을 사용하여 의존성을 관리합니다.

**가상 환경 생성:**
```shell
python -m venv .venv
```

**가상 환경 활성화:**

- **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
- **Windows (CMD):**
  ```shell
  .venv\Scripts\Activate.bat
  ```
- **macOS/Linux (Bash):**
  ```shell
  source .venv/bin/activate
  ```

### 2. 의존성 설치

가상 환경이 활성화된 상태에서 필요한 Python 패키지를 설치합니다.

```shell
pip install -r requirements.txt
```

## 예제 실행

각 예제 폴더의 `README.md` 파일에서 자세한 실행 방법을 확인할 수 있습니다.

- **[Hello 예제 (라이브러리 미사용)](./hello_example/README.md)**
  - 순수 Python과 JSON-RPC를 사용하여 MCP 통신을 구현하는 방법을 보여줍니다.
- **[Hello 라이브러리 예제](./hello_lib_example/README.md)**
  - `mcp` 라이브러리를 사용하여 쉽고 간결하게 MCP 서버/클라이언트를 구현하는 방법을 보여줍니다.
- **[로컬 다운로드 파일 목록 조회 예제](./show_local_download/README.md)**
  - 사용자의 로컬 다운로드 폴더에 접근하여 파일 목록을 반환하는 실용적인 예제입니다.
- **[링크 스캐너 예제](./link-scanner/README.md)**
  - 특정 웹사이트의 모든 내부 하이퍼링크를 재귀적으로 스캔하는 예제입니다.

## MCP 서버 설정 (for Cline)

Cline과 같은 MCP 클라이언트에서 이 프로젝트의 서버들을 사용하려면, 클라이언트의 설정 파일에 아래와 같이 서버 정보를 추가해야 합니다.

**참고:** 아래 경로의 `c:/..../` 부분은 사용자의 실제 프로젝트 경로로 변경해야 합니다.

```json
{
  "mcpServers": {
    "python-hello-server": {
      "command": "c:/..../mal-mcp-test/.venv/Scripts/python.exe",
      "args": [
        "c:/..../mal-mcp-test/hello_example/hello_server.py"
      ],
      "env": {}
    },
    "python-hello-lib-server": {
      "command": "c:/..../mal-mcp-test/.venv/Scripts/python.exe",
      "args": [
        "c:/..../mal-mcp-test/hello_lib_example/hello_lib_server.py"
      ],
      "env": {}
    },
    "show-local-download": {
      "command": "c:/..../mal-mcp-test/.venv/Scripts/python.exe",
      "args": [
        "c:/..../mal-mcp-test/show_local_download/download_server.py"
      ],
      "env": {},
      "autoApprove": [
        "list_download_files"
      ]
    },
    "link-scanner": {
      "command": "c:/..../mal-mcp-test/.venv/Scripts/python.exe",
      "args": [
        "c:/..../mal-mcp-test/link-scanner/scanner_server.py"
      ],
      "env": {}
    }
  }
}
```
