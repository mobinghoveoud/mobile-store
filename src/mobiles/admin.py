from django.contrib import admin

from mobiles.models import Brand, Mobile, Nationality, PriceHistory, Variant


@admin.register(Nationality)
class NationalityAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "get_created",
    )
    readonly_fields = (
        "get_updated",
        "get_created",
    )
    list_per_page = 20

    @admin.display(description=Nationality._meta.get_field("updated").verbose_name)
    def get_updated(self, obj):
        return obj.formatted_updated()

    @admin.display(description=Nationality._meta.get_field("created").verbose_name)
    def get_created(self, obj=None):
        return obj.formatted_created()


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "nationality",
        "get_created",
    )
    readonly_fields = (
        "get_updated",
        "get_created",
    )
    list_filter = ("nationality",)
    list_per_page = 20

    @admin.display(description=Brand._meta.get_field("updated").verbose_name)
    def get_updated(self, obj=None):
        return obj.formatted_updated()

    @admin.display(description=Brand._meta.get_field("created").verbose_name)
    def get_created(self, obj):
        return obj.formatted_created()


@admin.register(Mobile)
class MobileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "brand",
        "model",
        "country",
        "get_created",
    )
    readonly_fields = (
        "get_updated",
        "get_created",
    )
    list_filter = ("brand",)
    list_per_page = 20

    @admin.display(description=Mobile._meta.get_field("updated").verbose_name)
    def get_updated(self, obj):
        return obj.formatted_updated()

    @admin.display(description=Mobile._meta.get_field("created").verbose_name)
    def get_created(self, obj=None):
        return obj.formatted_created()


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "mobile",
        "color",
        "size",
        "get_created",
    )
    readonly_fields = (
        "get_updated",
        "get_created",
    )
    list_filter = ("mobile",)
    list_per_page = 20

    @admin.display(description=Variant._meta.get_field("updated").verbose_name)
    def get_updated(self, obj):
        return obj.formatted_updated()

    @admin.display(description=Variant._meta.get_field("created").verbose_name)
    def get_created(self, obj=None):
        return obj.formatted_created()


@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "variant",
        "price",
        "status",
        "get_date",
    )
    readonly_fields = ("get_date",)
    list_filter = ("status", "variant")
    list_per_page = 20

    @admin.display(description=PriceHistory._meta.get_field("date").verbose_name)
    def get_date(self, obj):
        return obj.formatted_date()
