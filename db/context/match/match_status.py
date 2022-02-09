from db.models.match import Match
from db.models.profile_type import ProfileType
from db.models.user import User


class MatchStatus:

    @staticmethod
    def get(user: User, **kwargs):
        status = None

        if user.type in ProfileType.valid_student_types():
            try:
                status = Match.objects.get(student=user.student, **kwargs)
            except Match.DoesNotExist:
                pass
        if user.type in ProfileType.valid_company_types():
            try:
                status = Match.objects.get(company=user.company, **kwargs)
            except Match.DoesNotExist:
                pass

        return status
