from rest_framework import viewsets
from rest_framework.response import Response
from django.core.cache import cache
from .models import FAQ
from .serializers import FAQSerializer
from googletrans import Translator

translator = Translator()

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def list(self, request):
        lang = request.query_params.get('lang', 'en')  # e.g., ?lang=hi
        queryset = self.get_queryset()
        data = []
        for faq in queryset:
            # Check cache first
            cache_key = f'faq_{faq.id}_{lang}'
            translated_answer = cache.get(cache_key)
            if not translated_answer:
                translated_answer = translator.translate(faq.answer_en, dest=lang).text
                cache.set(cache_key, translated_answer, 3600)  # Cache for 1 hour
            data.append({
                'question': faq.get_translated_question(lang),
                'answer': translated_answer
            })
        return Response(data)