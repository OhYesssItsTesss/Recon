import os
import json
try:
    import keyring
except (ImportError, Exception):
    # Keyring might fail to import on serverless/linux environments
    keyring = None
from typing import Dict, List, Optional

# Interface for AI Drivers
class AIDriver:
    def generate(self, prompt: str) -> str:
        raise NotImplementedError

class GeminiDriver(AIDriver):
    def __init__(self, api_key: str):
        # Using the new google-genai SDK
        from google import genai
        self.client = genai.Client(api_key=api_key)

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text

class OpenAIDriver(AIDriver):
    def __init__(self, api_key: str):
        # Lazy import to avoid hard dependency
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key)

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

class Strategist:
    def __init__(self, provider: str = "gemini"):
        self.provider = provider
        self.driver: Optional[AIDriver] = None
        self._load_driver()

    def _load_driver(self):
        # 1. Try Environment (Primary for Vercel/Serverless)
        env_key_name = f"{self.provider.upper()}_API_KEY"
        api_key = os.getenv(env_key_name)
        
        print(f"[DEBUG] Provider: {self.provider}")
        print(f"[DEBUG] Searching for Env Var: {env_key_name}")
        print(f"[DEBUG] Env Var Found: {'YES' if api_key else 'NO'}")

        # 2. Try Keyring (Local Dev fallback)
        if not api_key and keyring:
            try:
                api_key = keyring.get_password("ReconCLI", env_key_name)
                if api_key:
                    print(f"[DEBUG] Key found in Keyring.")
            except Exception as e:
                print(f"[DEBUG] Keyring failed: {e}")
                pass
        
        if not api_key:
            print(f"[!] Warning: No API Key found for {self.provider}. Checked env var '{env_key_name}' and Keyring.")
            return

        try:
            if self.provider == "gemini":
                self.driver = GeminiDriver(api_key)
            elif self.provider == "openai":
                self.driver = OpenAIDriver(api_key)
            # Add Anthropic/Ollama here
        except ImportError as e:
            print(f"[!] Missing dependency for {self.provider}: {e}")

    def generate_report(self, topic: str, trend_data: Dict, discussions: List[Dict]) -> Dict:
        if not self.driver:
            return {"error": f"AI Driver ({self.provider}) not initialized. Run 'recon setup' first."}

        print(f"[*] Strategist ({self.provider}): Synthesizing intelligence for '{topic}'...")

        # Prepare context
        discussion_text = ""
        if discussions:
            for d in discussions:
                discussion_text += f"--- Thread: {d['title']} ---\n{d['content'][:800]}\n\n"
        else:
            discussion_text = "No direct Reddit threads found."

        prompt = f"""
        You are a ruthless Market Intelligence Analyst (The Strategist).
        Analyze the following data for the business idea/topic: "{topic}"

        ### PART 1: QUANTITATIVE DATA (Google Trends)
        - Trajectory: {trend_data.get('trajectory', 'Unknown')}
        - Rising Queries: {", ".join(trend_data.get('rising_queries', []))}

        ### PART 2: QUALITATIVE DATA (Reddit Discussions)
        {discussion_text}

        ### MISSION
        1. Determine if this is a viable opportunity.
        2. Identify the visceral pain points (anger/frustration).
        3. Develop a 3-Prong Marketing Strategy.

        ### ADVERSARIAL RULES
        - If 'discussions' are sparse or missing, you MUST cap the 'opportunity_score' at 50 and set verdict to 'CAUTION' or 'NO-GO'.
        - State clearly in the 'one_line_summary' if you are relying on general knowledge vs. the provided discussion data.
        - Look for evidence of 'Willingness to Pay'.

        ### OUTPUT JSON FORMAT ONLY
        {{
            "verdict": "GO" | "CAUTION" | "NO-GO",
            "opportunity_score": integer (0-100),
            "market_phase": "Rising" | "Saturated" | "Dead" | "Unknown",
            "one_line_summary": "string",
            "top_pain_points": ["string", "string", "string"],
            "recommended_angle": "string (Positioning)",
            "marketing_playbook": {{
                "traditional": "string",
                "viral": "string",
                "guerrilla": "string"
            }},
            "key_insights": [
                {{
                    "source_title": "string (Title of the source)",
                    "insight": "string (One sentence on what this source revealed)"
                }}
            ]
        }}
        """

        try:
            text = self.driver.generate(prompt).strip()
            if text.startswith("```json"):
                text = text[7:-3].strip()
            elif text.startswith("```"):
                text = text[3:-3].strip()
            
            return json.loads(text)
        except Exception as e:
            print(f"[!] Strategist Error: {e}")
            return {"error": str(e)}
