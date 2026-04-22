from django.db import models


class Expense(models.Model):
    INCOME = "income"
    EXPENSE = "expense"

    CATEGORY_CHOICES = [
        (INCOME, "Доход"),
        (EXPENSE, "Расход"),
    ]

    date = models.DateField("Дата")
    category = models.CharField("Категория", max_length=10, choices=CATEGORY_CHOICES)
    amount = models.PositiveIntegerField("Сумма (в рублях)")
    description = models.TextField("Описание", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"[{self.get_category_display()}] {self.amount} ₽ — {self.description[:30]}"