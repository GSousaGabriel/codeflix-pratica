from uuid import uuid4
from django.db import models

class Genre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=255, blank=False)
    categories_ids = models.ManyToManyField('category_app.Category', related_name='genres')
    is_active = models.BooleanField(default=True)
    
    
    class Meta:
        db_table = "genres"
    
    def __str__(self):
        return self.name