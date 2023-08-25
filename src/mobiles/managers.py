from django.db import models


class BrandManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("nationality")


class MobileManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("brand", "country")


class VariantManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("mobile")


class PriceHistoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("variant")
