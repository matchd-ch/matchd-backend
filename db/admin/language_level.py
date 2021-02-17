from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from db.models import LanguageLevel


class LanguageLevelAdmin(ModelAdmin):
    model = LanguageLevel
    menu_label = _('Sprachen Niveaus')
    menu_icon = 'folder-open-inverse'
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('level',)
    search_fields = ('level', 'description', )


modeladmin_register(LanguageLevelAdmin)
