from pydantic import BaseModel, EmailStr, Field, field_validator


class EmployeeCreate(BaseModel):
    name: str = Field(max_length=255)
    email: EmailStr
    position: str = Field(max_length=255)

    @field_validator("name", "position")
    @classmethod
    def validate_non_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be empty")
        return value


class EmployeeResponse(EmployeeCreate):
    id: int