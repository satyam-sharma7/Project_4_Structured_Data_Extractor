from openai import OpenAI
from dotenv import load_dotenv
import json
import os

from schemas.article import ArticleExtract
from schemas.email import EmailExtract
from schemas.invoice import InvoiceExtract
from schemas.resume import ResumeExtract

load_dotenv()

client = OpenAI(
    base_url= os.getenv("GOOGLE_URL"),
    api_key= os.getenv("GOOGLE_AI_STUDIO")
)

def extract(file_content, prompt, schema):
    response = client.chat.completions.parse(
        model= os.getenv("GOOGLE_MODEL"),
        messages=[
            {"role":"system", "content": prompt},
            {"role": "user", "content": file_content}
        ],
        temperature= 0.2,
        response_format= schema,
    )
    
    return json.loads(response.choices[0].message.content)


def route_and_extract(format: str, file_content: str):
    if format == "article":
        sys_prompt = "You are a structured data extractor. Extract all available fields from this article accurately. For missing fields return null. Do not guess or hallucinate values."
        extracted = extract(file_content, sys_prompt, ArticleExtract)

    elif format == "email":
        sys_prompt = "You are a structured data extractor. Extract all available fields from this email accurately. For missing fields return null. Do not guess or hallucinate values."
        extracted = extract(file_content, sys_prompt, EmailExtract)

    elif format == "invoice":
        sys_prompt = "You are a structured data extractor. Extract all available fields from this invoice accurately. For missing fields return null. Do not guess or hallucinate values."
        extracted = extract(file_content, sys_prompt, InvoiceExtract)

    elif format == "resume":
        sys_prompt = "You are a structured data extractor. Extract all available fields from this resume accurately. For missing fields return null. Do not guess or hallucinate values."
        extracted = extract(file_content, sys_prompt, ResumeExtract)

    else:
        print("content_type function caused problem.")
        print(f"Inferred format: {format}")

    return extracted
