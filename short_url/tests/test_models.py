from django.test import TestCase
from short_url.models import UrlShortened
from django.forms.models import model_to_dict
from django.utils import timezone
from datetime import timedelta


class TestModels(TestCase):

    def setUp(self):
        self.valid_url = {
            'url': 'https://mobi2buy.com/',
            'name': 'mob2by',
            'date_expiration': timezone.now()
        }
        self.invalid_url = {'url': ""}
        self.urlshort = UrlShortened.objects.create(**{
            'url': 'https://mobi2buy.com/'
        })

    def test_url_is_created(self):
        self.assertEquals(self.urlshort.url, 'https://mobi2buy.com/')

    def test_create_valid_url(self):
        url = UrlShortened.objects.create(**self.valid_url)
        self.assertDictEqual(model_to_dict(url), self.valid_url)

    def test_create_valid_url_no_date_expiration(self):
        del self.valid_url['date_expiration']
        url = UrlShortened.objects.create(**self.valid_url)
        self.assertEquals(url.url, self.valid_url['url'])
        self.assertEquals(url.name, self.valid_url['name'])

        to_day = timezone.now().day
        date_expiration = url.date_expiration - timedelta(7)
        self.assertEquals(to_day, date_expiration.day)

    def test_create_valid_url_no_name(self):
        del self.valid_url['name']
        url = UrlShortened.objects.create(**self.valid_url)
        self.assertEquals(url.url, self.valid_url['url'])
        self.assertEquals(url.date_expiration,
                          self.valid_url['date_expiration'])
        self.assertIsNot(url.name, '')

    def test_dont_create_invalid_url(self):
        url = UrlShortened.objects.create(**self.invalid_url)
        self.assertEquals(url.url, self.invalid_url['url'])

    def test_get_all_urls(self):
        count = UrlShortened.objects.all().count()
        self.assertEquals(count, 1)
