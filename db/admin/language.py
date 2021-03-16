from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from db.models import Language


class LanguageAdmin(ModelAdmin):
    model = Language
    menu_label = _('Sprachen')
    menu_icon = 'folder-open-inverse'
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name', 'short_list')
    search_fields = ('name',)


modeladmin_register(LanguageAdmin)
