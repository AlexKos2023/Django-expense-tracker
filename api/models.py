from django.conf import settings
from django.db import models


class Expense(models.Model):
    INCOME = "income"
    EXPENSE = "expense"

    CATEGORY_CHOICES = [
        (INCOME, "Доход"),
        (EXPENSE, "Расход"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField("Дата")
    category = models.CharField("Категория", max_length=10, choices=CATEGORY_CHOICES)
    amount = models.PositiveIntegerField("Сумма (в рублях)")
    description = models.TextField("Описание", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        desc = self.description[:30] if self.description else ""
        return f"[{self.get_category_display()}] {self.amount} ₽ — {desc}"