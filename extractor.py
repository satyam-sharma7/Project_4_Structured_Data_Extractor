from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from pathlib import Path
import json

from loader import content_type
from router import route_and_extract
from batch import batch_process

console = Console()

def main():
    console.print(Panel(f"[green]Welcome to Document Extractor[/]\n[dim]Model:Gemini[dim]"), style="green")
    console.print(f"[bold]Types of document we can extract:[/]\n1. Article\n2. Email\n3. Resume\n4. Invoice\n")
    path = Path(Prompt.ask(f"Enter your file or Folder location"))

    if path.is_file():
        try:
            console.print("\n[yellow]Detecting File Formate...[/]")

            format, content = content_type(path)

            console.print(f"\n[green]Your {format} is being extracted...[/]")
            extracted = route_and_extract(format, content)


            record = {
                "file": path.name,
                "doc_type": format,
                "extracted": extracted
            }

            with open(f"saved_json/{format}.jsonl", 'a', encoding='utf-8') as f:
                f.write(json.dumps(record)+"\n")

            print(f"✅ {path.name} → {format}")

        except Exception as e:
            print(f"❌ Failed: {path.name} — {e}")

    elif path.is_dir():
        batch_process(path)


        


if __name__ == "__main__":
    main()
