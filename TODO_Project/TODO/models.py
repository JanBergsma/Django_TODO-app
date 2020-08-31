from django.db import models

# Create your models here.
class Item(models.Model):
    title = models.CharField(max_length=80)
    completed = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}: {self.title}, {self.completed}, {self.creation_date}'