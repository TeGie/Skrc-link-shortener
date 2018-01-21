from unittest.mock import patch

from django.test import TestCase

from shorty.utils import code_generator, create_shortcode
from shorty.models import SkrcUrl


class SkrcUrlModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        SkrcUrl.objects.create(url='http://www.seleniumhq.org/')
        SkrcUrl.objects.create(url='https://www.python.org/', shortcode='')
        SkrcUrl.objects.create(url='https://docs.djangoproject.com/', shortcode='123456')
        cls.urls = SkrcUrl.objects.all()

    def test_shortcodes(self):
        self.assertEqual(6, len(self.urls[0].shortcode))
        self.assertEqual(6, len(self.urls[1].shortcode))
        self.assertEqual('123456', self.urls[2].shortcode)


class UtilsTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = SkrcUrl.objects.create(url='https://www.python.org/')

    def test_code_generator_output_length(self):
        self.assertEqual(6, len(code_generator()))

    def test_create_shortcode_function(self):
        with patch('shorty.utils.code_generator', return_value='123456') as mocked_generator:
            result = create_shortcode(self.url)

            mocked_generator.assert_called_with(size=6)
            self.assertEqual('123456', result)
