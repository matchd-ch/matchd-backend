from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from db.models import ChallengeType
from .permissions import ValidationPermissionHelper


class ChallengeTypeAdmin(ModelAdmin):
    model = ChallengeType
    menu_label = _('Challenge types')
    menu_icon = 'fa-folder'
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name', )
    search_fields = ('name', )
    permission_helper_class = ValidationPermissionHelper


modeladmin_register(ChallengeTypeAdmin)
