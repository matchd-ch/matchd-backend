from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from db.models import Skill
from .permissions import ValidationPermissionHelper


class SkillAdmin(ModelAdmin):
    model = Skill
    menu_label = _('Skills')
    menu_icon = 'folder-open-inverse'
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name',)
    search_fields = ('name',)
    permission_helper_class = ValidationPermissionHelper


modeladmin_register(SkillAdmin)
