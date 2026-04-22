from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("expenses/", views.ExpenseListCreateView.as_view(), name="expense-list"),
    path("expenses/<int:pk>/", views.ExpenseDetailView.as_view(), name="expense-detail"),
    path("expenses/<int:pk>/delete/", views.delete_expense, name="expense-delete"),
]