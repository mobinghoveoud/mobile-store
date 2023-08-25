from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.datetime_safe import datetime
from django.utils.translation import gettext_lazy as _

from mobiles.managers import BrandManager, MobileManager, PriceHistoryManager, VariantManager


class BaseModel(models.Model):
    updated = models.DateTimeField(_("Updated"), auto_now=True)
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ("created",)

    def formatted_created(self):
        return self.created.strftime("%Y-%m-%d %H:%M")

    def formatted_updated(self):
        return self.updated.strftime("%Y-%m-%d %H:%M")


class Nationality(BaseModel):
    name = models.CharField(_("Nationality name"), max_length=150)

    def __str__(self):
        return self.name


class Brand(BaseModel):
    name = models.CharField(_("Brand name"), max_length=150)
    nationality = models.ForeignKey(Nationality, on_delete=models.PROTECT, related_name="brands")

    objects = BrandManager()

    def __str__(self):
        return f"{self.name} ({self.nationality})"


class Mobile(BaseModel):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="mobiles")
    model = models.CharField(_("Mobile model"), max_length=150, unique=True)
    country = models.ForeignKey(Nationality, on_delete=models.PROTECT, related_name="mobiles")

    objects = MobileManager()

    def __str__(self):
        return f"{self.brand.name} {self.model} ({self.country})"


def mobile_image_path(instance, filename):
    ext = filename.split(".")[-1]
    return f"mobiles/{instance.mobile.model}-{uuid4().hex}.{ext}"


class Variant(BaseModel):
    mobile = models.ForeignKey(Mobile, on_delete=models.CASCADE, related_name="variants")
    color = models.CharField(_("Mobile color"), max_length=100)
    size = models.FloatField(_("Mobile screen size"), validators=[MinValueValidator(1)])
    image = models.ImageField(_("Mobile image"), upload_to=mobile_image_path)

    objects = VariantManager()

    def __str__(self):
        return f"{self.mobile.model} ({self.color}, {self.size})"


class PriceHistory(BaseModel):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name="prices")
    price = models.DecimalField(_("Variant price"), max_digits=9, decimal_places=0, validators=[MinValueValidator(1)])
    status = models.BooleanField(_("Status"), default=True)
    date = models.DateField(_("Price date"), default=datetime.now)

    objects = PriceHistoryManager()

    def get_status_display(self):
        return _("Available") if self.status else _("Not Available")

    def formatted_date(self):
        return self.date.strftime("%Y-%m-%d")

    def __str__(self):
        return f"{self.price}$ at {self.formatted_date()} ({self.get_status_display()})"
