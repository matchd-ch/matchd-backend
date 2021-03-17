from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from db.models import Category


class CategoryAdmin(ModelAdmin):
    model = Category
    menu_label = _('Categories')
    menu_icon = 'folder-open-inverse'
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name',)
    search_fields = ('name',)


modeladmin_register(CategoryAdmin)
