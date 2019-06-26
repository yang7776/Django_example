from django.db import models

class Product(models.Model):
    
    class Meta:
        ordering = ('created',)
    # def __str__(self):
    #     return self.name