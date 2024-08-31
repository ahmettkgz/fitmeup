from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.db import models
from users.models import Chef


class Category(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('-name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('recipe:recipe_by_category', args=[self.slug])


class Recipe(models.Model):
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    ingredients = models.CharField(max_length=250)
    instructions = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    CATEGORY_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('special_event', 'Special Event'),
    ]
    categories = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe_details', args=[str(self.id)])
