from django.utils.translation import gettext_lazy as _
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from db.models import Keyword
from .permissions import ValidationPermissionHelper


class KeywordAdmin(ModelAdmin):
    model = Keyword
    menu_label = _('Keywords')
    menu_icon = 'fa-folder'
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name', )
    search_fields = ('name', )
    permission_helper_class = ValidationPermissionHelper


modeladmin_register(KeywordAdmin)
