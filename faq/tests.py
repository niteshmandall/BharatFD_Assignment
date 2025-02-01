import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import FAQ

# Using pytest fixtures for setting up common objects

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def faq_instance(db):
    """
    Create and return an FAQ instance for testing.
    The `db` fixture provided by pytest-django ensures access to the test database.
    """
    faq = FAQ.objects.create(
        question_en="What is Python?",
        answer_en="Python is a popular programming language."
    )
    return faq


# ---------------------------
# Model Tests
# ---------------------------

@pytest.mark.django_db
def test_auto_translations_generated(faq_instance):
    """
    Test that the FAQ model automatically generates translations.
    """
    # Ensure translations are generated and differ from the English text
    assert faq_instance.question_hi, "Hindi translation should be generated"
    assert faq_instance.question_bn, "Bengali translation should be generated"
    assert faq_instance.question_hi != faq_instance.question_en, \
        "Hindi translation should be different from the English question"
    assert faq_instance.question_bn != faq_instance.question_en, \
        "Bengali translation should be different from the English question"


# ---------------------------
# API Tests
# ---------------------------

@pytest.mark.django_db
def test_get_faqs_default_language(api_client, faq_instance):
    """
    Test retrieving FAQs in the default language (English).
    """
    list_url = reverse('faq-list')  # Provided by the DefaultRouter
    response = api_client.get(list_url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    # Verify that the question and answer match the English fields
    assert data[0]['question'] == faq_instance.question_en
    assert data[0]['answer'] == faq_instance.answer_en

@pytest.mark.django_db
def test_get_faqs_in_hindi(api_client, faq_instance):
    """
    Test retrieving FAQs in Hindi using the ?lang=hi query parameter.
    """
    list_url = reverse('faq-list')
    response = api_client.get(f"{list_url}?lang=hi")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    # Compare with the Hindi translation from the model
    assert data[0]['question'] == faq_instance.question_hi

@pytest.mark.django_db
def test_update_faq_patch(api_client, faq_instance):
    """
    Test updating an FAQ using the PATCH method.
    """
    detail_url = reverse('faq-detail', kwargs={'pk': faq_instance.id})
    update_data = {
        "answer_en": "Updated answer using PATCH."
    }
    response = api_client.patch(detail_url, data=update_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    # Refresh the instance from the database
    faq_instance.refresh_from_db()
    assert faq_instance.answer_en == update_data["answer_en"]

@pytest.mark.django_db
def test_delete_faq(api_client, faq_instance):
    """
    Test deletion of an FAQ.
    """
    detail_url = reverse('faq-detail', kwargs={'pk': faq_instance.id})
    response = api_client.delete(detail_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # Verify that the FAQ is no longer in the database
    assert not FAQ.objects.filter(pk=faq_instance.id).exists()
