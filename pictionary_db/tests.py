from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from .models import TempCategory


class HomePageTests(TestCase):

    def setUp(self):
        TempCategory.objects.create(name="warkocz")

    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


class ResultPageTests(SimpleTestCase):

    def test_result_page_status_code(self):
        response = self.client.get('/thanks/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('result_page'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('result_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'result_page.html')
