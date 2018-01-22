from django.test import TestCase

from shorty.models import SkrcUrl


class HomeViewTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'shorty/base.html')
        self.assertTemplateUsed(response, 'shorty/home.html')

    def test_page_can_save_a_POST_request(self):
        self.client.post('/', data={'url': 'https://docs.djangoproject.com/'})

        self.assertEqual(1, SkrcUrl.objects.all().count())
        self.assertEqual('https://docs.djangoproject.com/', SkrcUrl.objects.first().url)

    def test_page_returns_correct_html_after_POST_request(self):
        response = self.client.post('/', data={'url': 'https://docs.djangoproject.com/'})

        self.assertContains(response, 'https://docs.djangoproject.com/')
        self.assertTemplateUsed(response, 'shorty/base.html')
        self.assertTemplateUsed(response, 'shorty/shortcode.html')

    def test_page_handles_two_POSTS_requests_correctly(self):
        self.client.post('/', data={'url': 'https://docs.djangoproject.com/'})
        self.client.post('/', data={'url': 'https://www.python.org/'})
        urls = SkrcUrl.objects.all()

        self.assertEqual(2, urls.count())
        self.assertEqual('https://docs.djangoproject.com/', urls[0].url)
        self.assertEqual('https://www.python.org/', urls[1].url)

    def test_page_cannot_save_a_POST_request_twice(self):
        response = self.client.post('/', data={'url': 'https://docs.djangoproject.com/'})
        response2 = self.client.post('/', data={'url': 'https://docs.djangoproject.com/'})

        self.assertEqual(1, SkrcUrl.objects.all().count())
        self.assertTrue(list(response.context[0])[0].get('created'))
        self.assertFalse(list(response2.context[0])[0].get('created'))

    def test_page_handles_empty_data_correctly(self):
        self.client.post('/', data={'url': ''})

        self.assertEqual(0, SkrcUrl.objects.all().count())

    def test_page_handles_incorrect_data_correctly(self):
        response = self.client.post('/', data={'url': 'abcd'})

        self.assertEqual(0, SkrcUrl.objects.all().count())
        self.assertContains(response, 'Enter a valid URL.')


class RedirectViewTest(TestCase):

    def test_page_redirects_correctly(self):
        self.client.post('/', data={'url': 'https://docs.djangoproject.com/'})
        shortcode = SkrcUrl.objects.first().shortcode
        response = self.client.get(f'/{shortcode}/')

        self.assertRedirects(response, 'https://docs.djangoproject.com/')

    def test_page_redirects_bad_shortcode_to_404_template(self):
        self.client.post('/', data={'url': 'https://docs.djangoproject.com/'})
        shortcode = SkrcUrl.objects.first().shortcode
        response = self.client.get(f'/{shortcode[3:] + shortcode[:3]}/')

        self.assertEqual(404, response.status_code)
        self.assertTemplateUsed(response, '404.html')
        self.assertTemplateUsed(response, 'shorty/base.html')
