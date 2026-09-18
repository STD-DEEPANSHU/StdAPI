"""
StdAPI Interactive Hacker-Style Terminal TUI
Uses Rich to render live stream inspections, download meters, and tool diagnostics.
"""
import sys
from ..extractors.registry import find_extractor, AVAILABLE_EXTRACTORS
from ..core.ffmpeg import FFmpegPipeline

try:
    from rich.console import Console
    from rich.table import Table
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False


def render_banner():
    banner = r"""
   _____ _       _     ___  ______ _____ 
  /  ___| |     | |   / _ \ | ___ \_   _|
  \ `--.| |_  __| |  / /_\ \| |_/ / | |  
   `--. \ __|/ _` |  |  _  ||  __/  | |  
  /\__/ / |_| (_| |  | | | || |    _| |_ 
  \____/ \__|\__,_|  \_| |_/\_|    \___/ 

[StdAPI 2.0] - Universal Industrial Engine & Developer Suite
"""
    if HAS_RICH:
        console.print(f"[bold cyan]{banner}[/bold cyan]")
    else:
        print(banner)


def show_diagnostics():
    render_banner()
    ffmpeg_ok = FFmpegPipeline.is_available()
    extractors_str = ", ".join([e.NAME for e in AVAILABLE_EXTRACTORS])

    if HAS_RICH:
        table = Table(title="[bold yellow]System & Engine Diagnostics[/bold yellow]", border_style="cyan")
        table.add_column("Component", style="cyan", justify="left")
        table.add_column("Status", style="green", justify="center")
        table.add_column("Capabilities", style="white")

        table.add_row("FFmpeg Core", "✓ Active" if ffmpeg_ok else "✗ Missing", "Stream Muxing, 320k MP3 Transcoding")
        table.add_row("Stealth Engine", "✓ Active", "TLS/JA3 Spoofing, Browser Cookie Extraction")
        table.add_row("MCP Server", "✓ Ready", "Claude Desktop & Cursor IDE Protocol")
        table.add_row("Active Extractors", f"✓ {len(AVAILABLE_EXTRACTORS)} Ready", extractors_str)

        console.print(table)
        console.print("\n[bold magenta]Commands:[/bold magenta]")
        console.print("  [cyan]stdapi extract <url>[/cyan]     -> Extract high-res media stream")
        console.print("  [cyan]stdapi mcp[/cyan]               -> Start Model Context Protocol server")
        console.print("  [cyan]stdapi convert <in> <out>[/cyan] -> Convert video to 320k MP3\n")
    else:
        print("=" * 60)
        print(" SYSTEM & ENGINE DIAGNOSTICS")
        print("=" * 60)
        print(f" * FFmpeg Core:       {'[ACTIVE]' if ffmpeg_ok else '[MISSING]'} (Muxing, Transcoding)")
        print(" * Stealth Engine:    [ACTIVE] (TLS Spoofing, Auto Cookies)")
        print(" * MCP Server:        [READY] (Claude Desktop & Cursor IDE)")
        print(f" * Active Extractors: [{len(AVAILABLE_EXTRACTORS)} Ready] ({extractors_str})")
        print("=" * 60)
        print("\nCommands:")
        print("  stdapi extract <url>     -> Extract high-res media stream")
        print("  stdapi mcp               -> Start Model Context Protocol server")
        print("  stdapi convert <in> <out> -> Convert video to 320k MP3\n")
