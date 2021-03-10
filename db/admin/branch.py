from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from db.models import Branch


class BranchAdmin(ModelAdmin):
    model = Branch
    menu_label = _('Branches')
    menu_icon = 'folder-open-inverse'
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name',)
    search_fields = ('name',)


modeladmin_register(BranchAdmin)
