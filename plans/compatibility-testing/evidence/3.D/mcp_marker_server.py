"""Minimal stdio MCP server (no SDK) for the 3.D bounded MCP attempt.

Implements just enough of MCP over newline-delimited JSON-RPC 2.0 on stdin/stdout
to be loaded by `claude --mcp-config`: initialize / notifications/initialized /
tools/list / tools/call.  It exposes ONE tool, `record_marker`, which writes the
caller-supplied text to a marker file.  A written marker file is authentic proof
that the model reached through the MCP transport and invoked the tool.

Session-local: pure stdio child of the claude lane; touches only the marker path
passed via env MCP_MARKER_PATH.  No network.
"""
import json
import os
import sys

MARKER_PATH = os.environ.get("MCP_MARKER_PATH", "mcp_marker.txt")
PROTO = "2024-11-05"

TOOLS = [
    {
        "name": "record_marker",
        "description": "Record a marker string to the run's evidence file. "
        "Call this exactly once with the text you were told to record.",
        "inputSchema": {
            "type": "object",
            "properties": {"text": {"type": "string", "description": "marker text"}},
            "required": ["text"],
        },
    }
]


def _send(obj):
    sys.stdout.write(json.dumps(obj) + "\n")
    sys.stdout.flush()


def _log(msg):
    sys.stderr.write(f"[mcp_marker] {msg}\n")
    sys.stderr.flush()


def main():
    _log(f"started; marker path={MARKER_PATH}")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
        method = req.get("method")
        rid = req.get("id")
        _log(f"recv method={method} id={rid}")
        if method == "initialize":
            _send({
                "jsonrpc": "2.0", "id": rid,
                "result": {
                    "protocolVersion": PROTO,
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "marker", "version": "1.0.0"},
                },
            })
        elif method in ("notifications/initialized", "initialized"):
            continue  # notification, no response
        elif method == "tools/list":
            _send({"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}})
        elif method == "tools/call":
            params = req.get("params") or {}
            name = params.get("name")
            args = params.get("arguments") or {}
            if name == "record_marker":
                text = str(args.get("text", ""))
                with open(MARKER_PATH, "w", encoding="utf-8") as fh:
                    fh.write(text)
                _log(f"recorded marker: {text!r}")
                _send({
                    "jsonrpc": "2.0", "id": rid,
                    "result": {"content": [{"type": "text",
                                            "text": f"recorded: {text}"}]},
                })
            else:
                _send({"jsonrpc": "2.0", "id": rid,
                       "error": {"code": -32601, "message": f"unknown tool {name}"}})
        elif rid is not None:
            _send({"jsonrpc": "2.0", "id": rid,
                   "error": {"code": -32601, "message": f"unknown method {method}"}})
    _log("stdin closed; exiting")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
