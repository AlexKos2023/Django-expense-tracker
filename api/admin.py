import csv
from django.contrib import admin
from django.http import HttpResponse
from .models import Expense


def export_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="expenses_admin.csv"'
    response.write("\ufeff")

    writer = csv.writer(response)
    writer.writerow(["Дата", "Категория", "Сумма", "Описание", "Пользователь"])

    for obj in queryset:
        writer.writerow([
            obj.date,
            obj.get_category_display(),
            obj.amount,
            obj.description,
            obj.user,
        ])

    return response


export_as_csv.short_description = "Скачать выбранные записи в CSV"


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("date", "category", "amount", "description", "user")
    list_filter = ("category", "date", "user")
    search_fields = ("description", "user__username")
    ordering = ("-date",)
    actions = [export_as_csv]