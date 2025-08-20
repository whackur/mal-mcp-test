import logging
import sys
from mcp.server.fastmcp import FastMCP

# Configure file-based logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="hello_lib_server.log",
    filemode="w",
    encoding="utf-8",  # Explicitly set encoding
)

# Add console (stderr) logging
console_handler = logging.StreamHandler(sys.stderr)
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

logging.info("Server script started")

try:
    # Create a FastMCP server instance
    mcp = FastMCP("python-hello-lib-server")
    logging.info("FastMCP instance created successfully")

    @mcp.tool(
        name="hello_python_lib",
        description="A tool that returns a simple greeting from the Python MCP library.",
    )
    def hello_python_lib(name: str) -> str:
        """Returns a simple greeting."""
        logging.info(f"'hello_python_lib' tool called with name={name}")
        result = f"Hello, {name}! This is a greeting from the Python MCP library."
        logging.info(f"Returning result: {result}")
        return result

    if __name__ == "__main__":
        logging.info("Server ready to run (mcp.run())")
        # Run the server via stdio
        mcp.run()
        logging.info("Server execution finished")

except Exception as e:
    logging.error(f"Exception during server initialization: {e}", exc_info=True)
    raise
