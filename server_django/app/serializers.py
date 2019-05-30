from app.models import User, MediaAuthor, Media, Review
from rest_framework import serializers
from django.contrib.auth.models import User as uu


class UserSerializer(serializers.ModelSerializer):
    authentication = serializers.PrimaryKeyRelatedField(read_only=True)

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


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = uu
        fields = "__all__"


class ComboSerializer(serializers.Serializer):
    user = UserSerializer()
    admin = AdminUserSerializer()



