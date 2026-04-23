from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.db.models import Sum, Q
from django.db.models.functions import TruncMonth
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now

import plotly.graph_objects as go
import plotly.io as pio

from .forms import ExpenseForm
from .models import Expense
from .serializers import ExpenseSerializer
from rest_framework import generics

import csv
from django.http import HttpResponse

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def index(request):
    today = now()
    selected_year = int(request.GET.get("year", today.year))
    selected_month = int(request.GET.get("month", today.month))

    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect(f"/?year={selected_year}&month={selected_month}")
    else:
        form = ExpenseForm()

    user_expenses = Expense.objects.filter(user=request.user)

    expenses = user_expenses.filter(
        date__year=selected_year,
        date__month=selected_month,
    ).order_by("-date")

    total_income = expenses.filter(category="income").aggregate(total=Sum("amount"))["total"] or 0
    total_expense = expenses.filter(category="expense").aggregate(total=Sum("amount"))["total"] or 0
    balance = total_income - total_expense

    monthly_data = (
        user_expenses
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(
            income=Sum("amount", filter=Q(category="income")),
            expense=Sum("amount", filter=Q(category="expense")),
        )
        .order_by("month")
    )

    months = []
    income_vals = []
    expense_vals = []

    for item in monthly_data:
        month = item["month"]
        months.append(month.strftime("%b %Y") if month else "")
        income_vals.append(item["income"] or 0)
        expense_vals.append(item["expense"] or 0)

    if not months:
        months = ["Нет данных"]
        income_vals = [0]
        expense_vals = [0]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=months, y=income_vals, name="Доход", marker_color="#2ca02c"))
    fig.add_trace(go.Bar(x=months, y=expense_vals, name="Расход", marker_color="#d62728"))
    fig.update_layout(
        barmode="group",
        title="Доходы и расходы по месяцам",
        xaxis_title="Месяц",
        yaxis_title="Рубли",
        template="plotly_white",
        height=450,
        margin=dict(l=20, r=20, t=60, b=40),
    )
    chart_html = pio.to_html(fig, full_html=False, include_plotlyjs="cdn")

    years = (
        user_expenses.dates("date", "year", order="ASC")
        .values_list("date__year", flat=True)
        .distinct()
    )
    years = list(years) or [today.year]

    months_choices = [
        (1, "Январь"), (2, "Февраль"), (3, "Март"), (4, "Апрель"),
        (5, "Май"), (6, "Июнь"), (7, "Июль"), (8, "Август"),
        (9, "Сентябрь"), (10, "Октябрь"), (11, "Ноябрь"), (12, "Декабрь"),
    ]

    return render(request, "api/index.html", {
        "form": form,
        "expenses": expenses,
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "chart_html": chart_html,
        "years": years,
        "months_choices": months_choices,
        "selected_year": selected_year,
        "selected_month": selected_month,
    })


@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == "POST":
        expense.delete()
    return redirect(request.META.get("HTTP_REFERER", "/"))


class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

@login_required
def export_csv(request):
    today = now()
    selected_year = int(request.GET.get("year", today.year))
    selected_month = int(request.GET.get("month", today.month))

    queryset = Expense.objects.filter(
        user=request.user,
        date__year=selected_year,
        date__month=selected_month,
    ).order_by("-date")

    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="expenses.csv"'
    response.write("\ufeff")

    writer = csv.writer(response)
    writer.writerow(["Дата", "Категория", "Сумма", "Описание"])

    for expense in queryset:
        writer.writerow([
            expense.date,
            expense.get_category_display(),
            expense.amount,
            expense.description,
        ])

    return response