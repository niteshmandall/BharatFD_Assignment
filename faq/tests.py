import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import FAQ

# ---------------------------
# Fixtures for Common Objects
# ---------------------------

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def faq_instance(db):
    """
    Create and return an FAQ instance for testing.
    """
    return FAQ.objects.create(
        question_en="What is Python?",
        answer_en="Python is a high-level programming language."
    )

@pytest.fixture
def multiple_faqs(db):
    """
    Create multiple FAQ instances for testing list endpoints.
    """
    FAQ.objects.create(question_en="What is Django?", answer_en="Django is a web framework.")
    FAQ.objects.create(question_en="What is AI?", answer_en="AI stands for Artificial Intelligence.")


# ---------------------------
# Model Tests
# ---------------------------

@pytest.mark.django_db
def test_faq_creation():
    """
    Test if an FAQ object is created successfully.
    """
    faq = FAQ.objects.create(
        question_en="What is pytest?",
        answer_en="pytest is a testing framework for Python."
    )
    assert faq.id is not None
    assert faq.question_en == "What is pytest?"
    assert faq.answer_en == "pytest is a testing framework for Python."

@pytest.mark.django_db
def test_get_translated_question(faq_instance):
    """
    Test that get_translated_question() correctly returns translations.
    """
    assert faq_instance.get_translated_question("hi") == faq_instance.question_hi
    assert faq_instance.get_translated_question("bn") == faq_instance.question_bn
    assert faq_instance.get_translated_question("fr") == faq_instance.question_en  # Fallback to English


# ---------------------------
# API Tests
# ---------------------------

@pytest.mark.django_db
def test_get_all_faqs(api_client, multiple_faqs):
    """
    Test retrieving all FAQs in the default language.
    """
    list_url = reverse('faq-list')
    response = api_client.get(list_url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2  # We created 2 FAQs


@pytest.mark.django_db
def test_get_single_faq(api_client, faq_instance):
    """
    Test retrieving a single FAQ by its ID.
    """
    detail_url = reverse('faq-detail', kwargs={'pk': faq_instance.id})
    response = api_client.get(detail_url)
    print("\nAPI Response JSON:", response.json())  # Debugging line
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["question_en"] == faq_instance.question_en  # This line is failing


@pytest.mark.django_db
def test_get_faq_with_invalid_language(api_client, faq_instance):
    """
    Test handling of an unsupported language.
    """
    list_url = reverse('faq-list')
    response = api_client.get(f"{list_url}?lang=xyz")  # Invalid language code
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['question'] == faq_instance.question_en  # Should fall back to English


@pytest.mark.django_db
def test_update_faq_invalid_data(api_client, faq_instance):
    """
    Test updating an FAQ with missing required fields.
    """
    detail_url = reverse('faq-detail', kwargs={'pk': faq_instance.id})
    update_data = {"question_en": ""}  # Empty question should be rejected
    response = api_client.patch(detail_url, data=update_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_update_faq_patch(api_client, faq_instance):
    """
    Test updating an FAQ using the PATCH method.
    """
    detail_url = reverse('faq-detail', kwargs={'pk': faq_instance.id})
    update_data = {"answer_en": "Updated answer using PATCH."}
    response = api_client.patch(detail_url, data=update_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    faq_instance.refresh_from_db()
    assert faq_instance.answer_en == update_data["answer_en"]


@pytest.mark.django_db
def test_update_faq_put(api_client, faq_instance):
    """
    Test updating an FAQ using the PUT method (full update).
    """
    detail_url = reverse('faq-detail', kwargs={'pk': faq_instance.id})
    update_data = {
        "question_en": "What is Django updated?",
        "answer_en": "Django is updated with new features."
    }
    response = api_client.put(detail_url, data=update_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    faq_instance.refresh_from_db()
    assert faq_instance.question_en == update_data["question_en"]
    assert faq_instance.answer_en == update_data["answer_en"]


@pytest.mark.django_db
def test_delete_faq(api_client, faq_instance):
    """
    Test deleting an FAQ by ID.
    """
    detail_url = reverse('faq-detail', kwargs={'pk': faq_instance.id})
    response = api_client.delete(detail_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not FAQ.objects.filter(pk=faq_instance.id).exists()


@pytest.mark.django_db
def test_delete_nonexistent_faq(api_client):
    """
    Test deleting a non-existent FAQ should return 404.
    """
    detail_url = reverse('faq-detail', kwargs={'pk': 99999})  # Non-existent ID
    response = api_client.delete(detail_url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
