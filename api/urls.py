from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("expenses/<int:pk>/delete/", views.delete_expense, name="expense-delete"),
    path("export/csv/", views.export_csv, name="export-csv"),
]