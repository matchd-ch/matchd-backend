import pytest

from api.tests.fixtures import faq_category_objects, company_objects, company_object
from db.models import FAQ


def faqs_query(slug):
    return '''
    query {
        companyFaqs(slug: "%s"){
            name
            faqs{
                id
                title
                question
                answer
            }
        }
    } 
    ''' % slug


def add_faq_mutation():
    return '''
    mutation addFaq($addFAQ: AddFAQInput!) {
        addFaq(addFaq: $addFAQ) {
            success,
            errors
        }
    }
    '''


def update_faq_mutation():
    return '''
    mutation updateFaq($updateFAQ: UpdateFAQInput!) {
        updateFaq(updateFaq: $updateFAQ) {
            success,
            errors
        }
    }
    '''


@pytest.fixture
def faq_objects(faq_category_objects, company_object):
    return [
        FAQ.objects.create(id=1, title='Old Title', question='Old Question', answer='Old Answer',
                           category=faq_category_objects[0], company=company_object)
    ]


@pytest.fixture
def query_faqs(execute):
    def closure(user, slug):
        return execute(faqs_query(slug), **{'user': user})

    return closure


@pytest.fixture
def faq_add_faq(execute):
    def closure(user, category_id, title, question, answer):
        return execute(add_faq_mutation(), variables={
            'addFAQ': {
                'category': {'id': category_id},
                'title': title,
                'question': question,
                'answer': answer
            }
        }, **{'user': user})

    return closure


@pytest.fixture
def faq_update_faq(execute):
    def closure(user, faq_id, category_id, title, question, answer):
        return execute(update_faq_mutation(), variables={
            'updateFAQ': {
                'faqId': faq_id,
                'category': {'id': category_id},
                'title': title,
                'question': question,
                'answer': answer
            }
        }, **{'user': user})

    return closure
