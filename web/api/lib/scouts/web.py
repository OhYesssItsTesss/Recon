import requests
from typing import List, Dict
import time

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

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

    def search_competitors(self, topic: str, limit: int = 5) -> List[Dict]:
        """
        Search for competitors using DuckDuckGo HTML (Manual Scrape).
        """
        if not BeautifulSoup:
            print("[!] Warning: beautifulsoup4 not installed. Skipping competitor scout.")
            return []

        print(f"[*] WebScout: Hunting competitors for '{topic}'...")
        results = []
        queries = [f"{topic} alternatives", f"{topic} vs", f"{topic} pricing"]
        
        headers = {
            "User-Agent": self.user_agent,
            "Referer": "https://duckduckgo.com/"
        }

        try:
            for q in queries:
                url = "https://html.duckduckgo.com/html/"
                data = {"q": q}
                
                resp = requests.post(url, data=data, headers=headers, timeout=10)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    
                    # DDG HTML result structure
                    # <div class="result"> <h2 class="result__title"> <a class="result__a" href="...">title</a> </h2> ... </div>
                    
                    search_results = soup.find_all('div', class_='result')
                    
                    for res in search_results:
                        title_tag = res.find('a', class_='result__a')
                        snippet_tag = res.find('a', class_='result__snippet')
                        
                        if title_tag and snippet_tag:
                            link = title_tag.get('href')
                            title = title_tag.get_text(strip=True)
                            snippet = snippet_tag.get_text(strip=True)
                            
                            results.append({
                                "title": title,
                                "url": link,
                                "content": snippet
                            })
                            
                        if len(results) >= limit:
                            break
                else:
                    print(f"[!] DDG Search failed: {resp.status_code}")
                
                if len(results) >= limit:
                    break
                time.sleep(1) # Be polite

        except Exception as e:
            print(f"[!] Competitor Scout Error: {e}")

        return results

if __name__ == "__main__":
    ws = WebScout()
    data = ws.search_reddit("Meal Prep", limit=2)
    for d in data:
        print(f"Source: {d['url']}\nTitle: {d['title']}\n")
