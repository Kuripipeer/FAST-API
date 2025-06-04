from pydantic import BaseModel, Field

class Computer(BaseModel):
    brand: str = Field(min_length=1, max_length=15)
    model: str = Field(max_length=30)
    color: str = Field(min_length=3, max_length=15)
    ram: str = Field(min_length=1, max_length=8)
    storage: str = Field(min_length=1, max_length=8)

    class Config:
        json_schema_extra = {
            "example": {
                "brand": "HP",
                "model": "Pavilion",
                "color": "Black",
                "ram": "16 GB",
                "storage" : "1TB"
            }
        }