# Recon 🛡️

**The Market Intelligence CLI for Developers.**

> Stop building products nobody wants. Validate your ideas with real-world data in 30 seconds.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-green.svg)
![Status](https://img.shields.io/badge/status-stable-success.svg)

## 🧐 What is Recon?

Recon is a tool that acts as your personal Chief Marketing Officer. It searches the internet to see if people actually want your business idea.

It doesn't just guess. It **finds the pain points** (people complaining) and generates a **marketing strategy** for you.

---

## 🚀 How to Use (For Everyone)

### Option A: I just want to run it (Windows .exe)
*Best for non-coders.*

1.  **Download:** Go to the [Releases Page](https://github.com/OhYesssItsTesss/Recon/releases) and download `Recon.exe`.
2.  **Run:** Double-click `Recon.exe`.
3.  **First Time:** It will ask for your AI Key (Gemini is free). Paste it in.
4.  **Analyze:** Type `recon analyze "Your Idea"` and hit Enter.

### Option B: For Developers
*Best for coders and contributors.*

```bash
git clone https://github.com/OhYesssItsTesss/Recon.git
cd Recon
pip install -r requirements.txt
python src/cli.py analyze "Idea"
```

### Option C: For AI Agents
*Best for Gemini CLI, Claude Code, or Cursor.*

Just give your Agent the link to this repo. Recon is "Agent-Ready" out of the box.
*   **Command:** `python src/cli.py analyze "Idea" --json`
*   **Note:** You must set the `GEMINI_API_KEY` environment variable for the agent.

---

## ✨ Features

- **🚀 Trend Analysis:** Visualizes search momentum using Google Trends.
- **🗣️ Visceral Pain Discovery:** Scrapes Reddit & Hacker News to find real people complaining.
- **🧠 Adversarial AI Brain:** Uses Gemini 2.0 (or OpenAI/Anthropic) to analyze the data. It is programmed to be skeptical.
- **🛡️ Secure:** Stores your API keys in your OS Keyring (never in plain text).

## 🏗️ How to Build (For Maintainers)

If you want to create the `.exe` file yourself:

1.  Run the build script:
    ```bash
    python build_exe.py
    ```
2.  The `Recon.exe` file will appear in the `dist/` folder.
3.  Upload this file to GitHub Releases.

## 🛠️ Configuration

Recon supports multiple AI providers. You can switch between them:

```bash
python src/cli.py analyze "Idea" --provider openai
```

| Provider | Cost | Speed | Recommendation |
|----------|------|-------|----------------|
| **Gemini** | Free* | ⚡ Fast | Best for general use |
| **OpenAI** | $$ | 🐢 Slower | Best for complex reasoning |
| **Anthropic**| $$ | ⚡ Fast | Best for creative strategy |

## 📄 License

MIT