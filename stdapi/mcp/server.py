"""
StdAPI Model Context Protocol (MCP) Server
Allows Claude Desktop, Cursor IDE, and AI Coding Agents to use StdAPI
as native functions to inspect media, run FFmpeg operations, and fetch web search data.
"""
import sys
import json
import asyncio
from typing import Dict, Any
from ..extractors.registry import find_extractor
from ..core.ffmpeg import FFmpegPipeline

TOOLS_MANIFEST = [
    {
        "name": "extract_media",
        "description": "Extract direct stream URL, title, thumbnail, and author from Instagram, YouTube, TikTok, Twitter, or Pinterest.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "The media URL to extract"}
            },
            "required": ["url"]
        }
    },
    {
        "name": "convert_media",
        "description": "Convert video or audio file to 320kbps MP3 or trim it using FFmpeg.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "input_file": {"type": "string", "description": "Path to input file"},
                "output_file": {"type": "string", "description": "Path for output MP3"},
                "bitrate": {"type": "string", "default": "320k"}
            },
            "required": ["input_file", "output_file"]
        }
    }
]


async def handle_tool_call(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    if name == "extract_media":
        url = arguments.get("url", "")
        extractor = find_extractor(url)
        if not extractor:
            return {"error": f"No supported extractor for URL: {url}"}
        res = await extractor.extract(url)
        return res.to_dict()

    elif name == "convert_media":
        in_f = arguments["input_file"]
        out_f = arguments["output_file"]
        bitrate = arguments.get("bitrate", "320k")
        success = await FFmpegPipeline.convert_to_audio(in_f, out_f, bitrate)
        return {"success": success, "output": out_f}

    return {"error": f"Unknown tool {name}"}


async def run_stdio_mcp_server():
    """Run JSON-RPC 2.0 stdio loop for Claude / Cursor MCP integrations."""
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await asyncio.get_event_loop().connect_read_pipe(lambda: protocol, sys.stdin)

    while True:
        line = await reader.readline()
        if not line:
            break
        try:
            req = json.loads(line.decode().strip())
            req_id = req.get("id")
            method = req.get("method")

            if method == "tools/list":
                resp = {"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS_MANIFEST}}
            elif method == "tools/call":
                params = req.get("params", {})
                name = params.get("name")
                args = params.get("arguments", {})
                result = await handle_tool_call(name, args)
                resp = {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(result)}]}}
            else:
                resp = {"jsonrpc": "2.0", "id": req_id, "result": {}}

            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()
