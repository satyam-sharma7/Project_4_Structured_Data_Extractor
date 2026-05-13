from pathlib import Path
from loader import content_type
from router import route_and_extract
from rich.console import Console
import json

from evaluation import score

console = Console()
def batch_process(path: str):
    files = list(path.iterdir())
    print(f"Found {len(files)} files\n")

    success, failed, flagged = 0, 0, 0

    for file in files:
        try:
            file_path = file.absolute()
            format, file_content = content_type(file_path)
            console.print(f"\n[green]Your {format} is being extracted...[/]")
            extracted, schema = route_and_extract(format, file_content)

            eval_score, reason = score(extracted, schema, file_content)
            
            record = {
                "file": file.name,
                "doc_type": format,
                "status": "pass" if eval_score >=0.75 else "fail",
                "score": eval_score,
                "reason": reason,
                "extracted": extracted
            }

            if eval_score >= 0.75:
                with open(f"saved_json/{format}.jsonl", 'a', encoding='utf-8') as f:
                    f.write(json.dumps(record)+"\n")

                print(f"✅ {file.name} → {format}")
                success += 1



            elif eval_score < 0.75:
                with open("review_queue.jsonl", 'a', encoding='utf-8') as f:
                    f.write(json.dumps(record)+"\n")

                print(f"{file.name} fails the critria.\nevaluation marks was {eval_score}")
                flagged += 1
            

        except Exception as e:
            print(f"❌ Failed: {file.name} — {e}")
            failed +=1

    print(f"\n===== Summary =====")
    print(f"Success: {success}")
    print(f"Flagged: {flagged}  ← needs review")
    print(f"Failed:  {failed}")

