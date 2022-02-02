from django.core.exceptions import ValidationError


class ProfileFormStepValidator:

    def __init__(self, min_required_step=1):
        self.min_required_step = min_required_step

    def validate(self, company_or_student):
        if company_or_student.profile_step < self.min_required_step:
            raise ValidationError(code='invalid_step',
                                  message='You must first complete the previous steps.')
