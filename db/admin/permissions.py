from wagtail_modeladmin.helpers import PermissionHelper

from db.models import ProfileType


class ValidationPermissionHelper(PermissionHelper):

    def user_can_list(self, user):
        return True

    def user_can_create(self, user):
        return True

    def user_can_edit_obj(self, user, obj):
        return True

    def user_can_delete_obj(self, user, obj):
        if user.type == ProfileType.INTERNAL:
            return True
        return False
