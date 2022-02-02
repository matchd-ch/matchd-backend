from django.core.exceptions import ValidationError


class JobPostingFormStepValidator:

    def __init__(self, min_required_step=1):
        self.min_required_step = min_required_step

    def validate(self, job_posting):
        if job_posting.form_step < self.min_required_step:
            raise ValidationError(code='invalid_step',
                                  message='You must first complete the previous steps.')
