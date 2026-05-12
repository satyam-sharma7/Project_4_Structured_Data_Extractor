from pydantic import BaseModel, Field

class ResumeExtract(BaseModel):
    full_name: str = Field(description="Full name of the candidate.")
    email: str = Field(description="Email of the candidate")
    skills: list[str]
    years_of_experience: int = Field("inferred as an integer")
    most_recent_role:str
    education: list[str]
