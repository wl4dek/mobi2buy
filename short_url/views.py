from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import UrlShortened
from .serializers import UrlSerializer, UrlRetriveSerializer


class UrlCreate(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = UrlShortened.objects.all()
    serializer_class = UrlSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        path = reverse('retrive', kwargs={"name": response.data.get("name")})
        host = request.META.get('HTTP_HOST')
        result = f"{request.META.get('wsgi.url_scheme')}://{host}{path}"
        response.data = {
            "url": result
        }
        return response


class UrlList(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = UrlShortened.objects.all()
    serializer_class = UrlSerializer


class UrlRedirect(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    lookup_field = "name"
    queryset = UrlShortened.objects.all()
    serializer_class = UrlRetriveSerializer

    def retrieve(self, request, *args, **kwargs):
        result = super().retrieve(request, *args, **kwargs)
        return HttpResponseRedirect(redirect_to=result.data.get("url"))
