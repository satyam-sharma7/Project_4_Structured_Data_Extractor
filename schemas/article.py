from pydantic import BaseModel, Field

class ArticleExtract(BaseModel):
    title: str = Field(description="extracted or inferred title of article")
    author: str = Field(description="author if  mentioned")
    key_points: list[str] = Field(description="The core arguments or facts")
