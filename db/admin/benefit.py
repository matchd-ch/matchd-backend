from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .permissions import ValidationPermissionHelper
from db.models import Benefit


class BenefitAdmin(ModelAdmin):
    model = Benefit
    menu_label = _('Benefits')
    menu_icon = 'folder-open-inverse'
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('icon',)
    search_fields = ('icon',)
    permission_helper_class = ValidationPermissionHelper


modeladmin_register(BenefitAdmin)
