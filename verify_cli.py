import sys
from unittest.mock import MagicMock
import json

# Mock the expensive scouts/strategist to test CLI rendering logic ONLY
sys.modules['src.scouts.trends'] = MagicMock()
sys.modules['src.scouts.web'] = MagicMock()
sys.modules['src.strategist'] = MagicMock()

from src.scouts.trends import TrendScout
from src.scouts.web import WebScout
from src.strategist import Strategist
from src.cli import analyze

# Setup mocks
mock_trend = MagicMock()
mock_trend.analyze.return_value = {"trajectory": "Global", "rising_queries": []}
TrendScout.return_value = mock_trend

mock_web = MagicMock()
mock_web.search_reddit.return_value = [{"title": "Test Thread", "url": "http://test.com", "content": "Test content"}]
mock_web.search_competitors.return_value = [{"title": "Comp 1", "url": "http://comp1.com", "content": "Comp 1 content"}]
WebScout.return_value = mock_web

mock_strat = MagicMock()
mock_strat.generate_report.return_value = {
    "verdict": "GO",
    "opportunity_score": 85,
    "one_line_summary": "Test Summary of the opportunity.",
    "top_pain_points": ["Pain 1", "Pain 2"],
    "competitor_landscape": [
        {"name": "Big Corp", "status": "Active", "gap": "Too expensive"},
        {"name": "Indie App", "status": "Dead", "gap": "No updates"}
    ],
    "swot_analysis": {
        "strengths": ["Fast", "Cheap"],
        "weaknesses": ["Ugly", "Buggy"],
        "opportunities": ["Niche market"],
        "threats": ["Google entry"]
    },
    "recommended_angle": "The fast cheap alternative.",
    "marketing_playbook": {"traditional": "Ads", "viral": "Memes", "guerrilla": "DMs"}
}
Strategist.return_value = mock_strat

# Run verify
print("Verifying CLI Output (Mocked Data)...")
try:
    # We can't easily capture rich console output in a script without more hacking,
    # but running this ensures no exceptions are raised during rendering.
    analyze("Test Topic", json_mode=False, depth=1, provider="gemini")
    print("\nCLI Render Initialized Successfully.")
except Exception as e:
    print(f"CLI Render Failed: {e}")
