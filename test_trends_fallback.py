import sys
from unittest.mock import MagicMock

# Force generic ImportError for pytrends to test fallback
sys.modules['pytrends'] = None
sys.modules['pytrends.request'] = None

from web.api.lib.scouts.trends import TrendScout

if __name__ == "__main__":
    print("Testing TrendScout Fallback...")
    ts = TrendScout()
    # Should use the fallback path now
    result = ts.analyze("iPhone 16")
    print(result)
    
    if "News Proxy" in result['trajectory']:
        print("\n✅ Verification SUCCESS: Fallback to News Proxy active.")
    else:
        print("\n❌ Verification FAILED: Did not get News Proxy result.")
