from django.urls import path

from mobiles.views import all_view, brand_view, mobile_view, nationality_view, price_view, variant_view

app_name = "mobiles"

urlpatterns = [
    path("", all_view.AllMobilesView.as_view(), name="all-mobiles"),
    # Nationality
    path("nationalities/", nationality_view.NationalityListView.as_view(), name="nationality-list"),
    path("nationalities/create/", nationality_view.NationalityCreateView.as_view(), name="nationality-create"),
    path("nationalities/<int:pk>/edit/", nationality_view.NationalityUpdateView.as_view(), name="nationality-edit"),
    path("nationalities/<int:pk>/delete/", nationality_view.NationalityDeleteView.as_view(), name="nationality-delete"),
    # Brand
    path("brands/", brand_view.BrandListView.as_view(), name="brand-list"),
    path("brands/create/", brand_view.BrandCreateView.as_view(), name="brand-create"),
    path("brands/<int:pk>/edit/", brand_view.BrandUpdateView.as_view(), name="brand-edit"),
    path("brands/<int:pk>/delete/", brand_view.BrandDeleteView.as_view(), name="brand-delete"),
    # Mobile
    path("mobiles/", mobile_view.MobileListView.as_view(), name="mobile-list"),
    path("mobiles/create/", mobile_view.MobileCreateView.as_view(), name="mobile-create"),
    path("mobiles/<int:pk>/edit/", mobile_view.MobileUpdateView.as_view(), name="mobile-edit"),
    path("mobiles/<int:pk>/delete/", mobile_view.MobileDeleteView.as_view(), name="mobile-delete"),
    # Variant
    path("variants/", variant_view.VariantListView.as_view(), name="variant-list"),
    path("variants/create/", variant_view.VariantCreateView.as_view(), name="variant-create"),
    path("variants/<int:pk>/edit/", variant_view.VariantUpdateView.as_view(), name="variant-edit"),
    path("variants/<int:pk>/delete/", variant_view.VariantDeleteView.as_view(), name="variant-delete"),
    # PriceHistory
    path("price-histories/", price_view.PriceHistoryListView.as_view(), name="price-history-list"),
    path("price-histories/create/", price_view.PriceHistoryCreateView.as_view(), name="price-history-create"),
    path("price-histories/<int:pk>/edit/", price_view.PriceHistoryUpdateView.as_view(), name="price-history-edit"),
    path("price-histories/<int:pk>/delete/", price_view.PriceHistoryDeleteView.as_view(), name="price-history-delete"),
]
