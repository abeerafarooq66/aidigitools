import json

def main():
    with open('scripts/tools_catalog.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Total tools in catalog: {len(data)}")
    for i, (k, v) in enumerate(data.items(), 1):
        plans = v.get('plans', [])
        p_str = ", ".join([f"{p.get('name')}: {p.get('price_pkr')} PKR (${p.get('price_usd')})" for p in plans])
        print(f"{i:2d}. {k:<25} | {v.get('name'):<32} | {v.get('vendor'):<25} | {p_str}")

if __name__ == '__main__':
    main()
