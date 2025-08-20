# MCP TEST

# Virtual Environment

1. create venv

```shell
python -m venv .venv
```

2. activate venv

**powershell**

```powershell
.venv\Scripts\Activate.ps1
```

**cmd**
```shell
.venv\Scripts\Activate.bat
```

**bash**
```shell
.venv\Scripts\activate
```

# MCP Setting
```
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
    }
  }
}

```