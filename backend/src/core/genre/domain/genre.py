from dataclasses import dataclass, field
from uuid import UUID
from src.core._shared.entity import Entity

@dataclass
class Genre(Entity):
    name: str
    categories_ids: set[UUID] = field(default_factory=set)
    is_active: bool = True
    
    def __post_init__(self):
        self.validate()
        
    def change_name(self, name):
        self.name = name
        self.validate()
        
    def activate(self):
        self.is_active = True
        self.validate()
        
    def deactivate(self):
        self.is_active = False
        self.validate()
    
    def add_category(self, category_id: UUID):
        self.categories_ids.add(category_id)
        self.validate()
    
    def remove_category(self, category_id: UUID):
        self.categories_ids.remove(category_id)
        self.validate()
    
    def clear_category(self):
        self.categories_ids.clear()
        self.validate()
        
    def validate(self):
        if(len(self.name) > 255):
            self.notification.add_error("Name should not be longer than 255 characters")
        elif not self.name:
            self.notification.add_error("Name should not be empty")
            
        if self.notification.has_errors:
            raise ValueError(self.notification.messages)
        
    def __str__(self):
        return f"{self.name} - ({self.is_active})"
    
    def __repr__(self):
        return f"<Genre {self.name} ({self.id})>"