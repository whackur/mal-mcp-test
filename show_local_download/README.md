# MCP 로컬 다운로드 파일 목록 조회 예제

이 예제는 `mcp[cli]` SDK를 사용하여 사용자의 로컬 다운로드 폴더 내의 파일 목록을 조회하는 MCP 서버와 클라이언트를 구현한 것입니다. 이 MCP 도구를 호출하면, 실행 환경(Windows, macOS, Linux)에 관계없이 해당 사용자의 'Downloads' 디렉터리 안의 파일 및 폴더 목록을 반환합니다.

## 주요 파일

- `download_server.py`: `list_download_files`라는 MCP 도구를 제공하는 서버입니다. 이 도구는 호출 시 사용자의 다운로드 폴더 내용을 조회하여 반환합니다.
- `download_client.py`: `download_server.py`에 연결하여 `list_download_files` 도구를 호출하고 그 결과를 출력하는 클라이언트입니다.

## 실행 방법

가상 환경이 활성화되고 `requirements.txt`의 의존성이 설치된 상태에서 아래 명령어를 실행하여 클라이언트를 실행할 수 있습니다.

```shell
python ./show_local_download/download_client.py
```

## 동작 방식

1. `download_client.py`가 `download_server.py`를 서브프로세스로 실행합니다.
2. 클라이언트는 서버에 `list_download_files` 도구 호출을 요청합니다.
3. 서버는 `pathlib.Path.home() / "Downloads"`를 사용하여 플랫폼에 독립적인 방식으로 다운로드 폴더 경로를 찾습니다.
4. 서버는 해당 폴더의 파일 및 폴더 목록을 문자열로 만들어 클라이언트에 반환합니다.
5. 클라이언트는 서버로부터 받은 파일 목록을 콘솔에 출력합니다.
