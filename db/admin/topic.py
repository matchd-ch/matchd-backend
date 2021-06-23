from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from db.models import Topic
from .permissions import ValidationPermissionHelper


class TopicAdmin(ModelAdmin):
    model = Topic
    menu_label = _('Topics')
    menu_icon = 'fa-folder'
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name', )
    search_fields = ('name', )
    permission_helper_class = ValidationPermissionHelper


modeladmin_register(TopicAdmin)
