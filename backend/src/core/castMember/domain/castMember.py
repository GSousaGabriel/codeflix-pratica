from dataclasses import dataclass, field
from enum import StrEnum
from uuid import UUID
import uuid

class CastMemberTypeEnum(StrEnum):
    ACTOR = "ACTOR"
    DIRECTOR = "DIRECTOR"

@dataclass
class CastMember:
    name: str
    type: CastMemberTypeEnum
    id: UUID = field(default_factory=uuid.uuid4)
    
    def __post_init__(self):
        self.validate()
        
    def change_name(self, name: str):
        self.name = name
        self.validate()
        
    def change_type(self, type: CastMemberTypeEnum):
        self.type = type
        self.validate()
        
    def validate(self):
        if len(self.name) > 255:
            raise ValueError("Name should not be longer than 255 characters")
        elif not self.name:
            raise ValueError("Name should not be empty")
        
        if self.type not in CastMemberTypeEnum:
            raise ValueError("Type should be either ACTOR or DIRECTOR")
        
    def __str__(self):
        return f"{self.name} - ({self.type})"
    
    def __repr__(self):
        return f"<Genre {self.name} ({self.id})>"
    
    def __eq__(self, other):
        return (self.id == other.id) and isinstance(other, CastMember)