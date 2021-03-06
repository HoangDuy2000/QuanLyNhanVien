from QuanLyNhaSach import db, app, utils
from QuanLyNhaSach.models import Category, Product, User, Orders, OrderDetails, UserRole
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, AdminIndexView, Admin
from flask_login import logout_user, current_user
from flask import redirect, url_for


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class AuthenticatedManage(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.MANAGE


class AuthenticatedEmployee(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.EMPLOYEE


class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class OrderView(ModelView):
    can_view_details = True
    can_export = True
    edit_modal = True


class ProductView(ModelView):
    can_view_details = True
    can_delete = True
    edit_modal = True
    column_searchable_list = ['name', 'price']
    form_excluded_columns = ['order_details']


class CategoryView(ModelView):
    edit_modal = True


class UserView(AuthenticatedAdmin):
    can_view_details = True
    edit_modal = True
    form_excluded_columns = ['order']
    column_searchable_list = ['username']


class StatsView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html',
                           stats=utils.product_stats())


class ReportsView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        return self.render('admin/reports.html',
                           reports=utils.sales_report())


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if current_user.is_authenticated and not current_user.user_role == UserRole.USER:
            return self.render('admin/index.html',
                               stats=utils.category_stats())
        return redirect(url_for('login_post'))


admin = Admin(app=app, name='QU???N TR??? NH?? S??CH', template_mode='bootstrap4', index_view=MyAdminIndexView())
admin.add_view(CategoryView(Category, db.session, name='Danh M???c'))
admin.add_view(ProductView(Product, db.session, name='S???n Ph???m'))
admin.add_view(UserView(User, db.session, name='Ng?????i d??ng'))
admin.add_view(OrderView(Orders, db.session, name='H??a ????n'))
admin.add_view(ModelView(OrderDetails, db.session, name='Chi Ti???t H??a ????n'))
admin.add_view(StatsView(name='Th???ng K??'))
admin.add_view(ReportsView(name='B??o C??o'))
