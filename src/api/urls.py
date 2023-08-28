from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from api import views

app_name = "api"

urlpatterns = [
    path("korea-brands/", views.KoreaBrandsView.as_view(), name="korea-brands"),
    path("mobile-brands/", views.MobileBrandsView.as_view(), name="mobile-brands"),
    path("same-nationality/", views.SameNationalityView.as_view(), name="same-nationality"),
    # Spectacular
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="api:schema"), name="swagger-ui"),
    path("schema/redoc/", SpectacularRedocView.as_view(url_name="api:schema"), name="redoc"),
]
