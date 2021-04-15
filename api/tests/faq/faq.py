import json

from django.contrib.auth import get_user_model
from graphene_django.utils import GraphQLTestCase
from graphql_auth.models import UserStatus
from api.schema import schema
from db.models import Employee, Company, Student, ProfileType, FAQCategory, FAQ


# pylint:disable=R0913
# pylint:disable=R0902
# pylint:disable=R0904
class FAQGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    query_add_faq = '''
    mutation addFaq($addFAQ: AddFAQInput!) {
        addFaq(addFaq: $addFAQ) {
            success,
            errors
        }
    }
    '''

    variables_add_faq_base = {
        "addFAQ": {
            "category": {"id": 1},
            "title": "FAQ Title",
            "question": "FAQ Question",
            "answer": "FAQ Answer"
        }
    }

    variables_add_faq_invalid = {
        "addFAQ": {
            "category": {"id": 1337},
            "title": "",
            "question": "",
            "answer": ""
        }
    }

    variables_add_faq_invalid_to0_long = {
        "addFAQ": {
            "category": {"id": 1},
            "title": "test" * 1000,
            "question": "test" * 1000,
            "answer": "test" * 1000
        }
    }

    query_update_faq = '''
    mutation UpdateFAQ($updateFAQ: UpdateFAQInput!) {
        updateFaq(updateFaq: $updateFAQ) {
            success,
            errors
        }
    }
    '''

    variables_update_faq_base = {
        "updateFAQ": {
            "faqId": 1,
            "category": {"id": 2},
            "title": "New Title",
            "question": "New Question",
            "answer": "New Answer"
        }
    }

    variables_update_faq_invalid = {
        "updateFAQ": {
            "faqId": 1,
            "category": {"id": 1337},
            "title": "",
            "question": "",
            "answer": ""
        }
    }

    variables_update_faq_invalid_faq_id = {
        "updateFAQ": {
            "faqId": 1337,
            "category": {"id": 1},
            "title": "New Title",
            "question": "New Question",
            "answer": "New Answer"
        }
    }

    query_delete_faq = '''
        mutation DeleteFAQ($deleteFaq: DeleteFAQInput!) {
            deleteFaq(deleteFaq: $deleteFaq) {
                success,
                errors
            }
        }
        '''

    variables_delete_faq_base = {
        "deleteFaq": {
            "faqId": 1,
        }
    }

    variables_delete_faq_invalid = {
        "deleteFaq": {
            "faqId": 1337,
        }
    }

    def setUp(self):
        self.company = Company.objects.create(id=1, uid='CHE-999.999.999', name='Doe Unlimited', zip='0000',
                                              city='DoeCity', slug='doe-unlimited', profile_step=1,
                                              type=ProfileType.COMPANY)

        self.different_company = Company.objects.create(id=2, uid='CHE-000.000.000', name='Doe Company', zip='9999',
                                                        city='DoeCity', slug='doe-company', profile_step=1,
                                                        type=ProfileType.COMPANY)
        self.company.save()
        self.user = get_user_model().objects.create(
            username='john@doe.com',
            email='john@doe.com',
            type='company',
            first_name='Johnny',
            last_name='Test',
            company=self.company
        )
        self.user.set_password('asdf1234$')
        self.user.save()

        user_status = UserStatus.objects.get(user=self.user)
        user_status.verified = True
        user_status.save()

        self.user_same_company = get_user_model().objects.create(
            username='max@doe.com',
            email='max@doe.com',
            type='company',
            first_name='Max',
            last_name='Test',
            company=self.company
        )
        self.user_same_company.set_password('asdf1234$')
        self.user_same_company.save()

        user_status_same_company = UserStatus.objects.get(user=self.user_same_company)
        user_status_same_company.verified = True
        user_status_same_company.save()

        self.user_different_company = get_user_model().objects.create(
            username='edna@doe.com',
            email='edna@doe.com',
            type='company',
            first_name='Edna',
            last_name='Test',
            company=self.different_company
        )
        self.user_different_company.set_password('asdf1234$')
        self.user_different_company.save()

        user_status_different_company = UserStatus.objects.get(user=self.user_different_company)
        user_status_different_company.verified = True
        user_status_different_company.save()

        self.employee = Employee.objects.create(
            role='Trainer',
            user=self.user
        )
        self.employee.save()

        self.student = get_user_model().objects.create(
            username='jane@doe.com',
            email='jane@doe.com',
            type='student'
        )
        self.student.set_password('asdf1234$')
        self.student.save()

        self.student_profile = Student.objects.create(user=self.student, mobile='+41771234568')

        user_status = UserStatus.objects.get(user=self.student)
        user_status.verified = True
        user_status.save()

        self.faq_category_id_1 = FAQCategory.objects.create(id=1, name="Category 1")
        self.faq_category_id_2 = FAQCategory.objects.create(id=2, name="Category 2")
        self.faq_id_1 = FAQ.objects.create(id=1, title='Old Title', question='Old Question', answer='Old Answer',
                                           category=self.faq_category_id_1, company=self.company)

    def _test_and_get_faq_response_content(self, query, variables, login, error, success=True):
        self._login(login)
        response = self.query(query, variables=variables)

        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        if success:
            self.assertTrue(content['data'].get(error).get('success'))
            self.assertIsNone(content['data'].get(error).get('errors'))
        else:
            self.assertFalse(content['data'].get(error).get('success'))
            self.assertIsNotNone(content['data'].get(error).get('errors'))
        return content

    def _test_with_invalid_data(self, query, variables, login, error_key, expected_errors):
        self._login(login)

        response = self.query(query, variables=variables)
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        errors = content['data'].get(error_key).get('errors')
        for expected_error in expected_errors:
            self.assertIn(expected_error, errors)

    def _test_with_errors(self, query, variables, login):
        self._login(login)

        response = self.query(query, variables=variables)
        self.assertResponseHasErrors(response)

    def _test_and_get_faq_response_without_login(self, query, variables, error):
        response = self.query(query, variables=variables)
        self.assertResponseHasErrors(response)

    def _login(self, username):
        response = self.query(
            '''
            mutation TokenAuth {
                tokenAuth(username: "%s", password: "asdf1234$") {
                    success,
                    errors,
                    token
                }
            }
            ''' % username
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertTrue(content['data'].get('tokenAuth').get('success'))
        self.assertIsNotNone(content['data'].get('tokenAuth').get('token'))

    def _faq_query(self, slug):
        response = self.query(
            '''
            query companyFaqs{
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
        )

        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        first_category = content['data'].get('companyFaqs')[0]
        second_category = content['data'].get('companyFaqs')[1]
        first_category_first_faq = first_category.get('faqs')[0]
        first_category_second_faq = first_category.get('faqs')[1]
        second_category_first_faq = second_category.get('faqs')[0]
        self.assertEqual(first_category.get('name'), 'Category 1')
        self.assertEqual(first_category_first_faq.get('id'), '1')
        self.assertEqual(first_category_first_faq.get('title'), 'Old Title')
        self.assertEqual(first_category_first_faq.get('question'), 'Old Question')
        self.assertEqual(first_category_first_faq.get('answer'), 'Old Answer')

        self.assertEqual(first_category.get('name'), 'Category 1')
        self.assertEqual(first_category_second_faq.get('id'), '2')
        self.assertEqual(first_category_second_faq.get('title'), 'second Title')
        self.assertEqual(first_category_second_faq.get('question'), 'second Question')
        self.assertEqual(first_category_second_faq.get('answer'), 'second Answer')

        self.assertEqual(second_category.get('name'), 'Category 2')
        self.assertEqual(second_category_first_faq.get('id'), '3')
        self.assertEqual(second_category_first_faq.get('title'), 'third Title')
        self.assertEqual(second_category_first_faq.get('question'), 'third Question')
        self.assertEqual(second_category_first_faq.get('answer'), 'third Answer')
        return content

    def _faq_query_with_errors(self, slug):
        response = self.query(
            '''
            query companyFaqs{
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
        )

        self.assertResponseHasErrors(response)

    def test_add_faq_valid_base_company(self):
        self._test_and_get_faq_response_content(self.query_add_faq, self.variables_add_faq_base, 'john@doe.com',
                                                'addFaq')
        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company
        faq = company.faqs.all()[1]
        self.assertEqual(faq.category.id, 1)
        self.assertEqual(faq.title, 'FAQ Title')
        self.assertEqual(faq.question, 'FAQ Question')
        self.assertEqual(faq.answer, 'FAQ Answer')

    def test_add_faq_too_long_variables(self):
        self._test_with_invalid_data(self.query_add_faq, self.variables_add_faq_invalid, 'john@doe.com', 'addFaq',
                                     ['title', 'question', 'answer'])
        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company
        self.assertEqual(len(company.faqs.all()), 1)

    def test_update_faq_valid_base_company(self):
        self._test_and_get_faq_response_content(self.query_update_faq, self.variables_update_faq_base, 'john@doe.com',
                                                'updateFaq')
        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company
        faq = company.faqs.all()[0]
        self.assertEqual(faq.category.id, 2)
        self.assertEqual(faq.title, 'New Title')
        self.assertEqual(faq.question, 'New Question')
        self.assertEqual(faq.answer, 'New Answer')

    def test_update_faq_valid_base_company_different_user_same_company(self):
        self._test_and_get_faq_response_content(self.query_update_faq, self.variables_update_faq_base, 'max@doe.com',
                                                'updateFaq')
        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company
        faq = company.faqs.all()[0]
        self.assertEqual(faq.category.id, 2)
        self.assertEqual(faq.title, 'New Title')
        self.assertEqual(faq.question, 'New Question')
        self.assertEqual(faq.answer, 'New Answer')

    def test_update_faq_valid_base_company_different_user_different_company(self):
        self._test_with_errors(self.query_update_faq, self.variables_update_faq_base, 'edna@doe.com')
        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company
        faq = company.faqs.all()[0]
        self.assertEqual(faq.category.id, 1)
        self.assertEqual(faq.title, 'Old Title')
        self.assertEqual(faq.question, 'Old Question')
        self.assertEqual(faq.answer, 'Old Answer')

    def test_add_faq_invalid_data(self):
        self._test_with_invalid_data(self.query_add_faq, self.variables_add_faq_invalid, 'john@doe.com', 'addFaq',
                                     ['category', 'title', 'question', 'answer'])

    def test_update_faq_invalid_data(self):
        self._test_with_invalid_data(self.query_update_faq, self.variables_update_faq_invalid, 'john@doe.com',
                                     'updateFaq', ['category', 'title', 'question', 'answer'])

    def test_delete_faq_valid_base_company(self):
        self._test_and_get_faq_response_content(self.query_delete_faq, self.variables_delete_faq_base, 'john@doe.com',
                                                'deleteFaq')
        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company
        self.assertEqual(len(company.faqs.all()), 0)

    def test_delete_faq_valid_base_company_different_user_same_company(self):
        self._test_and_get_faq_response_content(self.query_delete_faq, self.variables_delete_faq_base, 'max@doe.com',
                                                'deleteFaq')
        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company
        self.assertEqual(len(company.faqs.all()), 0)

    def test_delete_faq_valid_base_company_different_user_different_company(self):
        self._test_with_errors(self.query_update_faq, self.variables_update_faq_base, 'edna@doe.com')
        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company
        self.assertEqual(len(company.faqs.all()), 1)

    def test_delete_faq_invalid_data(self):
        self._test_with_errors(self.query_delete_faq, self.variables_delete_faq_invalid, 'john@doe.com')
        self._test_with_errors(self.query_delete_faq, self.variables_delete_faq_invalid, 'john@doe.com')
        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company
        self.assertEqual(len(company.faqs.all()), 1)

    def test_add_faq_valid_base_student(self):
        self._test_and_get_faq_response_content(self.query_add_faq, self.variables_add_faq_base, 'jane@doe.com',
                                                'addFaq', False)
        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company
        self.assertEqual(len(company.faqs.all()), 1)

    def test_add_faq_valid_base_without_login(self):
        self._test_and_get_faq_response_without_login(self.query_add_faq, self.variables_add_faq_base, 'addFaq')
        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company
        self.assertEqual(len(company.faqs.all()), 1)

    def test_edit_faq_valid_base_without_login(self):
        self._test_and_get_faq_response_without_login(self.query_update_faq, self.variables_update_faq_base,
                                                      'updateFaq')
        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company
        faq = company.faqs.all()[0]
        self.assertEqual(faq.category.id, 1)
        self.assertEqual(faq.title, 'Old Title')
        self.assertEqual(faq.question, 'Old Question')
        self.assertEqual(faq.answer, 'Old Answer')

    def test_delete_faq_valid_base_without_login(self):
        self._test_and_get_faq_response_without_login(self.query_delete_faq, self.variables_delete_faq_base,
                                                      'deleteFaq')
        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company
        self.assertEqual(len(company.faqs.all()), 1)

    def test_faq_query_as_company(self):
        FAQ.objects.create(id=2, title='second Title', question='second Question', answer='second Answer',
                           category=self.faq_category_id_1, company=self.company)

        FAQ.objects.create(id=3, title='third Title', question='third Question', answer='third Answer',
                           category=self.faq_category_id_2, company=self.company)
        self._login('john@doe.com')
        self._faq_query('doe-unlimited')

    def test_faq_query_as_student(self):
        FAQ.objects.create(id=2, title='second Title', question='second Question', answer='second Answer',
                           category=self.faq_category_id_1, company=self.company)

        FAQ.objects.create(id=3, title='third Title', question='third Question', answer='third Answer',
                           category=self.faq_category_id_2, company=self.company)
        self._login('jane@doe.com')
        self._faq_query('doe-unlimited')

    def test_faq_query_without_login(self):
        self._faq_query_with_errors('doe-unlimited')

    def test_faq_query_as_company_with_wrong_slug(self):
        self._login('john@doe.com')
        self._faq_query_with_errors('Not-a-valid-slug')

    def test_faq_query_as_student_with_wrong_slug(self):
        self._login('jane@doe.com')
        self._faq_query_with_errors('Not-a-valid-slug')

    def test_faq_query_without_login_with_wrong_slug(self):
        self._faq_query_with_errors('Not-a-valid-slug')
