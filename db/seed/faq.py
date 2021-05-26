from db.seed.base import BaseSeed
from db.models import FAQ as FAQModel, FAQCategory


# pylint: disable=W0612
class FAQ(BaseSeed):

    def create_or_update(self, data, *args, **kwargs):

        if data is None:
            return
        faqs_data = data.get('company').get('faqs')
        if faqs_data is None:
            return
        for faq_data in faqs_data:
            faq = FAQModel()
            faq.category = FAQCategory.objects.get(id=faq_data.get('category'))
            faq.question = faq_data.get('question')
            faq.answer = faq_data.get('answer')
            faq.company = kwargs.get('company')
            faq.save()

    def random(self, *args, **kwargs):
        pass
