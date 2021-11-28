from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Author:
    id: int = field(init=False)
    name: str
    email: str
    description: str
    createdAt: datetime = field(default_factory=datetime.utcnow)
