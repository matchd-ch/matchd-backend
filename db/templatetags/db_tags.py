from django import template

from db.models import ProfileType

register = template.Library()


@register.simple_tag
def is_student(value):
    return value in ProfileType.valid_student_types()


@register.simple_tag
def is_company(value):
    return value in ProfileType.valid_company_types()
