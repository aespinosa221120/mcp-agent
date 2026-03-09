from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool

def add(a: int, b: int) -> int:
 """Add two numbers"""
 return a + b

if __name__ == "__main__":
 # IMPORTANT: Use SSE transport so VS Code can connect via URL.
 mcp.run(transport="sse")