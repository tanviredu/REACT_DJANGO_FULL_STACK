from django.shortcuts import render
from rest_framework import serializers,viewsets,status
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Movie,Rating
from django.contrib.auth.models import User
from .serializers import MovieSerializer,RatingSerializer,UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    ## for authentication
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True,methods=['POST'])
    def rate_movie(self,request,pk=None):
        if "stars" in request.data:
            movie = Movie.objects.get(id=pk)
            stars = request.data['stars']
            #user = User.objects.get(id=1)
            user = request.user
            print(user)
            try:
                ## update operation
                rating = Rating.objects.get(user=user.id,movie=movie.id)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating,many=False)
                response = {"message":"rating updated","result":serializer.data}
                return Response(response,status=status.HTTP_200_OK)
            except:
                #Create
                rating = Rating.objects.create(user=user,movie=movie,stars=stars)
                serializer = RatingSerializer(rating, many=False)
                response = {"message": "rating created", "result": serializer.data}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {"message":"you need to provide the stars"}
            return Response(response,status=status.HTTP_404_NOT_FOUND)





class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    ## override the update method and createmethod
    ## to block functionality from here
    ## we add rating from the MovieViewset

    def update(self,request,*args,**kwargs):
        response = {"message":"THIS OPERATION IS BLOCKED"}
        return Response(response,status=status.HTTP_400_BAD_REQUEST)

    def create(self,request,*args,**kwargs):
        response = {"message":"This Iperation is blocked"}
        return Response(response,status=status.HTTP_400_BAD_REQUEST)