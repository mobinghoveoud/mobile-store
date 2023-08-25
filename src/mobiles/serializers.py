from rest_framework import serializers

from mobiles.models import Brand, Mobile, PriceHistory, Variant


class PriceHistorySerializer(serializers.ModelSerializer):
    variant = serializers.CharField(source="variant.color")
    status = serializers.CharField(source="get_status_display")
    date = serializers.CharField(source="formatted_date")

    class Meta:
        model = PriceHistory
        fields = (
            "id",
            "variant",
            "price",
            "status",
            "date",
        )
        read_only_fields = ("date",)


class VariantSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(source="mobile.model")
    prices = PriceHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Variant
        fields = (
            "id",
            "mobile",
            "color",
            "size",
            "prices",
            "image",
        )
        read_only_fields = (
            "updated",
            "created",
        )


class MobileSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source="brand.name")
    country = serializers.CharField(source="country.name")
    variants = VariantSerializer(many=True, read_only=True)

    class Meta:
        model = Mobile
        fields = (
            "id",
            "brand",
            "model",
            "country",
            "variants",
        )
        read_only_fields = (
            "updated",
            "created",
        )

    def __init__(self, instance=None, flat=False, **kwargs):
        super().__init__(instance, **kwargs)
        self.flat = flat

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not self.flat:
            return data

        mobile_data = data.pop("variants")
        result = {}
        index = 0
        for variant in mobile_data:
            for price in variant["prices"]:
                variant_data = {
                    "brand": data["brand"],
                    "model": data["model"],
                    "country": data["country"],
                    "color": variant["color"],
                    "size": variant["size"],
                    "image": variant["image"],
                    "price": price["price"],
                    "status": price["status"],
                    "date": price["date"],
                }

                result[index] = variant_data
                index += 1

        return result


class BrandSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    mobiles = MobileSerializer(many=True, read_only=True)
    nationality = serializers.CharField(source="nationality.name")

    class Meta:
        model = Brand
        fields = (
            "id",
            "name",
            "nationality",
            "mobiles",
        )
        read_only_fields = (
            "updated",
            "created",
        )

    def __init__(self, instance=None, flat=False, **kwargs):
        super().__init__(instance, **kwargs)
        self.flat = flat

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not self.flat:
            return data

        mobile_data = data.pop("mobiles")
        result = {}
        index = 0
        for mobile in mobile_data:
            for variant in mobile["variants"]:
                for price in variant["prices"]:
                    variant_data = {
                        "brand": data["name"],
                        "nationality": data["nationality"],
                        "model": mobile["model"],
                        "country": mobile["country"],
                        "color": variant["color"],
                        "size": variant["size"],
                        "image": variant["image"],
                        "price": price["price"],
                        "status": price["status"],
                        "date": price["date"],
                    }

                    result[index] = variant_data
                    index += 1

        return result
