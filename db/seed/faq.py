from db.seed import random
from db.seed.base import BaseSeed
from db.models import FAQ as FAQModel, FAQCategory, Company


# pylint: disable=W0612
class FAQ(BaseSeed):

    def create_or_update(self, data, *args, **kwargs):

        if data is None:
            return
        faqs_data = data.get('company').get('faqs')
        if faqs_data is None or len(faqs_data) == 0:
            self.createRandomFAQ(kwargs.get('company'))
            self.createRandomFAQ(kwargs.get('company'))
            self.createRandomFAQ(kwargs.get('company'))
        else:
            for faq_data in faqs_data:
                # faq, created = FAQModel.objects.get_or_create(
                #     question=faq_data.get('question'),
                #     answer=faq_data.get('answer'),
                #     company=kwargs.get('company'),
                #     category=FAQCategory.objects.get(id=faq_data.get('category')))
                # faq.save()
                self.createFAQ(faq_data,kwargs.get('company'))

    def random(self, *args, **kwargs):
        pass

    def createFAQ(self, data, company):
        faq = FAQModel()
        faq.category =FAQCategory.objects.get(id=data.get('category'))
        faq.question = data.get('question')
        faq.answer = data.get('answer')
        faq.company = company
        faq.save()

    def createRandomFAQ(self,company):
        faq = FAQModel()
        _question, _answer = self.rand.question_and_answer()
        _category = self.rand.faq_category()
        faq.category = FAQCategory.objects.get(id=_category)
        faq.question = _question
        faq.answer = _answer
        faq.company = company
        faq.save()