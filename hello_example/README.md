# MCP Hello sample
- raw request

# MCP Setting Code Example
```json
{
  "mcpServers": {
    "python-hello-server": {
      "command": "python",
      "args": [
        "c:/Users/......./hello_example/hello_server.py"
      ],
      "env": {}
    }
  }
}

```

# Run Script
```shell
python ./hello_example/hello_client.py
```