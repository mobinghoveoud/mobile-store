from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from mobiles.forms import PriceHistoryForm
from mobiles.models import PriceHistory


class PriceHistoryListView(View):
    def get(self, request):
        price_histories = PriceHistory.objects.select_related("variant__mobile").all()

        paginator = Paginator(price_histories, 10)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        return render(request, "mobiles/price_history/list.html", {"page_obj": page_obj})


class PriceHistoryCreateView(View):
    def get(self, request):
        form = PriceHistoryForm()
        return render(request, "mobiles/price_history/form.html", {"form": form})

    def post(self, request):
        form = PriceHistoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Price History created successfully.")
            return redirect("mobiles:price-history-list")
        return render(request, "mobiles/price_history/form.html", {"form": form})


class PriceHistoryUpdateView(View):
    def get(self, request, pk):
        price_history = get_object_or_404(PriceHistory, pk=pk)
        form = PriceHistoryForm(instance=price_history)
        return render(request, "mobiles/price_history/form.html", {"form": form})

    def post(self, request, pk):
        price_history = get_object_or_404(PriceHistory, pk=pk)
        form = PriceHistoryForm(request.POST, instance=price_history)
        if form.is_valid():
            form.save()
            messages.success(request, "Price History updated successfully.")
            return redirect("mobiles:price-history-list")
        return render(request, "mobiles/price_history/form.html", {"form": form})


class PriceHistoryDeleteView(View):
    def post(self, request, pk):
        price_history = get_object_or_404(PriceHistory, pk=pk)
        price_history.delete()
        messages.success(request, "Price History deleted successfully.")
        return redirect("mobiles:price-history-list")
