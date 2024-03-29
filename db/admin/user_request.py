from django.utils.translation import gettext_lazy as _
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from db.models import UserRequest
from .permissions import ValidationPermissionHelper


class UserRequestAdmin(ModelAdmin):
    model = UserRequest
    menu_label = _('Anfragen')
    menu_icon = 'fa-question-circle'
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('created_at', 'name', 'email', 'message')
    search_fields = ('name', 'email', 'message')
    permission_helper_class = ValidationPermissionHelper


modeladmin_register(UserRequestAdmin)
