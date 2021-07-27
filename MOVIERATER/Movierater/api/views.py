from django.http import response
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import serializers, viewsets,status
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Movie,Rating
from django.contrib.auth.models import User
from .serializers import MovieSerializer,RatingSerializer,UserSerializer



class UserViewSet(viewsets.ModelViewSet):
    queryset   = User.objects.all()
    serializer_class = UserSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset   = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    ## make a custom 
    ## details = True the url will be api/movies/<pk>/rate_movie
    
   ## adding custom endpoint
    @action(detail=True,methods=["POST"])
    def rate_movie(self,request,pk=None):
        if "starts" in request.data:
            ## we neeed three attribute for rating a movie
            # 1) starts which is the rating
            # 2) the movie object
            # 3) the user id
            # fetch the movie
            movie = Movie.objects.get(id=pk)
            starts = request.data["starts"]
            ## create a static user for This time
            #user = User.objects.get(id=1)
            user = request.user
            try:
                rating = Rating.objects.get(user=user.id,movie=movie.id)
                rating.starts = starts
                rating.save()
                serializer = RatingSerializer(rating,many=False)
                response = {"message":"rating updated","result":serializer.data}
                return Response(response,status=status.HTTP_200_OK)
            except:
                rating = Rating.objects.create(user=user,movie=movie,starts=starts)
                serializer = RatingSerializer(rating,many=False)
                response = {"message":"rating created","result":serializer.data}
                return Response(response,status=status.HTTP_200_OK)
        else:
            response = {"message":"you need to provide the starts"}
            return Response(response,status = status.HTTP_404_NOT_FOUND)

            

            






class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    ### you should not update and create the ratings
    ### directly from RatingViewSet
    ### you need to do that with rate_movie
    ### so override the update and create method
    ### to block this

    def update(self,request,*args,**kwargs):
        response = {"message":"you cant do that in this way"}
        return Response(response,status=status.HTTP_404_NOT_FOUND)
    def create(self,request,*args,**kwargs):
        response = {"message":"you cant do that in this way"}
        return Response(response,status=status.HTTP_404_NOT_FOUND)
        
 
