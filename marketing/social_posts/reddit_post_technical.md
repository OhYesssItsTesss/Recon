# Reddit Post (r/Python, r/SideProject)

**Title:** I built a CLI tool that roasts my startup ideas using Google Trends and Gemini (Open Source)

**Body:**

Hey everyone,

I kept building SaaS apps that nobody wanted. I realized I was skipping the "Validation" step because it was boring.

So I automated it.

**Recon** is a Python CLI that does the market research for you.

**How it works:**
1.  **Trend Analysis:** Uses `pytrends` to check if the keyword is rising or dying.
2.  **Reddit Scraping:** Uses `duckduckgo_search` + `bs4` to find "pain point" discussions on Reddit and Hacker News (No Reddit API keys required).
3.  **Synthesis:** Feeds the raw data into Gemini 2.0 Flash (or OpenAI/Anthropic) with an adversarial prompt to determine a "Go/No-Go" score.

**The Tech Stack:**
*   `typer` & `rich` for the CLI UI.
*   `keyring` for secure API key storage (no `.env` files).
*   `pyinstaller` to bundle it into a standalone `.exe`.

It’s not perfect, but it stopped me from building a "Sandpaper Underwear" startup yesterday (Score: 5/100).

**Repo:** [https://github.com/OhYesssItsTesss/Recon](https://github.com/OhYesssItsTesss/Recon)

Roast my code (or let the tool roast your ideas).
