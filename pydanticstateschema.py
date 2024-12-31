from pydantic import BaseModel, field_validator, ValidationError

class PydanticState(BaseModel):
    """
        PydanticState class for passing in Graph State
    """
    name: str
    mood: str

    @field_validator("mood")
    @classmethod
    def validate_mood(cls, v):
        """
            Custom validator for mood
        """
        if v not in ["happy", "sad", "angry"]:
            raise ValueError("Invalid mood")
        return v

# try:
#     PydanticState(name="John", mood="happy1")
# except ValidationError as e:
#     print(e)
