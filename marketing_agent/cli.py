import argparse
import sys
import json
from .buffer import BufferClient
from .social import SocialCardGenerator

def main():
    parser = argparse.ArgumentParser(description="AIDigiTools Marketing & Buffer Social Media Agent")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # buffer-status
    subparsers.add_parser("buffer-status", help="Check Buffer integration status")

    # social-pack
    pack_parser = subparsers.add_parser("social-pack", help="Generate daily social deal cards")
    pack_parser.add_argument("--tool", default="ChatGPT Plus", help="Tool name")
    pack_parser.add_argument("--price", type=int, default=2300, help="Price in PKR")
    pack_parser.add_argument("--url", default="https://aidigitools.tech/tools/chatgpt-plus.html", help="Product URL")

    # buffer-prepare
    prep_parser = subparsers.add_parser("buffer-prepare", help="Prepare a deal post for Buffer queue")
    prep_parser.add_argument("--tool", default="ChatGPT Plus", help="Tool name")
    prep_parser.add_argument("--price", type=int, default=2300, help="Price in PKR")

    args = parser.parse_args()

    if args.command == "buffer-status":
        client = BufferClient()
        status = client.get_status()
        print(f"[MarketingAgent] Buffer Status: {status['status']} - {status['message']}")
        return 0

    elif args.command == "social-pack":
        gen = SocialCardGenerator()
        card = gen.generate_deal_card(args.tool, args.price, args.url)
        print(f"[MarketingAgent] Generated Social Deal Card for {args.tool}:")
        print("--- CAPTION ---")
        print(card["caption"])
        print("--- SPEC ---")
        print(json.dumps(card["media_spec"], indent=2))
        return 0

    elif args.command == "buffer-prepare":
        gen = SocialCardGenerator()
        card = gen.generate_deal_card(args.tool, args.price, f"https://aidigitools.tech/tools/{args.tool.lower().replace(' ', '-')}.html")
        client = BufferClient()
        prep = client.prepare_post(card["caption"])
        print(f"[MarketingAgent] Post Prepared for {len(prep['channels'])} channels ({prep['char_count']} chars).")
        return 0

if __name__ == "__main__":
    sys.exit(main() or 0)
