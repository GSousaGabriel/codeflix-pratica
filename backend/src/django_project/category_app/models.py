from uuid import uuid4
from django.db import models

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    
    
    class Meta:
        db_table = "category"
    
    def __str__(self):
        return self.name