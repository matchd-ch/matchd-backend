from django.utils.translation import gettext_lazy as _
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from db.models import Company
from .permissions import ValidationPermissionHelper


class CompanyAdmin(ModelAdmin):
    model = Company
    menu_label = _('Companies')
    menu_icon = 'folder-open-inverse'
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name', )
    search_fields = ('name', )
    permission_helper_class = ValidationPermissionHelper


modeladmin_register(CompanyAdmin)
