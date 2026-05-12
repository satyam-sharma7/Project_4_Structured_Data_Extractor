from pydantic import BaseModel, Field

class EmailExtract(BaseModel):
    sender: str = Field(description="Email id of sender")
    subject: str = Field(description="Description of email inferred if not explicitly stated")
    summary: str = Field(description="Summarize in one sentence, max 20 words")
    action_items: list[str] = Field(description="things user need to do")
    key_information: list[str] = Field(description="important facts stated (not actions, just info)")
