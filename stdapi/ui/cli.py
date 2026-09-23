import sys
import asyncio
import argparse
from ..extractors.registry import find_extractor
from ..core.ffmpeg import FFmpegPipeline
from ..mcp.server import run_stdio_mcp_server
from .tui import show_diagnostics

try:
    from rich.console import Console
    from rich.table import Table
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False


def main():
    parser = argparse.ArgumentParser(
        prog="stdapi",
        description="StdAPI 2.0 — Universal media engine, FFmpeg pipeline, and MCP server."
    )
    subparsers = parser.add_subparsers(dest="command", help="Subcommand to run")

    # extract command
    p_extract = subparsers.add_parser("extract", help="Extract direct high-res stream from any URL")
    p_extract.add_argument("url", help="Media URL (Instagram, YouTube, TikTok, Twitter, Pinterest)")

    # convert command
    p_convert = subparsers.add_parser("convert", help="Convert media file to 320kbps MP3")
    p_convert.add_argument("input", help="Input file path")
    p_convert.add_argument("output", help="Output file path")

    # agent command
    p_agent = subparsers.add_parser("agent", help="Execute autonomous agent mission on laptop")
    p_agent.add_argument("mission", help="Task for STD AI (e.g. 'dishabot bana ek chatbot', 'insta open kar')")

    # hud command
    subparsers.add_parser("hud", help="Launch native Cyber Virtual Desktop HUD window")

    # clean command
    subparsers.add_parser("clean", help="Scan and clean temporary junk cache files")

    # mcp command
    subparsers.add_parser("mcp", help="Start MCP server for Claude Desktop / Cursor IDE")

    # tui command
    subparsers.add_parser("tui", help="Show interactive engine status & diagnostics")

    args = parser.parse_args()

    if not args.command or args.command == "tui":
        show_diagnostics()
        sys.exit(0)


    if args.command == "mcp":
        asyncio.run(run_stdio_mcp_server())

    elif args.command == "extract":
        async def do_extract():
            ext = find_extractor(args.url)
            if not ext:
                print(f"[Error] No matching extractor found for {args.url}")
                return
            res = await ext.extract(args.url)

            if HAS_RICH:
                table = Table(title=f"[bold green]✓ Extracted: {res.extractor}[/bold green]", border_style="green")
                table.add_column("Property", style="cyan")
                table.add_column("Value", style="white")

                table.add_row("Title", res.title)
                table.add_row("Author", res.author or "Unknown")
                table.add_row("Duration", f"{res.duration}s" if res.duration else "N/A")
                table.add_row("Direct Stream", res.best_video_url or "N/A")
                console.print(table)
            else:
                print(f"\n✓ Extracted: {res.extractor}")
                print(f"  Title:         {res.title}")
                print(f"  Author:        {res.author or 'Unknown'}")
                print(f"  Duration:      {res.duration or 'N/A'}")
                print(f"  Direct Stream: {res.best_video_url or 'N/A'}\n")

        asyncio.run(do_extract())

    elif args.command == "agent":
        from ..agent import StdAgent
        agent = StdAgent()
        agent.run(args.mission)

    elif args.command == "hud":
        from ..agent import StdAgent
        agent = StdAgent()
        agent.launch_hud()

    elif args.command == "clean":
        import shutil
        from pathlib import Path
        import os
        temp_dir = Path(os.environ.get("TEMP", Path.home() / "AppData/Local/Temp"))
        cleaned_mb = 0
        if temp_dir.exists():
            for item in temp_dir.iterdir():
                try:
                    if item.is_file() or item.is_symlink():
                        sz = item.stat().st_size
                        item.unlink(missing_ok=True)
                        cleaned_mb += sz / (1024 * 1024)
                    elif item.is_dir():
                        shutil.rmtree(item, ignore_errors=True)
                except Exception:
                    pass
        print(f"[+] System Junk Purged: {round(cleaned_mb, 1)} MB temp cache cleared.")


if __name__ == "__main__":
    main()

