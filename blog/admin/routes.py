from flask_admin import Admin
from .views import MyAdminIndexView
from blog import models
from blog.admin.views import CustomView, TagAdminView, UserAdminView

from blog.extension import db

admin = Admin(
    name="Blog Admin Panel", index_view=MyAdminIndexView(), template_mode="bootstrap4"
)

admin.add_view(TagAdminView(models.Tag, db.session, category="Models"))
admin.add_view(CustomView(models.Article, db.session, category="Models"))
admin.add_view(UserAdminView(models.User, db.session, category="Models"))
