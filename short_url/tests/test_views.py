from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from short_url.models import UrlShortened


class TestShortUrlViews(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.valid_url = {
            "url": "https://mobi2buy.com/",
            "name": "mob2by"
        }
        UrlShortened.objects.create(**self.valid_url)
        self.user = get_user_model().objects.create_user(
            'user.test@email.com',
            'user_test'
        )

    def test_no_authenticate_get_list_urls(self):
        response = self.client.get(reverse("list"))
        self.assertEquals(response.status_code, 403)

    def test_authenticated_get_list_urls(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse("list"))
        self.assertEquals(len(response.json().get("results")), 1)
        self.assertDictContainsSubset(
            self.valid_url, response.json().get("results")[0])

    def test_get_retrive_urls(self):
        response = self.client.get(reverse("retrive", args=["mob2by"]))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, "https://mobi2buy.com/")

    def test_create_url(self):
        response = self.client.post(reverse("create"), {
            "url": "https://mobi2buy.com/",
            "name": "m2by"
        })
        path = reverse("retrive", kwargs={"name": "m2by"})
        self.assertEquals(response.status_code, 201)
        self.assertDictEqual(response.json(), {"url": f"http://None{path}"})

    def test_create_url_invalid_values(self):
        response = self.client.post(reverse("create"), {"url": ""})
        self.assertEquals(response.status_code, 400)
