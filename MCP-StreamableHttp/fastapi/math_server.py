from mcp.server.fastmcp import FastMCP

mcp=FastMCP(name="MathServer",stateless_http=True)

@mcp.tool()
def add_two(n: int) -> int:
    """ Add two to a number """
    return n + 2