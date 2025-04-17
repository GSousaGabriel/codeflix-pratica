from dataclasses import dataclass
from enum import StrEnum
from src.core._shared.entity import Entity

class CastMemberTypeEnum(StrEnum):
    ACTOR = "ACTOR"
    DIRECTOR = "DIRECTOR"

@dataclass
class CastMember(Entity):
    name: str
    type: CastMemberTypeEnum
    
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
            self.notification.add_error("Name should not be longer than 255 characters")
        elif not self.name:
            self.notification.add_error("Name should not be empty")
        
        if self.type not in CastMemberTypeEnum:
            self.notification.add_error("Type should be either ACTOR or DIRECTOR")
            
        if self.notification.has_errors:
            raise ValueError(self.notification.messages)
        
    def __str__(self):
        return f"{self.name} - ({self.type})"
    
    def __repr__(self):
        return f"<Genre {self.name} ({self.id})>"