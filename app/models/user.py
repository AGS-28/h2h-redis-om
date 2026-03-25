from typing import List, Optional
from datetime import datetime, date
from enum import Enum
from redis_om import JsonModel, EmbeddedJsonModel, Field
from app.models.base import BaseMeta

class UserRole(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"

class Address(EmbeddedJsonModel):
    street: str = Field(index=True)
    city: str = Field(index=True)
    state: str = Field(index=True)
    zip_code: str = Field(index=True)
    country: str = Field(default="Indonesia", index=True)

class User(JsonModel):
    # Basic indexed fields
    id: int = Field(index=True)
    username: str = Field(index=True, full_text_search=True)
    email: str = Field(index=True)
    name: str = Field(index=True, full_text_search=True)
    
    # Numeric fields
    age: int = Field(index=True, sortable=True)
    salary: float = Field(index=True, sortable=True)
    
    # Boolean field
    is_active: bool = Field(default=True, index=True)
    
    # Optional field
    bio: Optional[str] = Field(default=None, full_text_search=True)
    
    # Date and Datetime fields
    birth_date: date = Field(index=True)
    joined_at: datetime = Field(default_factory=datetime.now, index=True)
    
    # Enum field
    role: UserRole = Field(default=UserRole.VIEWER, index=True)
    
    # Container types
    tags: List[str] = Field(default=[], index=True)
    metadata: dict = Field(default={})
    
    # Embedded Model
    address: Optional[Address] = Field(default=None)

    class Meta(BaseMeta):
        model_key_prefix = "users"
