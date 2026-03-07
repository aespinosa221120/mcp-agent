---
tools: ["se333-server/add"]  # Update with actual MCP tools as needed
description: "Test agent that generates, executes, and refines tests automatically."
model: GPT-5.2
---

## Agent Instructions ##

1. Generate initial test cases for the code in CodeBase/
2. Execute the test cases using MCP server tools
3. Parse coverage feedback from the test results (e.g., JaCoCo XML)
4. Identify areas of low coverage and modify or add new tests
5. Repeat the cycle iteratively to maximize coverage