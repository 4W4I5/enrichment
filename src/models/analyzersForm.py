import json
from pydantic import BaseModel


class AnalyzersForm(BaseModel):
    node_id: str | None = None
    ioc: str
    type: str
    selected_analyzers: list[str]

    # @classmethod
    # def __get_validators__(cls):
    #     yield cls.validate_to_json

    # @classmethod
    # def validate_to_json(cls, value):
    #     if isinstance(value, str):
    #         return cls(**json.loads(value))
    #     return value
