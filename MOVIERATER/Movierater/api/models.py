from enum import unique
from django.core import validators
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator


class Movie(models.Model):
    title       = models.CharField(max_length=200)
    description = models.TextField(max_length=360)

    def no_of_ratings(self):
        ratings = Rating.objects.filter(movie=self)
        return len(ratings)

    def avg_rating(self):
        sum = 0
        ratings = Rating.objects.filter(movie=self)
        for rating in ratings:
            sum+=rating.starts
        if (len(ratings)) > 0:
            return sum/len(ratings)
        else:
            return 0

    
    def __str__(self):
        return str(self.title)

class Rating(models.Model):
    movie       = models.ForeignKey(Movie,on_delete=models.CASCADE)
    user        = models.ForeignKey(User,on_delete=models.CASCADE)
    starts      = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])

    def __str__(self):
        return str(self.movie)


    class Meta:
        unique_together = (('user','movie'))
        index_together  = (('user','movie'))

