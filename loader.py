import os
from pathlib import Path
from enum import Enum
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def content_type(path: str):

    with open(path, 'r', encoding="utf-8") as f:
        file_content = f.read()

    class ContentCategory(str, Enum):
        INVOICE = 'invoice'
        EMAIL = "email"
        ARTICLE = "article"
        RESUME = "resume"

    class FileClassifier(BaseModel):
        category: ContentCategory

    client = OpenAI(
        base_url= os.getenv("GOOGLE_URL"),
        api_key= os.getenv("GOOGLE_AI_STUDIO")
    )

    response = client.chat.completions.parse(
        model= os.getenv("GOOGLE_MODEL"),
        messages=[
            {"role": "system", "content": "Classify the following text into exactly one category."},
            {"role": "user", "content": file_content}
        ],
        response_format= FileClassifier
    )

    result = response.choices[0].message.parsed

    return result.category.value, file_content    # --> invoicee|email|article|resume

