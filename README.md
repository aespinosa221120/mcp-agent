# MCP Agent Server (`mcp-agent`)

MCP (Model Context Protocol) server repository for SE333.

This repository is dedicated to the MCP server only. The actual target application/project lives in a separate repository (`se333-demo`, including `projectAnalyzed`).

The normal workflow is:

1. Run this MCP server (`python CodeBase/main.py`).
2. Connect from the other repo/client to `http://127.0.0.1:8000/sse`.
3. Invoke MCP tools exposed here (`add`, `code_review_agent`).

## Quick Start

```bash
git clone <your-repo-url>
cd mcp-agent

python3.12 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -e .

python CodeBase/main.py
```

Server endpoint:

- `http://127.0.0.1:8000/sse`

## Technical Documentation

### Project Overview

This project exposes MCP tools over SSE transport using `FastMCP`.

Current MCP server identity:

- Server name: `se333-server`
- Entry point: `CodeBase/main.py`
- Transport: `sse`
- Client connection URL: `http://127.0.0.1:8000/sse`

### Architecture Summary

Runtime flow:

1. `FastMCP("se333-server")` initializes the server.
2. Tool functions are registered via `@mcp.tool()`.
3. `mcp.run(transport="sse")` starts the HTTP/SSE MCP service.
4. External client (from `se333-demo`) calls tools using MCP protocol messages.
5. Tool handlers return typed results or formatted text reports.


### Dependencies and Runtime Requirements

From `pyproject.toml`:

- Python: `>=3.12`
- `fastmcp>=3.1.0`
- `httpx>=0.28.1`
- `mcp[cli]>=1.26.0`

External CLI tools required by `code_review_agent`:

- `spotbugs`
- `pmd`
- `codeql`
- `checkstyle`

`TODO`: Pin and document tested versions for each external analyzer.

## Complete MCP Tool API Documentation

Source of truth: `CodeBase/main.py`

### Tool Catalog

| Tool Name | Purpose | Input Type | Return Type |
|---|---|---|---|
| `add` | Basic addition/smoke test tool | `a: int`, `b: int` | `int` |
| `code_review_agent` | Run multi-tool static analysis | `project_path: str` | `str` |

### Tool: `add`

Purpose:

- Adds two integer values.

Function signature:

```python
add(a: int, b: int) -> int
```

Inputs:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `a` | `int` | Yes | First number |
| `b` | `int` | Yes | Second number |

Output:

- Integer result of `a + b`.

Request example (MCP call):

```json
{
	"jsonrpc": "2.0",
	"id": 1,
	"method": "tools/call",
	"params": {
		"name": "add",
		"arguments": {
			"a": 5,
			"b": 7
		}
	}
}
```

Response example (shape may vary by client SDK):

```json
{
	"jsonrpc": "2.0",
	"id": 1,
	"result": {
		"content": [
			{
				"type": "text",
				"text": "12"
			}
		]
	}
}
```

Assumptions, edge cases, errors:

- Assumes integer inputs.
- Type mismatch may be rejected by MCP/tool schema validation before the function executes.
- Python integer behavior supports large values.

### Tool: `code_review_agent`

Purpose:

- Executes SpotBugs, PMD, CodeQL, and Checkstyle on a provided path and returns one combined text report.

Function signature:

```python
code_review_agent(project_path: str) -> str
```

Inputs:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `project_path` | `str` | Yes | Path to analyzed project/directory |

Output:

- A single string with analyzer sections:
	- `SPOTBUGS RESULTS:`
	- `PMD RESULTS:`
	- `CODEQL RESULTS:`
	- `CHECKSTYLE RESULTS:`
- If an exception occurs, section contains `<Tool> error: ...`.

Request example (MCP call):

```json
{
	"jsonrpc": "2.0",
	"id": 2,
	"method": "tools/call",
	"params": {
		"name": "code_review_agent",
		"arguments": {
			"project_path": "/absolute/path/to/projectAnalyzed"
		}
	}
}
```

Response example (truncated):

```json
{
	"jsonrpc": "2.0",
	"id": 2,
	"result": {
		"content": [
			{
				"type": "text",
				"text": "SPOTBUGS RESULTS:\n...\n\nPMD RESULTS:\n...\n\nCODEQL RESULTS:\n...\n\nCHECKSTYLE RESULTS:\n..."
			}
		]
	}
}
```

Analyzer command mapping:

| Analyzer | Command used in current code |
|---|---|
| SpotBugs | `spotbugs -textui <project_path>` |
| PMD | `pmd -d <project_path> -R category/java/bestpractices.xml -f text` |
| CodeQL | `codeql database analyze <project_path>` |
| Checkstyle | `checkstyle -c /google_checks.xml <project_path>` |

