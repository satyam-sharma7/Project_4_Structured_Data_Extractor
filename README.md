# Structured Data Extractor

A command-line pipeline that turns unstructured text documents (articles, emails, resumes, invoices) into schema-conformant JSON using LLMs, and **scores its own output** so low-quality extractions never reach your clean dataset.

Each document goes through three LLM steps: **classify → extract → evaluate**. Results scoring `>= 0.75` are saved; the rest are routed to a review queue for a human to check.

---

## Features

- **Automatic document classification**: an LLM labels each file as `article`, `email`, `resume`, or `invoice`, so you don't specify the type
- **Type-based routing**: each document type gets its own system prompt and JSON schema
- **Schema-guided extraction**: JSON-mode output at `temperature=0.2` for consistency
- **Hallucination guard**: the prompt tells the model to return `null` for missing fields rather than guess
- **LLM-as-judge scoring**: a separate call compares the raw document, schema, and extraction, and returns a `0.0-1.0` score with a short reason
- **Quality gate**: pass/fail threshold at `0.75`; failures go to `review_queue.jsonl`
- **Single-file or batch mode**: point it at a file or a whole folder
- **Rich terminal UI** and an end-of-run summary (success / flagged / failed)

---

## How It Works

```
 file / folder
      │
      ▼
 ┌───────────┐  read file (UTF-8 text) + classify type
 │ loader    │  via OpenRouter
 └─────┬─────┘
       │ (doc_type, content)
       ▼
 ┌───────────┐  pick prompt + schema for the type,
 │ router    │  extract JSON via Gemini
 └─────┬─────┘
       │ extracted JSON
       ▼
 ┌───────────┐  LLM-as-judge: strict 0.0-1.0 score + reason
 │ evaluation│
 └─────┬─────┘
       │
  ┌────┴─────────────────────┐
  ▼                          ▼
score >= 0.75           score < 0.75
saved_json/<type>.jsonl review_queue.jsonl
```

---

## Project Structure

```
Project_4_Structured_Data_Extractor/
├── extractor.py        # CLI entry point (single file or folder)
├── loader.py           # Reads the file and classifies its document type
├── router.py           # Routes by type, builds prompts, runs extraction
├── evaluation.py       # LLM-as-judge scoring of each extraction
├── batch.py            # Folder processing with pass/flag/fail summary
├── json_schemas/       # Target JSON schemas per document type
├── schemas/            # Schema definitions
├── samples/            # Sample input documents
├── saved_json/         # Accepted extractions, one .jsonl per doc type
├── requirements.txt
└── .gitignore
```

---

## Setup

**1. Clone**

```bash
git clone https://github.com/satyam-sharma7/Project_4_Structured_Data_Extractor.git
cd Project_4_Structured_Data_Extractor
```

**2. Install dependencies**

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt python-dotenv rich
```

> `python-dotenv` and `rich` are imported by the code but are not yet listed in `requirements.txt`, so they are installed explicitly here.

**3. Configure environment variables**

Two providers are used: OpenRouter for classification, and Google AI Studio (Gemini via its OpenAI-compatible endpoint) for extraction and evaluation. Create a `.env` file in the project root:

```env
# Classification (loader.py)
OPENROUTER_URL=https://openrouter.ai/api/v1
OPENROUTER_API_KEY_2=your_openrouter_api_key

# Extraction + evaluation (router.py, evaluation.py)
GOOGLE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
GOOGLE_AI_STUDIO=your_google_ai_studio_api_key
GOOGLE_MODEL=your_gemini_model_name
```

> Never commit `.env`. Make sure it is listed in `.gitignore`.

---

## Usage

```bash
python extractor.py
```

You will be prompted for a path:

```
Enter your file or Folder location: samples/invoice_01.txt
```

- **File path**: processes that single document
- **Folder path**: processes every file in the folder and prints a summary

### Input requirements

Files are read as UTF-8 plain text. PDFs, Word documents, and images are not supported yet (see Roadmap).

### Supported document types

| Type | Schema key |
| --- | --- |
| Article | `ArticleExtract` |
| Email | `EmailExtract` |
| Resume | `ResumeExtract` |
| Invoice | currently `EmailExtract` (see Known Issues) |

---

## Output Format

Every processed document produces a record like this:

```json
{
  "file": "invoice_01.txt",
  "doc_type": "invoice",
  "status": "pass",
  "score": 0.92,
  "reason": "All fields correctly extracted; no hallucinated values.",
  "extracted": { "...": "..." }
}
```

| Outcome | Condition | Destination |
| --- | --- | --- |
| Pass | `score >= 0.75` | `saved_json/<doc_type>.jsonl` |
| Fail | `score < 0.75` | `review_queue.jsonl` |
| Error | exception during processing | printed to console, counted as failed |

### Scoring rubric

The judge model is told to be strict and to penalize missing fields, hallucinated values, and wrong data types:

| Score | Meaning |
| --- | --- |
| 1.0 | Perfect: all fields correct |
| ~0.7 | Mostly correct: 1-2 minor errors or missing fields |
| ~0.5 | Partial: several missing or wrong fields |
| 0.0 | Completely wrong or empty |

---

## Design Decisions

- **Self-evaluation over blind trust.** LLM extraction fails quietly. A separate scoring pass makes failures visible and keeps `saved_json/` clean.
- **Human-in-the-loop for the long tail.** Low-scoring items are queued rather than discarded or silently accepted.
- **Explicit `null` for missing data.** Reduces fabricated values compared to letting the model fill gaps.
- **Separate models per stage.** Classification is a cheap, low-stakes call (a free OpenRouter model); extraction and grading use Gemini.
- **OpenAI-compatible clients.** Both providers are called through the OpenAI SDK, so swapping models is mostly a config change.

---

## Known Issues / Roadmap

- [ ] **Invoice routing uses the email schema.** In `router.py` the `invoice` branch loads `all_schema["EmailExtract"]`; it needs its own invoice schema.
- [ ] **Unvalidated classifier output.** `loader.py` defines Pydantic models (`ContentCategory`, `FileClassifier`) but never uses them. If the model returns a label outside the four types, `route_and_extract` falls into its `else` branch and crashes on an undefined `extracted`.
- [ ] **Classifier model is hardcoded** to a free OpenRouter model; move it to `.env`.
- [ ] **`requirements.txt` is incomplete**: add `python-dotenv` and `rich`.
- [ ] **Text files only.** Add PDF/DOCX parsing so real invoices and resumes work.
- [ ] **Batch mode reads every entry in the folder**, including subfolders and non-text files, which show up as failures.
- [ ] `review_queue.jsonl` is written to the project root, not `saved_json/`.
- [ ] No retry or rate-limit handling around API calls (3 calls per document).
- [ ] Extractions are not validated against the schema in code; quality relies on the LLM judge only.
- [ ] Add tests and a small benchmark with accuracy numbers per document type.
- [ ] Add a non-interactive CLI (`--path`, `--threshold`) for scripting.

---

## Tech Stack

- Python
- OpenAI SDK (`openai==2.33.0`) pointed at OpenRouter and Google's OpenAI-compatible Gemini endpoint
- Pydantic (`pydantic==2.12.5`)
- `python-dotenv`, `rich`

---

## Author

**Satyam** · [GitHub](https://github.com/satyam-sharma7) · [LinkedIn](https://www.linkedin.com/in/satyam-sharma-778383379/)
