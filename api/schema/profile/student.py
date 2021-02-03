import graphene
from graphql_auth.bases import Output
from django.utils.translation import gettext_lazy as _
from graphql_jwt.decorators import login_required

from db.forms.profile import StudentProfileStep6Form


class StudentProfileStep6Input(graphene.InputObjectType):
    state = graphene.String(description=_('State'), required=True)


class StudentProfileStep6(Output, graphene.Mutation):

    class Arguments:
        step6 = StudentProfileStep6Input(description=_('Profile Input Step 6 is required.'))

    class Meta:
        description = _('Updates the state of a student')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        errors = {}

        user = info.context.user

        if user.profile_step < 6:
            errors.update({
                'profile_step': [
                    {
                        'message': 'You must first complete the previous steps.',
                        'code': 'invalid_step'
                    }
                ]
            }
            )
            return StudentProfileStep6(success=False, errors=errors)

        profile_data = data.get('step6', None)
        profile_form = StudentProfileStep6Form(profile_data)
        profile_form.full_clean()
        if profile_form.is_valid():
            user.state = profile_data.get('state')
            if user.profile_step == 6:
                user.profile_step = 7
            user.save()
        else:
            errors.update(profile_form.errors.get_json_data())

        if errors:
            return StudentProfileStep6(success=False, errors=errors)

        return StudentProfileStep6(success=True, errors=None)


class StudentProfileMutation(graphene.ObjectType):
    student_profile_step6 = StudentProfileStep6.Field()
