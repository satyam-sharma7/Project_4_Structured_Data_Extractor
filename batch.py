from pathlib import Path
from loader import content_type
from router import route_and_extract
from rich.console import Console
import json 

def batch_process(path: str):
    files = list(path.iterdir())
    print(f"Found {len(files)} files\n")

    success, failed = 0, 0

    for file in files:
        try:
            file_path = file.absolute()
            format, file_content = content_type(file_path)
            Console().print(f"\n[green]Your {format} is being extracted...[/]")
            extracted = route_and_extract(format, file_content)

            record = {
                "file": file.name,
                "doc_type": format,
                "extracted": extracted
            }

            with open(f"saved_json/{format}.jsonl", 'a', encoding='utf-8') as f:
                f.write(json.dumps(record)+"\n")

            print(f"✅ {file.name} → {format}")
            success += 1

        except Exception as e:
            print(f"❌ Failed: {file.name} — {e}")
            failed +=1

    print(f"\n===== Summary =====")
    print(f"Success: {success}")
    print(f"Failed:  {failed}")

