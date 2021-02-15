from django.core.exceptions import ValidationError


class StudentProfileFormStepValidator:

    def __init__(self, min_required_step=1):
        self.min_required_step = min_required_step

    def validate(self, user):
        if user.profile_step < self.min_required_step:
            raise ValidationError(code='invalid_step', message='You must first complete the previous steps.')
