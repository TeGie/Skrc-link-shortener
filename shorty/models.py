from django.conf import settings
from django.db import models
from django.urls import reverse

from .utils import create_shortcode

SHORTCODE_MAX = getattr(settings, 'SHORTCODE_MAX', 15)


class SkrcUrl(models.Model):
    url = models.URLField(max_length=2000)
    shortcode = models.CharField(max_length=SHORTCODE_MAX, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.shortcode is None or self.shortcode == '':
            self.shortcode = create_shortcode(self)
        super(SkrcUrl, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.url)

    def get_short_url(self):
        url_path = reverse('shortcode', kwargs={'shortcode': self.shortcode})
        return 'https://skrc.herokuapp.com' + url_path
