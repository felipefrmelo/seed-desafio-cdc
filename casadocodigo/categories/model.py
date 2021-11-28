from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Category:
    id: int = field(init=False)
    name: str
  