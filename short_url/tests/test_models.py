from django.test import TestCase
from short_url.models import UrlShortened
from django.forms.models import model_to_dict
from django.utils import timezone
from datetime import timedelta
from scripts.remove_urls import remove_url


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

    def test_remove_url(self):
        today = timezone.now()

        UrlShortened.objects.create(**{
            "url": "http://teste.com",
            "date_expiration": today - timedelta(1)
        })
        UrlShortened.objects.create(**{
            "url": "http://teste2.com",
            "date_expiration": today + timedelta(1)
        })

        self.assertEquals(UrlShortened.objects.count(), 3)
        remove_url()
        self.assertEquals(UrlShortened.objects.count(), 2)
        url = UrlShortened.objects.order_by("date_expiration").first()
        date_expiration = str(url.date_expiration)
        self.assertEquals(date_expiration, str(today + timedelta(1)))
