import requests
from typing import List, Dict
import time

class WebScout:
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    def search_reddit(self, topic: str, limit: int = 5) -> List[Dict]:
        """
        Search Reddit directly using their .json endpoint (No API key needed).
        """
        print(f"[*] WebScout: Searching Reddit for '{topic}'...")
        # Encode topic for URL
        query = topic.replace(" ", "+")
        url = f"https://www.reddit.com/search.json?q={query}&limit={limit}&sort=relevance"
        
        results = []
        try:
            headers = {"User-Agent": self.user_agent}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                posts = data.get('data', {}).get('children', [])
                
                for post in posts:
                    pdata = post.get('data', {})
                    results.append({
                        "title": pdata.get('title'),
                        "url": f"https://reddit.com{pdata.get('permalink')}",
                        "content": pdata.get('selftext', '')[:1000] # Use the post body
                    })
            else:
                print(f"[!] Reddit direct search failed (Status {response.status_code})")
                
        except Exception as e:
            print(f"[!] Reddit Scout Error: {e}")

        # Also try Hacker News (Algolia API is very permissive)
        try:
            print(f"[*] WebScout: Searching Hacker News for '{topic}'...")
            hn_url = f"https://hn.algolia.com/api/v1/search?query={query}&tags=story&hitsPerPage=3"
            hn_resp = requests.get(hn_url, timeout=10)
            if hn_resp.status_code == 200:
                hn_data = hn_resp.json()
                for hit in hn_data.get('hits', []):
                    results.append({
                        "title": hit.get('title'),
                        "url": hit.get('url', f"https://news.ycombinator.com/item?id={hit.get('objectID')}"),
                        "content": hit.get('story_text', '')[:1000]
                    })
        except Exception as e:
            print(f"[!] HN Scout Error: {e}")

        # 3. Last Resort: DuckDuckGo News (If everything else failed)
        if not results:
            try:
                print(f"[*] WebScout: Fallback to DDG News for '{topic}'...")
                from duckduckgo_search import DDGS
                with DDGS() as ddgs:
                    news_results = list(ddgs.news(topic, max_results=3))
                    for news in news_results:
                        results.append({
                            "title": news['title'],
                            "url": news['url'],
                            "content": news['body'] or news['title']
                        })
            except Exception as e:
                print(f"[!] DDG Fallback Error: {e}")

        return results

if __name__ == "__main__":
    ws = WebScout()
    data = ws.search_reddit("Meal Prep", limit=2)
    for d in data:
        print(f"Source: {d['url']}\nTitle: {d['title']}\n")
