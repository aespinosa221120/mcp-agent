import subprocess
from fastmcp import FastMCP

mcp = FastMCP("se333-server")

@mcp.tool()
def add(a: int, b: int) -> int:
 """Add two numbers"""
 return a + b

@mcp.tool()
def code_review_agent(project_path: str) -> str:
    """
    Perform full AI code review using:
    - SpotBugs
    - PMD
    - CodeQL
    - Checkstyle
    """

    report = []

    # SpotBugs
    try:
        result = subprocess.run(
            ["spotbugs", "-textui", project_path],
            capture_output=True,
            text=True
        )
        report.append("SPOTBUGS RESULTS:\n" + result.stdout)
    except Exception as e:
        report.append(f"SpotBugs error: {e}")

    # PMD
    try:
        result = subprocess.run(
            ["pmd", "-d", project_path, "-R", "category/java/bestpractices.xml", "-f", "text"],
            capture_output=True,
            text=True
        )
        report.append("PMD RESULTS:\n" + result.stdout)
    except Exception as e:
        report.append(f"PMD error: {e}")

    # CodeQL
    try:
        result = subprocess.run(
            ["codeql", "database", "analyze", project_path],
            capture_output=True,
            text=True
        )
        report.append("CODEQL RESULTS:\n" + result.stdout)
    except Exception as e:
        report.append(f"CodeQL error: {e}")

    # Checkstyle
    try:
        result = subprocess.run(
            ["checkstyle", "-c", "/google_checks.xml", project_path],
            capture_output=True,
            text=True
        )
        report.append("CHECKSTYLE RESULTS:\n" + result.stdout)
    except Exception as e:
        report.append(f"Checkstyle error: {e}")

    return "\n\n".join(report)

if __name__ == "__main__":
 # IMPORTANT: Use SSE transport so VS Code can connect via URL.
 mcp.run(transport="sse")