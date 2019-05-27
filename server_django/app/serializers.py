from app.models import User, MediaAuthor, Media, Review
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class MediaAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaAuthor
        fields = "__all__"


class MediaSerializer(serializers.ModelSerializer):

    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Media
        fields = "__all__"


