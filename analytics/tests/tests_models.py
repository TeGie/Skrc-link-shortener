from django.test import TestCase

from shorty.models import SkrcUrl
from analytics.models import ClickEvent


class ClickEventModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = SkrcUrl.objects.create(url='https://www.python.org/')

    def test_create_event_manager_passing_bad_instance(self):
        ClickEvent.objects.create_event('bad instance')

        self.assertEqual(0, ClickEvent.objects.all().count())

    def test_create_event_manager(self):
        for _ in range(2):
            ClickEvent.objects.create_event(self.url)

        events = ClickEvent.objects.all()

        self.assertEqual(1, events.count())
        self.assertEqual(1, events.first().pk)
        self.assertEqual(2, events.first().count)
        # tests for relationship
        self.assertEqual(1, events.first().skrc_url.pk)
        self.assertEqual('https://www.python.org/', events.first().skrc_url.url)
        self.assertIsNotNone(events.first().skrc_url.shortcode)
