from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from app.models import MediaAuthor, Media, User, Review
from rest_framework.response import Response
from app.serializers import MediaAuthorSerializer, MediaSerializer, UserSerializer, ReviewSerializer, \
    AdminUserSerializer, ComboSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from django.contrib.auth.models import User as uu


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    tparams = {
        'title': 'Home Page',
        'year': datetime.now().year,
    }
    return render(request, 'index.html', tparams)


""" 
    Gets all media 
    Given a <b> max </b> num returns that ammount
"""


@api_view(['GET'])
def get_all_media(request):
    media = Media.objects.all()
    if 'max' in request.GET:
        _max = int(request.GET['max'])
        media = media[:_max]
    serializer = MediaSerializer(media, many=True)
    return Response(serializer.data)


"""
    Gets a media given an ID
"""


@api_view(['GET'])
def get_media(request):
    id = int(request.GET['id'])

    try:
        media = Media.objects.get(id=id)
    except Media.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = MediaSerializer(media)
    return Response(serializer.data)


"""
    Adds media to the database!

    todo: Images seem to not work correctly
"""


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def add_media(request):
    serializer = MediaSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
    Deletes a given media
"""


@api_view(["DELETE"])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def del_media(request, name):
    try:
        media = Media.objects.get(name=name)
    except Media.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    media.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


"""
    Gets all media authors
"""


@api_view(["GET"])
def get_all_media_authors(request):
    media_authors = MediaAuthor.objects.all()
    if 'max' in request.GET:
        _max = int(request.GET['max'])
        media_authors = media_authors[:_max]
    serializer = MediaAuthorSerializer(media_authors, many=True)
    return Response(serializer.data)


"""
    Gets media authors
"""


@api_view(["GET"])
def get_media_authors(request):
    id = int(request.GET["id"])

    try:
        media_author = MediaAuthor.objects.get(id=id)
    except MediaAuthor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = MediaAuthorSerializer(media_author)
    return Response(serializer.data)


"""
    Adds media authors to the database!

    todo: Images seem to not work correctly
"""


@api_view(['POST'])
def add_media_author(request):
    serializer = MediaAuthorSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
    Deletes a given media author
"""


@api_view(["DELETE"])
def del_media_author(request, id):
    try:
        media_author = MediaAuthor.objects.get(id=id)
    except MediaAuthor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    media_author.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


"""
    Gets all reviews
"""


@api_view(["GET"])
def get_all_reviews(request):
    reviews = Review.objects.all()
    if 'max' in request.GET:
        _max = int(request.GET['max'])
        reviews = reviews[:_max]
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


"""
    Gets reviews of a media
"""


@api_view(["GET"])
def get_media_reviews(request):
    id = int(request.GET["id"])

    try:
        review_list = Review.objects.filter(media=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ReviewSerializer(review_list, many=True)
    return Response(serializer.data)


"""
    Adds a review
"""


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def add_review(request):
    serializer = ReviewSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
    Gets the user
"""
from collections import namedtuple

Combo = namedtuple('Combo', ('user', 'admin'))


@api_view(["GET"])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_user(request):
    id = int(request.GET["id"])

    try:

        user = User.objects.get(id=id)
        uup = user.authentication

        cmb = Combo(
            user=user,
            admin=uup,
        )

    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ComboSerializer(cmb)

    return Response(serializer.data)


"""
    Adds a user
"""


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def add_user(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        user = uu.objects.create_user(request.data['username'], 'example@thebeatles.com', request.data['password'])
        user.save()

        serializer.authentication = user.id
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_user_reviews(request):
    user_id = int(request.GET["id"])
    reviews = Review.objects.filter(author_id=user_id)
    print(reviews)
    serializer = ReviewSerializer(reviews, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
