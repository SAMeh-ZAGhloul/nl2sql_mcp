#!/bin/zsh

# Colors for terminal output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "${BLUE}Starting NL2SQL MCP Dashboard...${NC}"

# Create a new tmux session
tmux new-session -d -s nl2sql

# Split the window into three panes
tmux split-window -h
tmux split-window -v

# Start SQLite MCP Server (Port 5557)
tmux send-keys -t 0 "cd $(pwd)/mcp/sqlite_server && echo '${GREEN}Starting SQLite MCP Server on port 5557...${NC}' && python3 server.py" C-m

# Start Gemini MCP Server (Port 5556)
tmux send-keys -t 1 "cd $(pwd)/mcp/gemini_server && echo '${GREEN}Starting Gemini MCP Server on port 5556...${NC}' && python3 server.py" C-m

# Wait for the MCP servers to start
sleep 3

# Start Main Flask Application (Port 5555)
tmux send-keys -t 2 "cd $(pwd)/backend && echo '${GREEN}Starting Main Application on port 5555...${NC}' && python3 app.py" C-m

# Attach to the tmux session
tmux attach-session -t nl2sql

echo "${GREEN}All services started successfully!${NC}"
echo "Main application is running at http://localhost:5555"
