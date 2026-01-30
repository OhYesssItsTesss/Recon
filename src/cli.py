import argparse
import json
import os
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from dotenv import load_dotenv

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.scouts.trends import TrendScout
from src.scouts.web import WebScout
from src.strategist import Strategist

load_dotenv()
console = Console()

def main():
    parser = argparse.ArgumentParser(description="Recon: Market Intelligence for Developers")
    parser.add_argument("command", choices=["analyze"], help="Command to run")
    parser.add_argument("topic", help="Market topic to analyze")
    parser.add_argument("--json", action="store_true", help="Output raw JSON for agents")
    parser.add_argument("--depth", type=int, default=5, help="Depth of search")
    parser.add_argument("--provider", default="gemini", choices=["gemini", "openai"], help="AI Provider")

    args = parser.parse_args()

    if args.command == "analyze":
        analyze(args.topic, args.json, args.depth, args.provider)

def analyze(topic, json_mode, depth, provider):
    # Check for keys before starting
    import keyring
    from setup_keys import setup as run_setup
    
    if not keyring.get_password("ReconCLI", f"{provider.upper()}_API_KEY") and not os.getenv(f"{provider.upper()}_API_KEY"):
        if not json_mode:
            console.print(f"[yellow]No API Key found for {provider}. Starting first-run setup...[/yellow]")
            run_setup()
        else:
            print(json.dumps({"error": "Missing API Key. Run setup first."}))
            return

    if not json_mode:
        console.print(f"[bold cyan]🔍 Recon Initialized[/bold cyan]")
        console.print(f"Target: [yellow]{topic}[/yellow] | Depth: {depth}")

    # 1. Initialize Agents
    trend_scout = TrendScout()
    web_scout = WebScout()
    strategist = Strategist(provider=provider)

    # 2. Gather Intelligence
    if not json_mode:
        with console.status("[bold green]Scouting Google Trends...[/bold green]"):
            trend_data = trend_scout.analyze(topic)
        
        with console.status("[bold green]Scouting Reddit (via DuckDuckGo)...[/bold green]"):
            discussions = web_scout.search_reddit(topic, limit=depth)
    else:
        trend_data = trend_scout.analyze(topic)
        discussions = web_scout.search_reddit(topic, limit=depth)

    # 3. Strategize
    if not json_mode:
        with console.status("[bold purple]Strategist is thinking...[/bold purple]"):
            report = strategist.generate_report(topic, trend_data, discussions)
    else:
        report = strategist.generate_report(topic, trend_data, discussions)

    if not report or "error" in report:
        if not json_mode:
            console.print(f"[bold red]Analysis Failed:[/bold red] {report.get('error', 'Unknown Error')}")
        else:
            print(json.dumps(report))
        return

    # 4. Output
    if json_mode:
        full_result = {
            "topic": topic,
            "trends": trend_data,
            "discussion_count": len(discussions),
            "analysis": report
        }
        print(json.dumps(full_result, indent=2))
    else:
        verdict = report.get('verdict', 'UNKNOWN')
        score = report.get('opportunity_score', 0)
        summary = report.get('one_line_summary', 'No summary available.')
        
        console.print("\n[bold]📊 MARKET REPORT[/bold]")
        console.print(f"Verdict: [{getColor(verdict)}]{verdict}[/{getColor(verdict)}] ({score}/100)")
        console.print(f"Summary: {summary}\n")

        table = Table(title="Top Pain Points")
        table.add_column("Pain Point", style="red")
        for point in report.get('top_pain_points', []):
            table.add_row(point)
        console.print(table)
        
        # Sources Table
        if discussions:
            sources_table = Table(title="Sources Researched", border_style="dim")
            sources_table.add_column("Source", style="cyan")
            sources_table.add_column("Link", style="blue")
            for d in discussions[:3]: # Show top 3
                sources_table.add_row(d.get('title')[:50] + "...", d.get('url'))
            console.print(sources_table)

        console.print(f"\n[bold]Recommended Angle:[/bold] {report.get('recommended_angle')}")
        
        # Marketing Playbook Panel
        playbook = report.get('marketing_playbook', {})
        playbook_text = f"""
[bold blue]Traditional:[/bold blue] {playbook.get('traditional', 'N/A')}

[bold magenta]Viral / Social:[/bold magenta] {playbook.get('viral', 'N/A')}

[bold green]Guerrilla:[/bold green] {playbook.get('guerrilla', 'N/A')}
        """
        console.print(Panel(playbook_text, title="Marketing Playbook", border_style="cyan"))

        console.print(f"\n[dim]Data Sources: Google Trends ({trend_data.get('trajectory')}) + {len(discussions)} Discussions Found[/dim]")

def getColor(verdict):
    if verdict == "GO": return "green"
    if verdict == "CAUTION": return "yellow"
    return "red"

if __name__ == "__main__":

    if len(sys.argv) == 1:

        # Interactive Mode (Double-click behavior)

        console.print("[bold cyan]🛡️ Recon Interactive Mode[/bold cyan]")

        console.print("Run via command line for more options: [green]recon analyze 'topic'[/green]\n")

        

        from rich.prompt import Prompt

        topic = Prompt.ask("Enter a business idea to analyze")

        if topic:

            analyze(topic, json_mode=False, depth=5, provider="gemini")

        

        input("\nPress Enter to exit...")

    else:

        app()
