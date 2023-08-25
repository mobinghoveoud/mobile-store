from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from mobiles.models import Brand


class AllMobilesView(View):
    def get(self, request):
        brands = Brand.objects.prefetch_related("mobiles__variants__prices")

        all_mobiles = []
        for brand in brands:
            for mobile in brand.mobiles.all():
                for variant in mobile.variants.all():
                    all_mobiles.append([
                        brand.name,
                        brand.nationality.name,
                        mobile.model,
                        variant.color,
                        variant.size,
                        mobile.country.name,
                        [price for price in variant.prices.all()],
                        variant.image.url,
                    ])

        paginator = Paginator(all_mobiles, 10)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        return render(request, "mobiles/all.html", {"page_obj": page_obj})
