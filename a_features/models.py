from django.db import models

# Create your models here.
class Feature(models.Model):
    name = models.CharField(max_length=255, unique=True)
    developer = models.CharField(max_length=255, unique=True)
    staging_enabled = models.BooleanField(default=False)
    production_enabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created']