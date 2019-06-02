from app.models import User, MediaAuthor, Media, Review, TokenManagement
from rest_framework import serializers
from django.contrib.auth.models import User as uu


class UserSerializer(serializers.ModelSerializer):
    authentication = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = User
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    media_name = serializers.CharField(source="media.name")
    username = serializers.CharField(source="author.authentication.username")
    img = serializers.CharField(source="author.img")

    class Meta:
        model = Review
        fields = "__all__"


class MediaAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaAuthor
        fields = "__all__"


class MediaSerializer(serializers.ModelSerializer):

    author = serializers.PrimaryKeyRelatedField(queryset=MediaAuthor.objects.all())

    class Meta:
        model = Media
        fields = "__all__"


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = uu
        fields = "__all__"


class ComboSerializer(serializers.Serializer):

    user = UserSerializer()
    admin = AdminUserSerializer()


class ReviewMediaSerializer(serializers.Serializer):

    review = ReviewSerializer(many=True)
    media = MediaSerializer(many=True)



class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenManagement
        fields = ('token',)


