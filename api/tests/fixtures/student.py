import pytest

from db.helper.forms import convert_date
from db.models import Student, ProfileType, ProfileState, Hobby, OnlineProject

# pylint: disable=C0209


def student_query(slug):
    return '''
    query {
      student(slug: "%s") {
        matchStatus {
          initiator
          confirmed
        }
        firstName
        lastName
        email
        slug
        mobile
        street
        zip
        city
        dateOfBirth
        nickname
        schoolName
        fieldOfStudy
        graduation
        branch {
          id
          name
        }
        jobType {
          id
          name
        }
        jobFromDate
        jobToDate
        skills {
          edges {
            node {
              id
              name
            }
          }
        }
        distinction
        state
        profileStep
        softSkills {
          edges {
            node {
              id
            }
          }
        }
        culturalFits {
          edges {
            node {
              id
            }
          }
        }
        slug
        hobbies {
          name
        }
        onlineProjects {
          url
        }
        languages {
            edges {
                node {
                    language {
                        name
                    }
                    languageLevel {
                        level
                    }
                }
            }
        }
        projectPostings {
          slug
        }
      }
    }
    ''' % slug


def student_with_job_posting_query(slug, job_posting_id):
    return '''
    query {
      student(slug: "%s", jobPostingId: %i) {
        matchStatus {
          initiator
          confirmed
        }
        firstName
        lastName
        email
        slug
        mobile
        street
        zip
        city
        dateOfBirth
        nickname
        schoolName
        fieldOfStudy
        graduation
        branch {
          id
          name
        }
        jobType {
          id
          name
        }
        jobFromDate
        jobToDate
        skills {
          edges {
            node {
              id
              name
            }
          }
        }
        distinction
        state
        profileStep
        softSkills {
          edges {
            node {
              id
            }
          }
        }
        culturalFits {
          edges {
            node {
              id
            }
          }
        }
        slug
        hobbies {
          name
        }
        onlineProjects {
          url
        }
        languages {
            edges {
                node {
                    language {
                        name
                    }
                    languageLevel {
                        level
                    }
                }
            }
        }
        projectPostings {
          slug
        }
      }
    }
    ''' % (slug, job_posting_id)


@pytest.fixture
def query_student(execute):
    def closure(user, slug, job_posting_id=None):
        if job_posting_id is None:
            return execute(student_query(slug), **{'user': user})
        return execute(student_with_job_posting_query(slug, job_posting_id), **{'user': user})
    return closure


@pytest.fixture
def user_student(get_user, default_password):
    username = 'student@matchd.test'
    user = get_user(username, default_password, True, ProfileType.STUDENT)
    Student.objects.create(user=user)
    return user


# pylint: disable=R0913
# pylint: disable=W0621
@pytest.fixture
def user_student_full_profile(user_student, branch_objects, job_type_objects, skill_objects, soft_skill_objects,
                              cultural_fit_objects):
    user_student.first_name = 'John'
    user_student.last_name = 'Doe'
    user_student.save()
    user_student.student.branch = branch_objects[0]
    user_student.student.job_type = job_type_objects[0]
    user_student.student.profile_step = 3
    user_student.student.state = ProfileState.ANONYMOUS
    user_student.student.mobile = '+41711234567'
    user_student.student.zip = '1337'
    user_student.student.city = 'nowhere'
    user_student.student.street = 'street 1337'
    user_student.student.date_of_birth = convert_date('01.03.1337')
    user_student.student.nickname = 'nickname'
    user_student.student.slug = 'nickname'
    user_student.student.school_name = 'school name'
    user_student.student.field_of_study = 'field of study'
    user_student.student.graduation = convert_date('03.1337', '%m.%Y')
    user_student.student.distinction = 'distinction'
    user_student.student.skills.set(skill_objects)
    hobbies = [
        Hobby.objects.create(id=1, name='hobby 1', student=user_student.student),
        Hobby.objects.create(id=2, name='hobby 2', student=user_student.student)
    ]
    user_student.student.hobbies.set(hobbies)
    online_projects = [
        OnlineProject.objects.create(id=1, url='https://www.project1.lo', student=user_student.student),
        OnlineProject.objects.create(id=2, url='https://www.project2.lo', student=user_student.student)
    ]
    user_student.student.online_projects.set(online_projects)
    user_student.student.soft_skills.set(soft_skill_objects[:6])
    user_student.student.cultural_fits.set(cultural_fit_objects[:6])
    user_student.student.save()
    return user_student


@pytest.fixture
def user_student_2(get_user, default_password):
    username = 'student2@matchd.test'
    user = get_user(username, default_password, True, ProfileType.STUDENT)
    Student.objects.get_or_create(user=user)
    return user


@pytest.fixture
def user_student_not_verified(get_user, default_password):
    username = 'student@matchd.test'
    user = get_user(username, default_password, False, ProfileType.STUDENT)
    Student.objects.get_or_create(user=user)
    return user
