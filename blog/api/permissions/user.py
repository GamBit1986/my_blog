from combojsonapi.permission import PermissionMixin, PermissionForGet, PermissionUser
from combojsonapi.permission.permission_system import PermissionForPatch, PermissionUser
from flask_login import current_user
from flask_combo_jsonapi.exceptions import AccessDenied

from blog.models import User


class UserListPermission(PermissionMixin):
    
    ALL_AVAILABLE_FIELDS = (
        "id",
        "username",
        "name",
        "email",
        "is_staff"
    )
    

    def get(self, *args, many=True, user_permission: PermissionUser = None, **kwargs) -> PermissionForGet:
        if not current_user.is_authenticated:
            raise AccessDenied("Please, sign in")
        self.permission_for_get.allow_columns = (self.ALL_AVAILABLE_FIELDS, 10)
        return self.permission_for_get
    
    

class UserPatchPermission(PermissionMixin):

    PATH_AVAILABLE_FIELDS = (
        "username",
        "name",
    )

    def patch_permission(self, *args, user_permission: PermissionUser = None, **kwargs) -> PermissionForPatch:
        self.permission_for_patch.allow_columns = (self.PATH_AVAILABLE_FIELDS, 10)
        return self.permission_for_patch

    def patch_data(self, *args, data=None, obj=None, user_permission: PermissionUser = None, **kwargs) -> dict:
        permission_for_patch = user_permission.permission_for_patch_permission(model=User)
        return {
            k:v
            for k, v in data.items()
            if k in permission_for_patch.columns
        }
