import pytest

from db.models.branch import Branch
from db.models.job_type import JobType
from db.models import Student
from db.models.user import User


@pytest.mark.django_db
def test_create_student(student_valid_args):
    student = Student.objects.create(**student_valid_args)

    assert isinstance(student, Student)


@pytest.mark.django_db
def test_get_student(student_valid_args):
    student = Student.objects.create(**student_valid_args)
    student = Student.objects.get(id=student.id)

    assert isinstance(student, Student)
    assert isinstance(student.user, User)
    assert isinstance(student.branch, Branch)
    assert isinstance(student.job_type, JobType)

    assert student.user == student_valid_args.get('user')
    assert student.user.first_name == student_valid_args.get('user').first_name
    assert student.mobile == student_valid_args.get('mobile')
    assert student.street == student_valid_args.get('street')
    assert student.zip == student_valid_args.get('zip')
    assert student.city == student_valid_args.get('city')
    assert student.date_of_birth == student_valid_args.get('date_of_birth')
    assert student.nickname == student_valid_args.get('nickname')
    assert student.school_name == student_valid_args.get('school_name')
    assert student.field_of_study == student_valid_args.get('field_of_study')
    assert student.graduation == student_valid_args.get('graduation')
    assert student.job_type == student_valid_args.get('job_type')
    assert student.job_from_date == student_valid_args.get('job_from_date')
    assert student.job_to_date == student_valid_args.get('job_to_date')
    assert student.distinction == student_valid_args.get('distinction')
    assert student.state == student_valid_args.get('state')
    assert student.slug == student_valid_args.get('slug')


@pytest.mark.django_db
def test_update_student(student_valid_args):
    mobile = '0279929334'
    student = Student.objects.create(**student_valid_args)
    Student.objects.filter(id=student.id).update(mobile=mobile)
    student.refresh_from_db()

    assert isinstance(student, Student)
    assert isinstance(student.mobile, str)

    assert student.mobile == mobile


@pytest.mark.django_db
def test_delete_student(student_valid_args):
    student = Student.objects.create(**student_valid_args)
    number_of_deletions, _ = student.delete()

    assert number_of_deletions == 1
