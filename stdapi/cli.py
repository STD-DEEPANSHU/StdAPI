import sys
import asyncio
import argparse
from stdapi import StdAPI

def main():
    parser = argparse.ArgumentParser(
        prog="stdapi",
        description="StdAPI CLI — Universal media downloader, AI chat, and search tool."
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # media command
    media_p = subparsers.add_parser("media", help="Extract or download media (YouTube, Insta, TikTok, etc.)")
    media_p.add_argument("url", help="Media URL")
    media_p.add_argument("-f", "--format", default="mp4", choices=["mp4", "mp3"], help="Format (mp4/mp3)")

    # ai command
    ai_p = subparsers.add_parser("ai", help="Ask AI a question")
    ai_p.add_argument("prompt", help="Prompt for AI")
    ai_p.add_argument("-m", "--model", default="gpt-4o-mini", help="AI Model (gpt-4o-mini, gemini, deepseek)")

    # search command
    search_p = subparsers.add_parser("search", help="Search the web or Wikipedia")
    search_p.add_argument("query", help="Search query")
    search_p.add_argument("--wiki", action="store_true", help="Search Wikipedia specifically")

    # tools command
    tools_p = subparsers.add_parser("tools", help="Developer utilities")
    tools_p.add_argument("--shorten", help="Shorten a URL")
    tools_p.add_argument("--lyrics", help="Get song lyrics")
    tools_p.add_argument("--qr", help="Generate QR link")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    async def run():
        async with StdAPI() as api:
            if args.command == "media":
                print(f"[*] Extracting media: {args.url}")
                res = await api.media.download(args.url, args.format)
                print(f"[✓] Title: {res.title}")
                print(f"[✓] Download URL: {res.download_url}")

            elif args.command == "ai":
                print(f"[*] Asking {args.model}...")
                res = await api.ai.chat(args.prompt, model=args.model)
                print(f"\n[AI]:\n{res.response}")

            elif args.command == "search":
                if args.wiki:
                    res = await api.search.wiki(args.query)
                    print(f"\n[Wikipedia: {res.title}]\n{res.extract}")
                else:
                    res = await api.search.web(args.query)
                    print(f"\nResults for '{args.query}':")
                    for i, r in enumerate(res.results, 1):
                        print(f"{i}. {r.title}\n   {r.url}\n   {r.snippet}\n")

            elif args.command == "tools":
                if args.shorten:
                    res = await api.tools.shorten(args.shorten)
                    print(f"Short URL: {res.short_url}")
                elif args.lyrics:
                    res = await api.tools.lyrics(args.lyrics)
                    print(f"\n[{res.title} - {res.author}]\n\n{res.lyrics}")
                elif args.qr:
                    res = await api.tools.qr(args.qr)
                    print(f"QR Code: {res.qr_image_url}")

    asyncio.run(run())

if __name__ == "__main__":
    main()
