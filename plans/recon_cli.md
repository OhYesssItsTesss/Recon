# Implementation Plan - "Recon" (Market Intelligence CLI) V3 - Public Intel

## 1. 🔍 Analysis & Context
*   **Objective:** Implement "Recon" with a `Search + Scrape` architecture to bypass Reddit's restricted API. The tool will aggregate "Demand" (Google Trends) and "Pain" (Reddit discussions found via Google Search).
*   **Affected Directory:** `Dev/Recon`
*   **Key Dependencies:**
    *   `googlesearch-python` (To find the discussions).
    *   `beautifulsoup4` + `requests` (To read the discussions).
    *   `pytrends` (Google Trends data).
    *   `google-genai` (Synthesis).
*   **Risks/Unknowns:**
    *   **Scraping Blocks:** Reddit blocks generic User-Agents. We must use a browser-like User-Agent string.
    *   **Google Search Limits:** `googlesearch-python` can be rate-limited if abused. We will limit to 5-10 results per scan.

## 2. 📋 Checklist
- [ ] **Step 1: Dependency Update:** Swap `praw` for `googlesearch-python` & `bs4`.
- [ ] **Step 2: Trends Scout:** Implement `src/scouts/trends.py`.
- [ ] **Step 3: Web Scout:** Implement `src/scouts/web.py` (Generic scraper for Reddit threads).
- [ ] **Step 4: The Strategist:** Implement `src/strategist.py` (Gemini Analysis).
- [ ] **Step 5: Integration:** Wire into `src/cli.py`.

## 3. 📝 Step-by-Step Implementation Details

### Step 1: Dependency Update
*   **Goal:** Ensure we have the right tools.
*   **Action:**
    *   Update `Dev/Recon/requirements.txt`:
        ```text
        typer[all]
        rich
        google-genai
        python-dotenv
        googlesearch-python
        beautifulsoup4
        requests
        pytrends
        pandas
        fake-useragent
        ```

### Step 2: The Trends Scout (Quantitative)
*   **Goal:** Measure Search Volume.
*   **Action:**
    *   Create `Dev/Recon/src/scouts/trends.py`.
    *   Class `TrendScout`:
        *   `analyze(keywords: list)`: Returns Dictionary with "Trajectory" (Rising/Falling) and "Related Queries".
        *   *Note:* Use `pytrends.build_payload(kw_list=[keyword])`.

### Step 3: The Web Scout (Qualitative)
*   **Goal:** Find and extract human conversations.
*   **Action:**
    *   Create `Dev/Recon/src/scouts/web.py`.
    *   Class `WebScout`:
        *   `search_reddit(topic, limit=5)`:
            *   Query: `site:reddit.com "{topic}" pain point OR struggle OR hate`
            *   Returns: List of URLs.
        *   `extract_text(url)`:
            *   Uses `requests` with a fake User-Agent.
            *   Uses `bs4` to strip HTML and get readable text (titles + comments).
            *   *Fallback:* If scraping fails, return the URL title/snippet from search results.

### Step 4: The Strategist (Synthesis)
*   **Goal:** The "CMO" Brain.
*   **Action:**
    *   Create `Dev/Recon/src/strategist.py`.
    *   Use `Gemini 2.0 Flash`.
    *   Method `generate_report(topic, trend_data, discussions)`:
        *   Prompt: "You are a Market Researcher. Analyze these reddit discussions and trend data..."
        *   Return JSON: `{verdict, pain_points, opportunity_score}`.

### Step 5: Integration
*   **Action:** Update `Dev/Recon/src/cli.py` to orchestrate the flow.

## 4. 🧪 Testing Strategy
*   **Unit Tests:** Test `extract_text` on a sample HTML string.
*   **Manual Verification:** Run `python -m src.cli analyze "Meal Prep" --json` and ensure it finds Reddit threads without an API key.

## 5. ✅ Success Criteria
1.  Tool runs without `praw` errors.
2.  Returns real Reddit content (via Google Search).
3.  Returns Google Trends trajectory.
