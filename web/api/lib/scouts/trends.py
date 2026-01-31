try:
    from pytrends.request import TrendReq
    import pandas as pd
    HAS_PYTRENDS = True
except ImportError:
    HAS_PYTRENDS = False

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

import requests

from typing import Dict, List
import time

class TrendScout:
    def __init__(self):
        # hl='en-US', tz=360 matches US/English settings
        if HAS_PYTRENDS:
            # Removing custom retry logic to avoid urllib3 deprecation issues
            self.pytrends = TrendReq(hl='en-US', tz=360)
        else:
            self.pytrends = None

    def analyze(self, topic: str) -> Dict:
        """
        Fetch 'Interest Over Time' and 'Related Queries' for a topic.
        """
        if not HAS_PYTRENDS:
            # Fallback to News Volume as a proxy for Trends
            # Fallback to News Volume as a proxy for Trends
            try:
                if not BeautifulSoup:
                    pass
                
                # Manual DDG News Search
                # https://duckduckgo.com/?q={topic}&iar=news&ia=news
                
                url = "https://html.duckduckgo.com/html/"
                data = {"q": f"{topic}", "iar": "news"}
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
                
                resp = requests.post(url, data=data, headers=headers, timeout=5)
                
                rising_queries = []
                count = 0
                
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    results = soup.find_all('div', class_='result')
                    count = len(results)
                    
                    for res in results[:3]:
                        title_tag = res.find('a', class_='result__a')
                        if title_tag:
                            rising_queries.append(title_tag.get_text(strip=True)[:50])
                
                if count >= 5:
                    trajectory = "Rising (News Proxy) 📈"
                elif count > 0:
                    trajectory = "Active (News Proxy) ➡️"
                else:
                    trajectory = "Cold (News Proxy) 📉"
                    
                return {
                    "trajectory": trajectory,
                    "interest_points": [],
                    "rising_queries": rising_queries,
                    "status": "Success (News Fallback)"
                }

            except Exception as e:
                print(f"[!] Trend Fallback Error: {e}")
                pass

            return {
                "trajectory": "Unknown (Lite Mode)",
                "interest_points": [],
                "rising_queries": [],
                "status": "Skipped (Serverless Optimization)"
            }
        try:
            # Build payload
            self.pytrends.build_payload(kw_list=[topic], timeframe='today 12-m', geo='US')
            
            # 1. Interest Over Time
            interest_df = self.pytrends.interest_over_time()
            trajectory = "Insufficient Data"
            points = []
            
            if not interest_df.empty:
                # Calculate simple trajectory (Last 4 weeks vs Previous 4 weeks)
                if len(interest_df) > 8:
                    recent = interest_df[topic].iloc[-4:].mean()
                    prev = interest_df[topic].iloc[-8:-4].mean()
                    
                    if recent > prev * 1.2:
                        trajectory = "Rising 📈"
                    elif recent < prev * 0.8:
                        trajectory = "Falling 📉"
                    else:
                        trajectory = "Stable ➡️"
                
                # Sample data points for the LLM
                points = interest_df[topic].tail(12).tolist() # Last 12 weeks

            # 2. Related Queries (Rising)
            related = self.pytrends.related_queries()
            rising_queries = []
            if related and topic in related:
                rising_df = related[topic]['rising']
                if rising_df is not None:
                    rising_queries = rising_df.head(5)['query'].tolist()

            return {
                "trajectory": trajectory,
                "interest_points": points,
                "rising_queries": rising_queries,
                "status": "Success"
            }

        except Exception as e:
            print(f"[!] TrendScout Error: {e}")
            return {
                "trajectory": "Error",
                "interest_points": [],
                "rising_queries": [],
                "status": f"Failed: {str(e)}"
            }

if __name__ == "__main__":
    ts = TrendScout()
    print(ts.analyze("Meal Prep"))
