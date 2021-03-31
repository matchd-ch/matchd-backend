from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from db.models import JobRequirement


class JobRequirementAdmin(ModelAdmin):
    model = JobRequirement
    menu_label = _('Job Anforderungen')
    menu_icon = 'fa-folder'
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name', )
    search_fields = ('name', )


modeladmin_register(JobRequirementAdmin)
