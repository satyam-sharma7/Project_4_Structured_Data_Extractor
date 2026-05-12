from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from pathlib import Path
import json

from loader import content_type
from router import route_and_extract
from batch import batch_process
from evaluation import score

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
            extracted, schema = route_and_extract(format, content)

            eval_score, reason = score(extracted, schema, content)
            
            record = {
                "file": path.name,
                "doc_type": format,
                "status": "pass" if eval_score >=0.75 else "fail",
                "score": eval_score,
                "reason": reason,
                "extracted": extracted
            }

            if eval_score >= 0.75:
                with open(f"saved_json/{format}.jsonl", 'a', encoding='utf-8') as f:
                    f.write(json.dumps(record)+"\n")

                print(f"✅ {path.name} → {format}")

            elif eval_score < 0.75:
                with open("review_queue.jsonl", 'a', encoding='utf-8') as f:
                    f.write(json.dumps(record)+"\n")

                print(f"{path.name} fails the critria.\nevaluation marks was {eval_score}")

        except Exception as e:
            print(f"❌ Failed: {path.name} — {e}")

    elif path.is_dir():
        batch_process(path)

if __name__ == "__main__":
    main()
