#!/bin/bash
set -e

# PATH for systemd (gemini, uv, npx in ~/.local/bin and node)
export PATH="$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
export HOME="/home/shima"

# Paths
PROJECT_DIR="/home/shima/projects/agent-second-brain"
VAULT_DIR="$PROJECT_DIR/vault"
ENV_FILE="$PROJECT_DIR/.env"

# Load environment variables
if [ -f "$ENV_FILE" ]; then
    export $(grep -v '^#' "$ENV_FILE" | xargs)
fi

# Check token
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "ERROR: TELEGRAM_BOT_TOKEN not set"
    exit 1
fi

# MCP timeout for stdio server (default 5 sec is too short)
export MCP_TIMEOUT=30000
export MAX_MCP_OUTPUT_TOKENS=50000

# Date and chat_id
TODAY=$(date +%Y-%m-%d)
CHAT_ID="${ALLOWED_USER_IDS//[\[\]]/}"  # remove brackets from [123456]

echo "=== d-brain processing for $TODAY ==="

# Run Gemini from vault/ for context (reads vault/.claude/CLAUDE.md)
cd "$VAULT_DIR"
GEMINI_MODEL="${GEMINI_MODEL:-gemini-3-pro-preview}"
TODOIST_TOOL_PREFIX="${TODOIST_TOOL_PREFIX:-todoist__}"
REPORT=$(gemini --approval-mode yolo \
    --model "$GEMINI_MODEL" \
    --prompt "Today is $TODAY. Execute daily processing according to dbrain-processor skill.

CRITICAL: MCP loads in 10-30 seconds. You are NOT in subprocess — MCP IS running, just initializing.

Algorithm:
1. Call ${TODOIST_TOOL_PREFIX}find-tasks-by-date
2. Error? Wait 10 sec, read goals/, daily/ files
3. Call again
4. Error again? Wait 20 more sec
5. Third call — GUARANTEED to work

DO NOT say MCP unavailable. It is available. Just wait and call." \
    2>&1) || true
cd "$PROJECT_DIR"

echo "=== Gemini output ==="
echo "$REPORT"
echo "===================="

# Remove HTML comments (break Telegram HTML parser)
REPORT_CLEAN=$(echo "$REPORT" | sed '/<!--/,/-->/d')

# Rebuild vault graph (keeps structure up to date)
echo "=== Rebuilding vault graph ==="
cd "$VAULT_DIR"
uv run .claude/skills/graph-builder/scripts/analyze.py || echo "Graph rebuild failed (non-critical)"
cd "$PROJECT_DIR"

# Git commit
git add -A
git commit -m "chore: process daily $TODAY" || true
git push || true

# Send to Telegram
if [ -n "$REPORT_CLEAN" ] && [ -n "$CHAT_ID" ]; then
    echo "=== Sending to Telegram ==="
    RESULT=$(curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
        -d "chat_id=$CHAT_ID" \
        -d "text=$REPORT_CLEAN" \
        -d "parse_mode=HTML")

    # If HTML failed, send without formatting
    if echo "$RESULT" | grep -q '"ok":false'; then
        echo "HTML failed: $RESULT"
        curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
            -d "chat_id=$CHAT_ID" \
            -d "text=$REPORT_CLEAN"
    fi
fi

echo "=== Done ==="
