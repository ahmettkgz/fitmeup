from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class WaterEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    glasses = models.IntegerField(default=0, help_text='Enter the number of glasses of water')

    def __str__(self):
        return f"{self.user.username} - {self.timestamp} - {self.glasses} glasses"

    @property
    def total_glasses(self):
        return self.glasses



