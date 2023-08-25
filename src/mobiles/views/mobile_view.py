from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from mobiles.forms import MobileForm
from mobiles.models import Mobile


class MobileListView(View):
    def get(self, request):
        mobiles = Mobile.objects.all()

        paginator = Paginator(mobiles, 10)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        return render(request, "mobiles/mobile/list.html", {"page_obj": page_obj})


class MobileCreateView(View):
    def get(self, request):
        form = MobileForm()
        return render(request, "mobiles/mobile/form.html", {"form": form})

    def post(self, request):
        form = MobileForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Mobile created successfully.")
            return redirect("mobiles:mobile-list")
        return render(request, "mobiles/mobile/form.html", {"form": form})


class MobileUpdateView(View):
    def get(self, request, pk):
        mobile = get_object_or_404(Mobile, pk=pk)
        form = MobileForm(instance=mobile)
        return render(request, "mobiles/mobile/form.html", {"form": form})

    def post(self, request, pk):
        mobile = get_object_or_404(Mobile, pk=pk)
        form = MobileForm(request.POST, instance=mobile)
        if form.is_valid():
            form.save()
            messages.success(request, "Mobile updated successfully.")
            return redirect("mobiles:mobile-list")
        return render(request, "mobiles/mobile/form.html", {"form": form})


class MobileDeleteView(View):
    def post(self, request, pk):
        mobile = get_object_or_404(Mobile, pk=pk)
        mobile.delete()
        messages.success(request, "Mobile deleted successfully.")

        return redirect("mobiles:mobile-list")
