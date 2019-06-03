from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from app.models import MediaAuthor, Media, User, Review, TokenManagement
from rest_framework.response import Response
from app.serializers import MediaAuthorSerializer, MediaSerializer, UserSerializer, ReviewSerializer, \
    AdminUserSerializer, ComboSerializer, TokenSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from django.contrib.auth.models import User as uu
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from collections import namedtuple


# Gets all media
# Given 'max' it returns the max number
@api_view(['GET'])
def get_all_media(request):
    media = Media.objects.all()
    if 'max' in request.GET:
        _max = int(request.GET['max'])
        media = media[:_max]
    serializer = MediaSerializer(media, many=True)
    return Response(serializer.data)


# Designates if a token has the power to change information
def can_change_info(token):
    tkn = TokenManagement.objects.get(token=token)
    us = uu.objects.get(username=tkn.user.authentication)
    if us.is_staff or us.is_superuser:
        return True
    return False


# Gets a single media given an id
# noinspection PyBroadException
@api_view(['GET'])
def get_single_media(request):
    try:
        media_id = int(request.GET['id'])
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        media = Media.objects.get(id=media_id)
    except Media.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = MediaSerializer(media)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Adds New media to DB
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def add_media(request):
    token_auth = str(request.META.get('HTTP_AUTHORIZATION'))  # return `None` if no such header# )
    raw_token = token_auth.replace("token", " ").strip()

    if not can_change_info(raw_token):
        return Response(status.HTTP_401_UNAUTHORIZED)

    MediaAuthor.objects.get(id=int(request.data['author']))
    serializer = MediaSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Search media by name
@api_view(["GET"])
def search_media(request):
    media_name = request.GET["name"]

    try:
        medias = Media.objects.filter(name__contains=media_name)
    except Media.DoesNotExist:
        return Response(status.HTTP_204_NO_CONTENT)

    serializer = MediaSerializer(medias, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

"""
    Deletes a given media
"""


@api_view(["DELETE"])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def del_media(request, name):
    token_auth = str(request.META.get('HTTP_AUTHORIZATION'))  # return `None` if no such header# )
    raw_token = token_auth.replace("token", " ").strip()

    if not can_change_info(raw_token):
        return Response(status.HTTP_401_UNAUTHORIZED)

    try:
        media = Media.objects.get(name=name)
        print(media)
    except Media.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    media.delete()
    return Response(status=status.HTTP_200_OK)


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
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def add_media_author(request):
    serializer = MediaAuthorSerializer(data=request.data)

    token_auth = str(request.META.get('HTTP_AUTHORIZATION'))  # return `None` if no such header# )
    raw_token = token_auth.replace("token", " ").strip()

    if not can_change_info(raw_token):
        return Response(status.HTTP_401_UNAUTHORIZED)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
    Deletes a given media author
"""


@api_view(["DELETE"])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def del_media_author(request, id):
    token_auth = str(request.META.get('HTTP_AUTHORIZATION'))  # return `None` if no such header# )
    raw_token = token_auth.replace("token", " ").strip()

    if not can_change_info(raw_token):
        return Response(status.HTTP_401_UNAUTHORIZED)

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

Combo = namedtuple('Combo', ('user', 'admin'))


@api_view(["GET"])
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
    Registers a user
"""

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        try:
            user = uu.objects.create_user(request.data['username'], request.data['email'], request.data['password'])
            user.save()

            new_usr = User(authentication_id=user.id)
            new_usr.save()

            token, created = Token.objects.get_or_create(user=user)

            tm = TokenManagement(user=new_usr, token=token.key, date_added=datetime.today())
            tm.save()

            serializer = TokenSerializer(tm)
        except:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_user_reviews(request):
    user_id = int(request.GET["id"])
    reviews = Review.objects.filter(author_id=user_id)
    serializer = ReviewSerializer(reviews, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def login(request):

    username = request.data['username']
    password = request.data['password']

    try:
        user = authenticate(username=username, password=password)
    except User.DoesNotExist:
        return Response(status.HTTP_204_NO_CONTENT)
    user_auth = uu.objects.get(username=user)

    try:
        normal_user = User.objects.get(authentication=user_auth.id)
    except User.DoesNotExist:
        return Response(status.HTTP_400_BAD_REQUEST)

    if user is None:
        return Response(status.HTTP_401_UNAUTHORIZED)
    else:

        if Token.objects.get(user=user_auth):
            Token.objects.get(user=user_auth).delete()

        token, created = Token.objects.get_or_create(user=user_auth)

        try:
            t_manager = TokenManagement.objects.get(user=normal_user)

            if t_manager:
                print("Deleted...")
                t_manager.delete()
        except:
            print("All good")

        tm = TokenManagement(user=normal_user, token=token.key, date_added=datetime.today())
        tm.save()

        serializer = TokenSerializer(tm)
        return Response(serializer.data)



@api_view(["PUT"])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def edit_author(request):
    token_auth = str(request.META.get('HTTP_AUTHORIZATION')) # return `None` if no such header# )
    raw_token = token_auth.replace("token", " ").strip()

    if not can_change_info(raw_token):
        return Response(status.HTTP_401_UNAUTHORIZED)

    au_id = int(request.GET["id"])
    try:
        author = MediaAuthor.objects.get(id=au_id)
    except MediaAuthor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = MediaAuthorSerializer(author, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def edit_media(request):
    token_auth = str(request.META.get('HTTP_AUTHORIZATION'))  # return `None` if no such header# )
    raw_token = token_auth.replace("token", " ").strip()

    if not can_change_info(raw_token):
        return Response(status.HTTP_401_UNAUTHORIZED)

    media_id = int(request.GET["id"])
    try:
        media = Media.objects.get(id=media_id)
    except Media.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = MediaSerializer(media, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def edit_media_author(request):
    token_auth = str(request.META.get('HTTP_AUTHORIZATION'))  # return `None` if no such header# )
    raw_token = token_auth.replace("token", " ").strip()

    if not can_change_info(raw_token):
        return Response(status.HTTP_401_UNAUTHORIZED)

    media_author = int(request.GET["id"])
    try:
        media = MediaAuthor.objects.get(id=media_author)
    except MediaAuthor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = MediaAuthorSerializer(media, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_user_by_token(request):
    tokn = request.GET['token']
    try:
        tkn = TokenManagement.objects.get(token=tokn)
    except TokenManagement.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)

    us = uu.objects.get(username=tkn.user.authentication)

    cmb = Combo(
        user=tkn.user,
        admin=us,
    )

    serializer = ComboSerializer(cmb)

    return Response(data=serializer.data)


@api_view(["PUT"])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def edit_user(request):
    user_id = int(request.GET["id"])
    try:
        user = User.objects.get(authentication_id=user_id)
        us = uu.objects.get(username=user.authentication)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = AdminUserSerializer(us, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def edit_user_not_admin(request):
    user_id = int(request.GET["id"])
    try:
        user = User.objects.get(id=user_id)
        us = uu.objects.get(username=user.authentication)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = AdminUserSerializer(us, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

