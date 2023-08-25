from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from mobiles.forms import NationalityForm
from mobiles.models import Nationality


class NationalityListView(View):
    def get(self, request):
        nationalities = Nationality.objects.all()

        paginator = Paginator(nationalities, 10)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        return render(request, "mobiles/nationality/list.html", {"page_obj": page_obj})


class NationalityCreateView(View):
    def get(self, request):
        form = NationalityForm()
        return render(request, "mobiles/nationality/form.html", {"form": form})

    def post(self, request):
        form = NationalityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Nationality created successfully.")
            return redirect("mobiles:nationality-list")
        return render(request, "mobiles/nationality/form.html", {"form": form})


class NationalityUpdateView(View):
    def get(self, request, pk):
        nationality = get_object_or_404(Nationality, pk=pk)
        form = NationalityForm(instance=nationality)
        return render(request, "mobiles/nationality/form.html", {"form": form})

    def post(self, request, pk):
        nationality = get_object_or_404(Nationality, pk=pk)
        form = NationalityForm(request.POST, instance=nationality)
        if form.is_valid():
            form.save()
            messages.success(request, "Nationality updated successfully.")
            return redirect("mobiles:nationality-list")
        return render(request, "mobiles/nationality/form.html", {"form": form})


class NationalityDeleteView(View):
    def post(self, request, pk):
        nationality = get_object_or_404(Nationality, pk=pk)
        nationality.delete()
        messages.success(request, "Nationality deleted successfully.")

        return redirect("mobiles:nationality-list")
