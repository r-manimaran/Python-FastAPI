from mcp.server.fastmcp import FastMCP

mcp= FastMCP(name="EchoServer", stateless_http=True)

@mcp.tool()
def echo(message: str) -> str:
    """ Echo a message """
    return message