from django.db import models
from django.contrib.auth.models import User


## defining the database

class Movie(models.Model):
    ''' MOVIE TABLE WITH TITLE AND DESCRIPTION
    '''
    title       = models.CharField(max_length=200)
    description = models.TextField(max_length=400)

    def no_of_ratings(self):

        ''' IT RETURN HOW MANY PEOPLE
        RATE THIS MOVIE NOT THE SUM OF
        RATING'''
        ratings = Rating.objects.filter(movie=self)
        return len(ratings)

    def avg_rating(self):
        ''' RETURN THE AVERAGE RATING
            SUM OF THE RATING DEVIDED BY
            THE NO OF RATING
         '''
        sum = 0
        ratings = Rating.objects.filter(movie=self)
        for rating in ratings:
            sum+=rating.stars
            if(len(ratings))>0:
                return sum/len(ratings)
            else:
                return 0

    def __str__(self):
        return str(self.title)


class Rating(models.Model):
    '''
        RATING IT HAS A USER NUMBRT OF STARS
        AND MOVIE FROM THE MOVIE TABLE
        AND USER FROM THJE USER TABLE
    '''

    movie       = models.ForeignKey(Movie,on_delete=models.CASCADE)
    user        = models.ForeignKey(User,on_delete=models.CASCADE)
    stars       = models.IntegerField()

    def __str__(self):
        return str(self.movie)

    class Meta:
        unique_together = (('user','movie'))
        index_together  = (('user','movie'))