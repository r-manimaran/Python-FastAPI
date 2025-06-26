from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from tavily import TavilyClient
from typing import Dict, List
import os

load_dotenv()

travily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

mcp = FastMCP("web-search",host="0.0.0.0",port=8000)

@mcp.tool()
def web_search(query: str) -> List[Dict]:
    """
    Use this tool to search the web for information using the Tavily Api.

    Args:
        query (str): The query to search for.

    Returns:
        List[Dict]: A list of dictionaries containing the search results.
        Each dictionary contains the following keys:
            - title: The title of the search result.
            - url: The URL of the search result.
            - content: The content of the search result.
            - score: The relevance score of the search result.
    """
    try:
        response = travily_client.search(query)
        return response["results"]
    except Exception as e:
        return "No Result Found"

    return mcp.tavily_search(query) 
    
def main():
    mcp.run(transport="streamable-http")
    print("Hello from mcp-streamablehttp!")


if __name__ == "__main__":
    main()
