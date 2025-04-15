from uuid import uuid4
from django.db import models

class CastMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=255, blank=False)
    type = models.CharField(max_length=50, choices=[('ACTOR', 'ACTOR'), ('DIRECTOR', 'DIRECTOR')], blank=False)
    
    class Meta:
        db_table = "cast_members"
        
    def __str__(self):
        return self.name