from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for
from flask_login import current_user
from flask_admin import AdminIndexView, expose


class CustomView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_staff

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for("auth.login"))


class TagAdminView(CustomView):
    column_searchable_list = ("name",)
    column_filters = ("name",)
    can_export = True
    export_types = ["csv", "xlsx"]
    create_modal = True
    edit_modal = True


class UserAdminView(CustomView):
    column_exclude_list = ("password",)
    column_searchable_list = (
        "name",
        "username",
        "is_staff",
        "email",
    )
    column_filters = ("name", "username", "is_staff", "email")
    column_editable_list = ("name", "username", "is_staff", "email")
    can_create = True
    can_edit = True
    can_delete = False


class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if not (current_user.is_authenticated and current_user.is_staff):
            return redirect(url_for("auth.login"))
        return super(MyAdminIndexView, self).index()
