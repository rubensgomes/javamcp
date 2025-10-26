# Plan: Configure Claude Code to Use JavaMCP Server

## Overview
Set up the JavaMCP v0.2.0 server as a local stdio MCP server in Claude Code.

## Prerequisites Verification
1. Verify JavaMCP is installed and working
   - Check: `poetry run python -m javamcp --help`
   - Verify version 0.2.0

2. Verify config.yaml exists and is properly configured
   - Check: `cat config.yaml`
   - Should have repositories URLs and stdio mode

## Configuration Steps

### Option 1: Using Claude Code CLI (Recommended)
1. Add JavaMCP server using CLI:
   ```bash
   claude mcp add javamcp \
     --env JAVAMCP_CONFIG=/home/rubens/dev/personal/python/javamcp/config.yml \
     -- poetry run python -m javamcp --config /home/rubens/dev/personal/python/javamcp/config.yml
   ```

2. Verify server was added:
   ```bash
   claude mcp list
   ```

3. Restart Claude Code

### Option 2: Manual Configuration (More Control)
1. Create/edit `.mcp.json` in project root or `~/.claude.json` for global access

2. Add JavaMCP configuration:
   ```json
   {
     "mcpServers": {
       "javamcp": {
         "type": "stdio",
         "command": "poetry",
         "args": [
           "run",
           "python",
           "-m",
           "javamcp",
           "--config",
           "/home/rubens/dev/personal/python/javamcp/config.yml"
         ],
         "cwd": "/home/rubens/dev/personal/python/javamcp",
         "env": {
           "PYTHONPATH": "/home/rubens/dev/personal/python/javamcp/src"
         }
       }
     }
   }
   ```

3. Verify configuration:
   ```bash
   claude mcp get javamcp
   ```

4. Restart Claude Code

## Testing & Verification

1. In Claude Code, test the MCP tools are available:
   - search_methods
   - analyze_class
   - extract_apis
   - generate_guide

2. Test a sample query:
   - Ask Claude Code: "Use the search_methods tool to find methods named 'substring'"

3. Verify server logs (if logging enabled in config.yaml)

## Troubleshooting Steps

If server doesn't work:
1. Check server starts manually:
   ```bash
   poetry run python -m javamcp --config config.yml
   ```

2. Check Claude Code MCP logs:
   ```bash
   claude mcp logs javamcp
   ```

3. Verify Python environment:
   ```bash
   poetry env info
   ```

4. Verify all dependencies installed:
   ```bash
   poetry install --no-root
   ```

## Configuration Scopes

Choose appropriate scope:
- **Local** (.mcp.json in current project): Project-specific, not shared
- **User** (~/.claude.json): Available across all projects
- **Project** (.mcp.json committed to git): Team-shared configuration

## Files to Create/Modify
- `.mcp.json` (local/project scope) OR
- `~/.claude.json` (user scope)
- `config.yaml` (if not exists, copy from config.example.yaml)

## Additional Notes

### Working Directory
The `cwd` parameter in the configuration ensures the server runs from the correct directory where:
- Poetry virtual environment is located
- Configuration file can be found
- Repository cloning will occur in the correct location

### Environment Variables
The `env` section allows passing environment-specific settings:
- `JAVAMCP_CONFIG`: Path to config file (alternative to --config flag)
- `PYTHONPATH`: Ensures Python can find the javamcp module

### Server Lifecycle
- Claude Code will automatically start the MCP server when needed
- Server runs in stdio mode (standard input/output communication)
- Server will be stopped when Claude Code closes or server is removed

## Expected Behavior

Once configured, you should be able to:
1. Ask Claude Code to search for Java methods in indexed repositories
2. Request class analysis with full context including javadocs
3. Extract APIs from new Git repositories on-the-fly
4. Generate usage guides for specific Java API use cases

All 4 MCP tools will be available through natural language requests to Claude Code.
