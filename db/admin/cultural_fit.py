from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from db.models import CulturalFit


class CulturalFitAdmin(ModelAdmin):
    model = CulturalFit
    menu_label = _('Kulturelle Werte')
    menu_icon = 'folder-open-inverse'
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('student', 'company',)
    search_fields = ('student', 'company')


modeladmin_register(CulturalFitAdmin)
