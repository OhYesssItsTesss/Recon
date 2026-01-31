from src.scouts.web import WebScout
from src.strategist import Strategist
import json

if __name__ == "__main__":
    print("Testing Full Flow (Scout + Strategist)...")
    ws = WebScout()
    strat = Strategist()

    topic = "Notion Clone"
    
    # 1. Scout
    competitors = ws.search_competitors(topic, limit=3)
    # Mocking other data to save time/requests if needed, but let's run minimal real ones
    discussions = ws.search_reddit(topic, limit=2) 
    trend_data = {"trajectory": "Steady", "rising_queries": ["notion vs obsidian", "notion ai pricing"]}

    # 2. Strategist
    if strat.driver:
        report = strat.generate_report(topic, trend_data, discussions, competitors)
        print("\n=== REPORT ===")
        print(json.dumps(report, indent=2))
    else:
        print("Skipping Strategist (No Driver)")
