import graphene
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required
from django.utils.translation import gettext as _

from api.exceptions import MutationException
from api.schema.hobby import HobbyInputType
from api.schema.skill import SkillInputType
from db.forms import HobbyForm
from db.forms.profile.student import StudentProfileFormStep4
from db.models import UserType, Hobby, Skill


class StudentProfileInputStep4(graphene.InputObjectType):
    skills = graphene.List(SkillInputType, description=_('Skills'), required=False)
    hobbies = graphene.List(HobbyInputType, description=_('Hobbies'), required=False)
    # distinctions = graphene.String(description=_('Distinctions'), required=False)
    # online_projects = graphene.String(description=_('Online_Projects'), required=False)
    # languages = graphene.String(description=_('Languages'), required=True)
    # languagesLevel = graphene.String(description=_('LanguagesLevel'), required=True)


class StudentProfileStep4(Output, graphene.Mutation):
    class Arguments:
        step4 = StudentProfileInputStep4(description=_('Profile Input Step 4 is required.'))

    class Meta:
        description = _('Updates the profile of a student')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        errors = {}
        user = info.context.user
        if user.type not in UserType.valid_student_types():
            errors.update(generic_error_dict('type', _('You are not a student'), 'invalid_type'))
            return StudentProfileStep4(success=False, errors=errors)

        profile_data = data.get('step4', None)

        profile = user.student
        profile_form = StudentProfileFormStep4(profile_data)
        profile_form.full_clean()
        skills_to_save = None
        if profile_form.is_valid():
            profile_data_for_update = profile_form.cleaned_data

            skills_to_save = profile_data_for_update.get('skills')

            # profile.distinctions = profile_data_for_update.get('distinctions')
            # profile.online_projects = profile_data_for_update.get('online_projects')
            # profile.languages = profile_data_for_update.get('languages')

            # update step only if the user has step 1
            # TODO
            # if user.profile_step == 4:
            #     user.profile_step = 5
        else:
            errors.update(profile_form.errors.get_json_data())
        valid_hobby_forms = []
        if 'hobbies' in profile_data:
            for hobby in profile_data['hobbies']:
                hobby['student'] = profile.id
                if 'id' not in hobby:
                    hobby_form = HobbyForm(hobby)
                    hobby_form.full_clean()
                    if hobby_form.is_valid():
                        valid_hobby_forms.append(hobby_form)
                    else:
                        hobby_errors = hobby_form.errors.get_json_data()
                        if not silent_fail(hobby_errors):
                            errors.update(hobby_form.errors.get_json_data())
        if errors:
            return StudentProfileStep4(success=False, errors=errors)
        for form in valid_hobby_forms:
            form.save()
        # user.save()
        # profile.save()
        profile.skills.set(skills_to_save)
        return StudentProfileStep4(success=True, errors=None)


def silent_fail(errors):
    if '__all__' in errors:
        if len(errors['__all__']) == 1 and 'code' in errors['__all__'][0]:
            if errors['__all__'][0]['code'] == 'unique_together':
                return True
    return False


def generic_error_dict(key, message, code):
    return {
        key: [
            {
                'message': message,
                'code': code
            }
        ]
    }


def validation_error_to_dict(error, key):
    return generic_error_dict(key, error.message, error.code)


class StudentProfileMutation(graphene.ObjectType):
    student_profile_step4 = StudentProfileStep4.Field()
