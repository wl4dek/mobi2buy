from threading import Timer
from short_url.models import UrlShortened
from django.utils.timezone import now


def remove_url(interval=10.0):
    task = Timer(interval=interval, function=remove_url)
    task.daemon = True
    task.start()

    url = UrlShortened.objects.order_by("date_expiration").first()
    today = now()

    if url and url.date_expiration <= today:
        url.delete()
