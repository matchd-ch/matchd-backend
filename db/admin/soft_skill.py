from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from db.models import SoftSkill
from .permissions import ValidationPermissionHelper


class SoftSkillAdmin(ModelAdmin):
    model = SoftSkill
    menu_label = _('Soft Skills')
    menu_icon = 'folder-open-inverse'
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('student', 'company',)
    search_fields = ('student', 'company')
    permission_helper_class = ValidationPermissionHelper


modeladmin_register(SoftSkillAdmin)
