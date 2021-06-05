from datetime import datetime
import pytest

from db.models import ProjectPosting


@pytest.fixture
def project_posting_objects(company_object, project_type_objects, topic_objects):
    project_posting_1 = ProjectPosting.objects.create(id=1, company=company_object, slug='project-1',
                                                      project_type=project_type_objects[0], topic=topic_objects[0])
    project_posting_2 = ProjectPosting.objects.create(id=2, company=company_object, slug='project-2',
                                                      project_type=project_type_objects[0], topic=topic_objects[0])
    project_posting_3 = ProjectPosting.objects.create(id=3, company=company_object, slug='project-3',
                                                      project_type=project_type_objects[0], topic=topic_objects[0])
    return [
        project_posting_1,
        project_posting_2,
        project_posting_3,
    ]


@pytest.fixture
def project_posting_object(project_posting_objects):
    return project_posting_objects[0]


def project_posting_mutation(step):
    step = str(step)
    return '''
    mutation ProjectPostingMutation($step%s: ProjectPostingInputStep%s!) {
      projectPostingStep%s(step%s: $step%s) {
        success,
        errors,
        slug,
        projectPostingId
      }
    }
    ''' % (step, step, step, step, step)


@pytest.fixture
def project_posting_step_1(execute):
    def closure(user, title, description, additional_information, project_from_date, website, topic, project_type,
                keywords):
        return execute(project_posting_mutation(1), variables={
            'step1': {
                'title': title,
                'description': description,
                'additionalInformation': additional_information,
                'projectFromDate': project_from_date,
                'website': website,
                'topic': None if topic is None else {'id': topic.id},
                'projectType': None if project_type is None else {'id': project_type.id},
                'keywords': [{'id': obj.id} for obj in keywords]
            }
        }, **{'user': user})
    return closure


@pytest.fixture
def project_posting_step_2(execute):
    def closure(user, project_posting_id, state, employee):
        return execute(project_posting_mutation(2), variables={
            'step2': {
                'id': project_posting_id,
                'state': state,
                'employee': None if employee is None else {'id': employee.id}
            }
        }, **{'user': user})
    return closure
