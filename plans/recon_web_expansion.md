# Implementation Plan - Recon Web (Vercel App) & Marketing Expansion

## 1. 🔍 Analysis & Context
*   **Objective:** 
    1.  **Build Recon Web:** A lightweight, Vercel-deployable Web UI for Recon to capture emails ("Lead Magnet") and lower the barrier to entry.
    2.  **Expand Marketing:** Create a deeper, story-driven article and 3 distinct LinkedIn posts with varied CTAs (Download, Read, Hire Me).
*   **Affected Files:**
    *   `Dev/Recon/web/` (New Directory for Next.js App)
    *   `Dev/Recon/api/` (Python Serverless Function for Vercel)
    *   `Business/Vega/Marketing/social_posts/recon_launch/` (Update existing, add new)
*   **Key Dependencies:**
    *   **Web:** Next.js (React), Tailwind CSS, Lucide Icons.
    *   **Backend:** Vercel Python Runtime (to reuse `src/scouts` and `src/strategist`).
    *   **Email:** Supabase (easiest) or simple Google Sheets integration for email capture.
*   **Risks/Unknowns:**
    *   **Vercel Python Limits:** Vercel serverless functions have a 10s timeout (Free tier) or 60s (Pro). Recon scans take ~15-30s.
    *   **Mitigation:** We must use **Streaming** response or a "Job Queue" pattern (Overkill). *Better mitigation:* Optimize the Python script to be faster or split the request (Trend first, then Reddit). Or simply accept that the Free Web version is "Lite" (fewer sources).

## 2. 📋 Checklist
- [ ] **Step 1: Marketing Content Expansion:** Rewrite the article (Story mode) and generate 3 Post variants.
- [ ] **Step 2: Web App Scaffolding:** Create `Dev/Recon/web` (Next.js) + `api` (Python).
- [ ] **Step 3: Port Logic to Serverless:** Adapt `cli.py` logic into a FastAPI/Flask route for Vercel.
- [ ] **Step 4: Email Capture UI:** Add a simple "Enter Email to Unlock Full Report" gate.
- [ ] **Step 5: Verification:** Test the Vercel build locally.

## 3. 📝 Step-by-Step Implementation Details

### Step 1: Content Expansion (The Story)
*   **Goal:** Make the content "sticky."
*   **Action:**
    *   Update `linkedin_article_deep_dive.md`: Add a narrative arc ("The Friday Night Spark," "The Saturday Morning Regret," "The Solution").
    *   Create `linkedin_post_hire_me.md`: CTA = "I build systems like this for clients."
    *   Create `linkedin_post_download.md`: CTA = "Get the tool."
    *   Create `linkedin_post_story.md`: CTA = "Read the article."

### Step 2: Recon Web (The Lead Magnet)
*   **Goal:** A URL users can click.
*   **Action:**
    *   Initialize Next.js app in `Dev/Recon/web`.
    *   Create `api/analyze.py`: A Vercel Serverless Function that imports `src.scouts` and `src.strategist`.
    *   **Constraint:** Since Vercel Python is tricky with scraping (headless browsers often fail), we rely heavily on the *API-based* scouts we just built (Reddit .json, HN API, Pytrends).
    *   **UI:** A clean, dark-mode input box: "Validate My Idea." -> Spinner -> Results.

### Step 3: The "Lite" Logic
*   **Goal:** Ensure it runs within Vercel's limits.
*   **Action:**
    *   Web version defaults to `depth=3` (Fast).
    *   Web version caches results (if possible) or uses `asyncio` to run scouts in parallel (Python `asyncio.gather`).

## 4. 🧪 Testing Strategy
*   **Marketing:** Review drafts against the "Cynical Engineer" persona.
*   **Web:** Run `vercel dev` locally to test Python/Next.js interop.

## 5. ✅ Success Criteria
1.  Three distinct LinkedIn posts.
2.  One rich, narrative-driven Article.
3.  A working `Dev/Recon/web` folder ready to deploy to Vercel.
