from pydantic import BaseModel
from typing import Any, List, Optional

class FilterItem(BaseModel):
    field: str
    op: str
    value: Any

class QueryRequest(BaseModel):
    model: str
    filters: Optional[List[FilterItem]] = []
    limit: Optional[int] = None
    offset: Optional[int] = None
    sort_by: Optional[str] = None
    sort_asc: bool = True
    fields: Optional[List[str]] = None
