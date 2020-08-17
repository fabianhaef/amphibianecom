from django.test import TestCase
from django.urls import reverse


class TestHomeView(TestCase):

    def test_get(self):
        url = reverse('home')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
