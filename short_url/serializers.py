from .models import UrlShortened
from rest_framework import serializers


class UrlSerializer(serializers.ModelSerializer):
    url = serializers.URLField(required=True)
    name = serializers.CharField(required=False)
    date_expiration = serializers.DateTimeField(required=False)

    class Meta:
        model = UrlShortened
        fields = ["url", "name", "date_expiration"]


class UrlRetriveSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlShortened
        fields = ["url"]
