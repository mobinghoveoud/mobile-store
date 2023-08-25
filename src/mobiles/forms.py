from django import forms

from mobiles.models import Brand, Mobile, Nationality, PriceHistory, Variant


class NationalityForm(forms.ModelForm):
    class Meta:
        model = Nationality
        fields = [
            "name",
        ]


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = [
            "name",
            "nationality",
        ]


class MobileForm(forms.ModelForm):
    class Meta:
        model = Mobile
        fields = [
            "model",
            "brand",
            "country",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class VariantForm(forms.ModelForm):
    class Meta:
        model = Variant
        fields = [
            "mobile",
            "color",
            "size",
            "image",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PriceHistoryForm(forms.ModelForm):
    class Meta:
        model = PriceHistory
        fields = [
            "variant",
            "price",
            "status",
            "date",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
