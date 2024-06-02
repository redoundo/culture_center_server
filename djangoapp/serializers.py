from rest_framework import serializers
from .models import *


class LecturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lectures
        fields = '__all__'


class CentersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Centers
        fields = '__all__'


class BranchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branches
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class TargetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Targets
        fields = '__all__'


class LikedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liked
        fields = '__all__'


class AppliedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applied
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


