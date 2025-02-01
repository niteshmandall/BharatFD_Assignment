from django.test import TestCase
from .models import FAQ

class FAQTest(TestCase):
    def test_faq_creation(self):
        faq = FAQ.objects.create(
            question_en="What is Python?",
            answer_en="Python is a programming language."
        )
        self.assertTrue(faq.question_hi)  # Check Hindi translation
        self.assertTrue(faq.question_bn)  # Check Bengali translation

    def test_api_endpoint(self):
        response = self.client.get('/api/faqs/?lang=hi')
        self.assertEqual(response.status_code, 200)