`TODO`: Include analyzer `stderr`, exit code, and duration in output for easier debugging.

## Installation and Configuration Guide

### Prerequisites

| Requirement | Details |
|---|---|
| OS | macOS/Linux/Windows (commands below use macOS/Linux shell syntax) |
| Python | `>=3.12` |
| Package manager | `pip` |
| Virtual environment | Recommended (`venv`) |
| External analyzers | `spotbugs`, `pmd`, `codeql`, `checkstyle` for full tool coverage |

### Setup Commands (Clone to First Successful Run)

```bash
git clone <your-repo-url>
cd mcp-agent

python3.12 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -e .

python CodeBase/main.py
```

Success criteria:

- Server process starts without import/runtime errors.
- MCP clients can connect to `http://127.0.0.1:8000/sse`.

### MCP Client Configuration Example

File: `.vscode/mcp.json`

```json
{
	"servers": {
		"se333-MCP-server": {
			"url": "http://127.0.0.1:8000/sse",
			"type": "http"
		}
	},
	"inputs": []
}
```

### Environment Variables and Configuration Options

No required custom environment variables are defined in code right now.

| Variable | Required | Why |
|---|---|---|
| `PATH` | Yes | Must include Python and optional analyzer executables |
| `JAVA_HOME` | Optional | Commonly needed by Java-based analyzers |
| `CODEQL_HOME` | Optional | May be needed depending on CodeQL installation |

`TODO`: Add explicit host/port configuration options if remote deployment is required.

### Development vs Production-Style Usage

Development:

- Run directly: `python CodeBase/main.py`.
- Localhost-only connection expected.

Production-style (recommended practices):

- Run behind process manager/container.
- Add TLS, authentication, and network restrictions.
- Add structured logging and health checks.

`TODO`: Add official deployment manifests (Docker/system service) and security baseline.

## Usage Examples

### Start server

```bash
source .venv/bin/activate
python CodeBase/main.py
```

### Validate Python dependencies

```bash
python -c "from fastmcp import FastMCP; import mcp, httpx; print('imports-ok')"
```

### Invoke `add`

- Input: `a=10`, `b=25`
- Output: `35`

### Invoke `code_review_agent`

- Input: `project_path="/path/to/se333-demo/projectAnalyzed"`
- Output: combined analyzer report text.

## Testing and Validation Instructions

Automated tests:

- `TODO`: No automated test suite is currently in this repository.

Manual validation checklist:

1. Start server with `python CodeBase/main.py`.
2. Connect client using URL `http://127.0.0.1:8000/sse`.
3. Call `add` and confirm deterministic numeric output.
4. Call `code_review_agent` with a valid path.
5. Simulate missing analyzer in `PATH` and confirm error section is returned.

## Logging and Debugging Tips

- Keep server terminal visible while invoking tools.
- Verify each analyzer exists:

```bash
which spotbugs
which pmd
which codeql
which checkstyle
```

- If report content is incomplete, run analyzer command manually with same arguments and inspect `stderr`.
- Ensure `project_path` is absolute and accessible from the server runtime user.

## Troubleshooting and FAQ Section

### Common Issues and Fixes

| Issue | Likely Cause | Resolution |
|---|---|---|
| `ModuleNotFoundError` for `fastmcp`, `mcp`, or `httpx` | Dependencies not installed in active env | Activate `.venv` and run `pip install -e .` |
| MCP client cannot connect | Server down or wrong URL/path | Start server and verify `http://127.0.0.1:8000/sse` |
| `No such file or directory` in analyzer output | Analyzer not installed/in `PATH` | Install tool and verify with `which <tool>` |
| Checkstyle config errors | `/google_checks.xml` not present | Update code to valid config path |
| CodeQL command fails on path | Database workflow not prepared | Create/analyze CodeQL database per CodeQL docs |

### FAQ

**Q: What is this repository responsible for?**
A: Only the MCP server and MCP tool definitions. The analyzed application code is in a different repository (`se333-demo`).

**Q: Where do I run the server from?**
A: Run `python CodeBase/main.py` from this repository.

**Q: What MCP endpoint should the client use?**
A: `http://127.0.0.1:8000/sse`.

**Q: Why does `code_review_agent` return partial/empty sections?**
A: Analyzer output may be going to `stderr` or analyzer prerequisites are not satisfied.

**Q: Are there production deployment docs included?**
A: Not yet.
`TODO`: Add deployment runbook and environment hardening guide.
