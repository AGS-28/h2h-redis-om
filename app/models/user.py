from redis_om import JsonModel, Field
from app.models.base import BaseMeta

class User(JsonModel):
    id: int = Field(index=True)
    username: str = Field(index=True)
    email: str = Field(index=True)
    name: str = Field(index=True)

    class Meta(BaseMeta):
        model_key_prefix = "users"
