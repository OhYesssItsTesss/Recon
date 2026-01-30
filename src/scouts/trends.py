from pytrends.request import TrendReq
import pandas as pd
from typing import Dict, List
import time

class TrendScout:
    def __init__(self):
        # hl='en-US', tz=360 matches US/English settings
        # Removing custom retry logic to avoid urllib3 deprecation issues
        self.pytrends = TrendReq(hl='en-US', tz=360)

    def analyze(self, topic: str) -> Dict:
        """
        Fetch 'Interest Over Time' and 'Related Queries' for a topic.
        """
        print(f"[*] TrendScout: Analyzing '{topic}'...")
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
