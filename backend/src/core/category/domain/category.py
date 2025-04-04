from dataclasses import dataclass, field
import uuid
from uuid import UUID

@dataclass
class Category:
    name: str
    description: str = ""
    is_active: bool = True
    id: UUID = field(default_factory=uuid.uuid4)
    
    def __post_init__(self):
        self.validate()
        
    def update_category(self, name, description):
        self.name = name
        self.description = description
        self.validate()
        
    def activate(self):
        self.is_active = True
        self.validate()
        
    def deactivate(self):
        self.is_active = False
        self.validate()
        
    def validate(self):
        if(len(self.name) > 255):
            raise ValueError("Name should not be longer than 255 characters")
        elif not self.name:
            raise ValueError("Name should not be empty")
        
    def __str__(self):
        return f"{self.name} - {self.description} ({self.is_active})"
    
    def __repr__(self):
        return f"<Category {self.name} ({self.id})>"
    
    def __eq__(self, other):
        return (self.id == other.id) and isinstance(other, Category)