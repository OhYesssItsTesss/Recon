# LinkedIn Article: The Architecture of Recon

**Title:** How I Built a Market Intelligence Engine in 4 Hours (Python + Gemini + No API Keys)

**Subtitle:** Bypassing the "API Bureaucracy" to build a tool that actually works.

---

### The Problem
Market research is boring. Searching Reddit for "pain points" is tedious. Most "Validator" tools are just ChatGPT wrappers that say "Great idea!" to everything. I needed a tool that was **Adversarial**. I needed a tool that wanted to kill my idea.

### The Stack
I built **Recon** using a "Scout & Strategist" architecture.

**1. The Scouts (The Eyes)**
I ran into a wall immediately: Reddit killed their free API access. Most devs stop there.
Instead, I built a `WebScout` using `duckduckgo_search` and `beautifulsoup4`. It performs "dorking" queries (e.g., `site:reddit.com "meal prep" struggle`) to find organic conversations without an API key.

**2. The Trend Scout (The Pulse)**
I used `pytrends` to pull 12 months of search volume data. Context matters—is the niche growing or dying?

**3. The Strategist (The Brain)**
This is where Gemini 2.0 Flash shines. I didn't just ask it to "summarize." I gave it an **Adversarial System Prompt**:
> *"If discussions are sparse, you MUST cap the score at 50. Do not be a Yes-Man."*

### The Result
A CLI tool that gives me a 0-100 score, a "Marketing Playbook" (Viral vs. SEO strategies), and a list of sources—all in 30 seconds.

### Open Source
I believe in "Context-Driven Development." The best tools are the ones you build to solve your own problems.

I’ve open-sourced Recon. You can install it via pip or just download the `.exe` if you aren't a coder.

**[Link to GitHub Repo]**

Let me know if it roasts your startup idea. I want to see the screenshots.
