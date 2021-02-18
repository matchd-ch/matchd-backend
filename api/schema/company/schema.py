import graphene
from django.utils.translation import gettext as _


class StudentProfileInputStep1(graphene.InputObjectType):
    first_name = graphene.String(description=_('First name'), required=True)
    last_name = graphene.String(description=_('Last name'), required=True)
    uid = graphene.String(description=_('Uid'), required=True)
    street = graphene.String(description=_('Street'), required=True)
    zip = graphene.String(description=_('Zip'), required=True)
    city = graphene.String(description=_('City'), required=True)
    phone = graphene.String(description=_('Phone Number'))
    email = graphene.String(description=_('Email'), required=True)