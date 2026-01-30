# Project: CMO-CLI (Chief Marketing Officer in your Terminal)

## Core Objective
A CLI tool for developers to validate business ideas, analyze market fit, and generate marketing copy using real-world data and AI analysis. It bridges the gap between "building cool tech" and "selling it."

## Architecture
- **Interface:** Python CLI (using `typer` or `click` + `rich` for UI).
- **Intelligence:** Gemini 2.0 Flash (via `google-genai` SDK).
- **Data Sources:** 
  - Reddit (via PRAW or scraping) for pain point discovery.
  - Google Trends (via `pytrends`) for demand validation.
  - Competitor Analysis (Web Scraping).

## Key Workflows
1.  **Market Recon:** `cmo analyze "Idea Name"` 
    *   Finds where people are complaining about this problem.
    *   Estimates "Pain Intensity."
2.  **Persona Builder:** `cmo profile "Target Audience"`
    *   Generates a psychographic profile of the user.
3.  **Copy Generator:** `cmo write "Landing Page"`
    *   Drafts headers and bullets that speak directly to the discovered pain points.
