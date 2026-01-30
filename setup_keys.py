import keyring
import getpass
import sys
from rich.console import Console
from rich.prompt import Prompt

console = Console()
SERVICE_NAME = "ReconCLI"

def setup():
    console.print("[bold cyan]🛡️ Recon CLI Security Setup[/bold cyan]")
    console.print("This will store your API keys in your system's secure credential manager.\n")
    
    provider = Prompt.ask("Select AI Provider", choices=["gemini", "openai", "anthropic"], default="gemini")
    
    key_name = f"{provider.upper()}_API_KEY"
    api_key = getpass.getpass(f"Enter your {provider.title()} API Key (hidden): ")
    
    if api_key:
        keyring.set_password(SERVICE_NAME, key_name, api_key)
        console.print(f"[green]✔ {provider.title()} Key saved successfully.[/green]")
    else:
        console.print("[yellow]Skipped.[/yellow]")

    console.print("\n[dim]You can run this again to update keys.[/dim]")

if __name__ == "__main__":
    setup()