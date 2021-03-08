from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from db.models import Expectation


class ExpectationAdmin(ModelAdmin):
    model = Expectation
    menu_label = _('Job Erwartungen')
    menu_icon = 'fa-folder'
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name', )
    search_fields = ('name', )


modeladmin_register(ExpectationAdmin)
