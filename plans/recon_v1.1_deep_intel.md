# Implementation Plan - Recon v1.1 (Deep Intelligence Update)

## 1. 🔍 Analysis & Context
*   **Objective:** Upgrade Recon's intelligence engine to provide deeper, more nuanced analysis. Specifically:
    1.  **Competitor Recon:** Identify existing players (Successes & Failures).
    2.  **Balanced Analysis:** Separate "Pain Points" from "Pros/Cons" to avoid conflation.
    3.  **Accuracy:** Improve source relevance.
*   **Affected Files:**
    *   `Dev/Recon/src/strategist.py` (Prompt Engineering)
    *   `Dev/Recon/src/scouts/web.py` (New Scout methods for Competitors)
    *   `Dev/Recon/web/api/lib/strategist.py` (Sync web version)
    *   `Dev/Recon/src/cli.py` (UI Updates)
*   **Key Dependencies:**
    *   `duckduckgo-search` (Already installed).
    *   `Gemini 2.0 Flash` (Already integrated).
*   **Risks/Unknowns:**
    *   **Token Limits:** Adding detailed competitor analysis might hit context window limits if we aren't careful with truncation.
    *   **Search Noise:** Searching for "Competitors" often yields generic "Top 10" listicles. We need to filter for specific product names.

## 2. 📋 Checklist
- [ ] **Step 1: Competitor Scout:** Add `search_competitors(topic)` to WebScout.
- [ ] **Step 2: Prompt Upgrade:** Update `Strategist` to ask for "Competitor Landscape" and split "Pain" from "Pros/Cons".
- [ ] **Step 3: CLI Update:** Add new tables for Competitors and Pros/Cons.
- [ ] **Step 4: Web UI Update:** Sync the frontend to display the new data.

## 3. 📝 Step-by-Step Implementation Details

### Step 1: The Competitor Scout
*   **Goal:** Find who is already doing it.
*   **Action:**
    *   Modify `src/scouts/web.py`:
        *   Add `search_competitors(topic)` method.
        *   Query: `"{topic}" alternative vs`, `"{topic}" competitors`, `"{topic}" pricing`.
        *   Return: List of `{name, url, snippet}`.

### Step 2: The Strategist Upgrade (The Brain)
*   **Goal:** Force the AI to think deeper.
*   **Action:**
    *   Update `src/strategist.py`:
        *   **New JSON Schema:**
            ```json
            {
                "verdict": "...",
                "competitor_landscape": [
                    {"name": "Name", "status": "Active/Dead", "gap": "What they miss"}
                ],
                "swot_analysis": {
                    "strengths": [],
                    "weaknesses": [],
                    "opportunities": [],
                    "threats": []
                },
                "visceral_pain_points": ["Specific User Quote 1", ...]
            }
            ```
        *   **Prompt Tweak:** "Do not conflate 'Features' with 'Pain'. Pain is emotional. Features are functional."

### Step 3: UI Enhancement
*   **Goal:** Display the data cleanly.
*   **Action:**
    *   Update `cli.py`: Add `Table(title="Competitor Landscape")`.
    *   Update `page.tsx` (Web): Add a "Competitors" card and a "SWOT" grid.

## 4. 🧪 Testing Strategy
*   **Test Case:** "Notion Clone".
    *   *Expectation:* Should list Notion, Obsidian, Tana. Should identify "Complexity" as a pain point.
*   **Negative Case:** "Sandpaper Underwear".
    *   *Expectation:* Competitors: None (or joke items). Threats: Injury.

## 5. ✅ Success Criteria
1.  Report lists at least 3 real competitors.
2.  Pain points are distinct from "Cons" (e.g., "Expensive" is a Con, "I feel ripped off" is Pain).
3.  Web UI displays the new data sections.
