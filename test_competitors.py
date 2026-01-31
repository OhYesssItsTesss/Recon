from src.scouts.web import WebScout

if __name__ == "__main__":
    ws = WebScout()
    print("Testing Competitor Search...")
    competitors = ws.search_competitors("Notion", limit=3)
    for c in competitors:
        print(f"Found: {c['title']} ({c['url']})")
