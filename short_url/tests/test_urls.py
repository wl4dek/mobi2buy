from django.test import SimpleTestCase
from django.urls import reverse, resolve
from short_url.views import UrlList, UrlRedirect, UrlCreate


class TestShortUrlUrls(SimpleTestCase):

    def test_list_url_is_resolved(self):
        url = reverse('list')
        self.assertEquals(resolve(url).func.view_class, UrlList)

    def test_create_url_is_resolved(self):
        url = reverse('create')
        self.assertEquals(resolve(url).func.view_class, UrlCreate)

    def test_retrive_url_is_resolved(self):
        url = reverse('retrive', args=['name'])
        self.assertEquals(resolve(url).func.view_class, UrlRedirect)
