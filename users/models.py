from django.db import models
from common.models import BasePerson
from django.contrib.auth.models import User


class Athlete(BasePerson):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='athlete_profile')
    sport = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} (Athlete)"


class Chef(BasePerson):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='chef_profile')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} "


class Other(BasePerson):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} (Other)"
