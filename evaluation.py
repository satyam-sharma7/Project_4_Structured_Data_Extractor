from openai import OpenAI
from dotenv import load_dotenv
import json
import os


load_dotenv()

client = OpenAI(
    base_url= os.getenv("GOOGLE_URL"),
    api_key= os.getenv("GOOGLE_AI_STUDIO")
)
def score(extracted: dict, schema: dict, raw_content: str):
    response = client.chat.completions.create(
        model=os.getenv("GOOGLE_MODEL"),
        messages=[
            {
                "role": "system",
                "content": """You are a strict evaluator of AI extraction quality.
You will be given:
1. The original raw document
2. The desired output schema  
3. The actual AI extraction output

Score the extraction from 0.0 to 1.0:
- 1.0 = perfect, all fields correctly extracted
- 0.7 = mostly correct, 1-2 minor errors or missing fields
- 0.5 = partial, several missing or wrong fields
- 0.0 = completely wrong or empty

Be strict. Penalize missing fields, hallucinated values, and wrong data types.
Respond ONLY with JSON: {"score": 0.72, "reason": "brief explanation"}"""
            },
            {
                "role": "user",
                "content": f"""Raw document:
{raw_content}

Desired schema:
{json.dumps(schema, indent=2)}

Actual extraction:
{json.dumps(extracted, indent=2)}"""
            }
        ],
        response_format={"type": "json_object"}
    )

    result = json.loads(response.choices[0].message.content)
    return result["score"], result["reason"]
