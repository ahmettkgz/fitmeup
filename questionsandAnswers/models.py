from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Question(models.Model):
    title = models.CharField(max_length=100)
    details = models.TextField(max_length=1000)
    recievers = models.CharField(max_length=10,
                                 choices=[('athlete', 'Athletes'), ('chef', 'Chefs'), ('other', 'Others')])
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('questionandanswerdetails', kwargs={'pk': self.pk})  # provide a link to see the details of it


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Answer to: {self.question.title}"
