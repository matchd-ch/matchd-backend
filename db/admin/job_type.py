from django.utils.translation import gettext_lazy as _
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from db.models import JobType
from .permissions import ValidationPermissionHelper


class JobTypeAdmin(ModelAdmin):
    model = JobType
    menu_label = _('Job Types')
    menu_icon = 'fa-folder'
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name', )
    search_fields = ('name', )
    permission_helper_class = ValidationPermissionHelper


modeladmin_register(JobTypeAdmin)
