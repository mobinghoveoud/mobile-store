from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from mobiles.forms import BrandForm
from mobiles.models import Brand


class BrandListView(View):
    def get(self, request):
        brands = Brand.objects.all()

        paginator = Paginator(brands, 10)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        return render(request, "mobiles/brand/list.html", {"page_obj": page_obj})


class BrandCreateView(View):
    def get(self, request):
        form = BrandForm()
        return render(request, "mobiles/brand/form.html", {"form": form})

    def post(self, request):
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Brand created successfully.")
            return redirect("mobiles:brand-list")
        return render(request, "mobiles/brand/form.html", {"form": form})


class BrandUpdateView(View):
    def get(self, request, pk):
        brand = get_object_or_404(Brand, pk=pk)
        form = BrandForm(instance=brand)
        return render(request, "mobiles/brand/form.html", {"form": form})

    def post(self, request, pk):
        brand = get_object_or_404(Brand, pk=pk)
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            form.save()
            messages.success(request, "Brand updated successfully.")
            return redirect("mobiles:brand-list")
        return render(request, "mobiles/brand/form.html", {"form": form})


class BrandDeleteView(View):
    def post(self, request, pk):
        brand = get_object_or_404(Brand, pk=pk)
        brand.delete()
        messages.success(request, "Brand deleted successfully.")

        return redirect("mobiles:brand-list")
