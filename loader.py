import os
import json
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
        base_url= os.getenv("OPENROUTER_URL"),
        api_key= os.getenv("OPENROUTER_API_KEY_2")
    )

    response = client.chat.completions.create(
        # model= os.getenv("GOOGLE_MODEL"),
        model = "inclusionai/ring-2.6-1t:free",
        messages=[
            {
                "role": "system",
                "content": """Classify the following text into exactly 
                one category as following format:
                {
                    "file_type":"article/resume/email/invoice"
                }
                """
            },

            {"role": "user", "content": file_content}
        ],
        response_format={
            "type": "json_object"
        }
    )

    result = json.loads(response.choices[0].message.content)    # --> invoicee|email|article|resume
    return result["file_type"], file_content


