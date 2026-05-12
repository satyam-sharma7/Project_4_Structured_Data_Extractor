from openai import OpenAI
from dotenv import load_dotenv
import json
import os

load_dotenv()

client = OpenAI(
    base_url= os.getenv("GOOGLE_URL"),
    api_key= os.getenv("GOOGLE_AI_STUDIO")
)

def extract(file_content, prompt, schema):
    response = client.chat.completions.create(
        model= os.getenv("GOOGLE_MODEL"),
        messages=[
            {"role":"system", "content": f"""{prompt}\n{schema}"""},
            {"role": "user", "content": file_content}
        ],
        temperature= 0.2,
        response_format= {
            "type": "json_object"
        },
    )
    
    return json.loads(response.choices[0].message.content)


with open("json_schemas/schema.json", 'r') as f:
    schema = json.load(f)

def route_and_extract(format: str, file_content: str):
    if format == "article":
        sys_prompt = "You are a structured data extractor. Extract all available fields from this article accurately. For missing fields return null. Do not guess or hallucinate values.return answer in following formate"
        extracted = extract(file_content, sys_prompt, schema["ArticleExtract"])

    elif format == "email":
        sys_prompt = "You are a structured data extractor. Extract all available fields from this email accurately. For missing fields return null. Do not guess or hallucinate values."
        extracted = extract(file_content, sys_prompt, schema["EmailExtract"])

    elif format == "invoice":
        sys_prompt = "You are a structured data extractor. Extract all available fields from this invoice accurately. For missing fields return null. Do not guess or hallucinate values."
        extracted = extract(file_content, sys_prompt, schema["InvoiceExtract"])

    elif format == "resume":
        sys_prompt = "You are a structured data extractor. Extract all available fields from this resume accurately. For missing fields return null. Do not guess or hallucinate values."
        extracted = extract(file_content, sys_prompt, schema["ResumeExtract"])

    else:
        print("content_type function caused problem.")
        print(f"Inferred format: {format}")

    return extracted
