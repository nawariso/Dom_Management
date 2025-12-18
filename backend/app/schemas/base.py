from pydantic import BaseModel


class SchemaBase(BaseModel):
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class ORMModel(SchemaBase):
    id: int
