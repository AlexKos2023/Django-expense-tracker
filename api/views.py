from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics
from .models import Expense
from .serializers import ExpenseSerializer
from .forms import ExpenseForm

class ExpenseListCreateView(generics.ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

def index(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = ExpenseForm()

    expenses = Expense.objects.all().order_by("-date")
    return render(request, "api/index.html", {"form": form, "expenses": expenses})

def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == "POST":
        expense.delete()
    return redirect("home")