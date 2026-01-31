from duckduckgo_search import DDGS
import json

print("Testing DDGS direct...")
try:
    with DDGS() as ddgs:
        print("DDGS object created. Running search...")
        results = list(ddgs.text("Notion alternatives", max_results=3))
        print(f"Results type: {type(results)}")
        print(f"Results count: {len(results)}")
        print(json.dumps(results, indent=2))
except Exception as e:
    print(f"Error: {e}")
