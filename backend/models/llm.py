class VerifyRequest(BaseModel):
    user_answer: str
    question: str
    context: str