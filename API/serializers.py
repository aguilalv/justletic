from rest_framework import serializers

class KeySerializer(serializers.Serializer):
    token = serializers.CharField(max_length=50)
    strava_id = serializers.CharField(max_length=50)

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=150)

class TokenSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    key = serializers.CharField(max_length=40)
