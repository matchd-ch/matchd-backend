from db.seed.attachment import Attachment
from db.seed.company import Company
from db.seed.employee import Employee
from db.seed.faq import FAQ
from db.seed.job_posting import JobPosting
from db.seed.student import Student
from db.seed.user import User


class Seed:
    users = User()
    employees = Employee()
    students = Student()
    companies = Company()
    attachments = Attachment()
    job_postings = JobPosting()
    faq = FAQ()

    def run(self, data):
        user = self.users.create_or_update(data)
        self.employees.create_or_update(data.get('employee'), user=user)
        student = self.students.create_or_update(data.get('student'), user=user)
        company = self.companies.create_or_update(data.get('company'), user=user)
        if company is not None:
            self.attachments.create_or_update(data, user=user, company=company)
            self.job_postings.create_or_update(data, company=company, user=user)
            self.faq.create_or_update(data, company=company)
        if student is not None:
            self.attachments.create_or_update(data, student=student)

    def random_student(self, index):
        return self.users.ranxdom(index=index)

    def random_company(self, index, company_type):
        return self.companies.random(index=index, company_type=company_type)
