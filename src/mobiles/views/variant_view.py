from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from mobiles.forms import VariantForm
from mobiles.models import Variant


class VariantListView(View):
    def get(self, request):
        variants = Variant.objects.select_related("mobile__country", "mobile__brand").all()

        paginator = Paginator(variants, 10)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        return render(request, "mobiles/variant/list.html", {"page_obj": page_obj})


class VariantCreateView(View):
    def get(self, request):
        form = VariantForm()
        return render(request, "mobiles/variant/form.html", {"form": form})

    def post(self, request):
        form = VariantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Variant created successfully.")
            return redirect("mobiles:variant-list")
        return render(request, "mobiles/variant/form.html", {"form": form})


class VariantUpdateView(View):
    def get(self, request, pk):
        variant = get_object_or_404(Variant, pk=pk)
        form = VariantForm(instance=variant)
        return render(request, "mobiles/variant/form.html", {"form": form})

    def post(self, request, pk):
        variant = get_object_or_404(Variant, pk=pk)
        form = VariantForm(request.POST, request.FILES, instance=variant)
        if form.is_valid():
            form.save()
            messages.success(request, "Variant updated successfully.")
            return redirect("mobiles:variant-list")
        return render(request, "mobiles/variant/form.html", {"form": form})


class VariantDeleteView(View):
    def post(self, request, pk):
        variant = get_object_or_404(Variant, pk=pk)
        variant.delete()
        messages.success(request, "Variant deleted successfully.")

        return redirect("mobiles:variant-list")
