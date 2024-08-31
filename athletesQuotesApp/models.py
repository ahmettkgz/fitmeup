from django.urls import reverse
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

from common.models import BasePerson
from users.models import Athlete


class AthleteQuote(models.Model):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    inspiration = models.CharField(max_length=350)
    posting_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.inspiration} by {self.athlete.user.username}"

    def get_absolute_url(self):
        return reverse('quote_details', kwargs={'id': self.id})
