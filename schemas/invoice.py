from pydantic import BaseModel, Field

class InvoiceExtract(BaseModel):
    invoice_number: str = Field(description="unique invoice number.")
    invoice_date : str = Field(description="Date which invoice is issued or made.")
    due_date: str = Field(description="Date When amount is to paid.")
    bill_to: str = Field(description="name of the person/company being billed.")
    subtotal: float = Field(description="subtotal before tax")
    tax_amount: float = Field(description="tax value")
    total_amount: float = Field(description="Final amount due.")
