from django.conf import settings
from rest_framework.response import Response
from django.core.cache import cache
from rest_framework import viewsets
from .models import FAQ
from .serializers import FAQSerializer
from googletrans import Translator, LANGUAGES

translator = Translator()

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def list(self, request):
        lang = request.query_params.get('lang', 'en')
        if lang not in LANGUAGES:
            lang = 'en'

        queryset = self.get_queryset()
        data = []

        for faq in queryset:
            cache_key = f'faq_{faq.id}_{lang}'
            translated_answer = cache.get(cache_key)
            if not translated_answer:
                answer_source = faq.answer_en
                if lang != 'en':
                    try:
                        translated_answer = translator.translate(answer_source, dest=lang).text
                    except Exception:
                        translated_answer = answer_source
                    cache.set(cache_key, translated_answer, 3600)
                else:
                    translated_answer = answer_source

            data.append({
                'id': faq.id,
                'question': faq.get_translated_question(lang),
                'answer': translated_answer
            })

        return Response(data)

    def perform_update(self, serializer):
        faq = serializer.save()
        # Invalidate cache for all supported languages
        supported_languages = [lang[0] for lang in settings.LANGUAGES]
        for lang in supported_languages:
            cache_key = f'faq_{faq.id}_{lang}'
            cache.delete(cache_key)
