from random import randint

from django.test import TestCase

from mobiles.models import Brand, Mobile, Nationality, PriceHistory, Variant
from mobiles.serializers import BrandSerializer, MobileSerializer
from mobiles.tests.util import generate_image_file


class SerializerTestCase(TestCase):
    nationalities: list
    brands: list
    mobiles: list
    variants: list
    price_histories: list

    @classmethod
    def setUpTestData(cls):
        colors = ["Red", "White", "Black"]

        cls.nationalities = []
        cls.brands = []
        cls.mobiles = []
        cls.variants = []
        cls.price_histories = []

        for i in range(3):
            nationality = Nationality.objects.create(name=f"Test Nationality {i}")
            brand = Brand.objects.create(name=f"Test Brand {i}", nationality=nationality)
            mobile = Mobile.objects.create(brand=brand, model=f"Test Mobile {i}", country=nationality)
            variant = Variant.objects.create(
                mobile=mobile, color=colors[i], size=randint(1, 10), image=generate_image_file()
            )
            price_history = PriceHistory.objects.create(variant=variant, price=randint(500, 100000))

            cls.nationalities.append(nationality)
            cls.brands.append(brand)
            cls.mobiles.append(mobile)
            cls.variants.append(variant)
            cls.price_histories.append(price_history)

    @classmethod
    def tearDownClass(cls):
        Variant.objects.all().delete()
        super().tearDownClass()

    def test_brand_serializer_single_flat(self):
        serializer = BrandSerializer(instance=self.brands[0], flat=True)
        output = serializer.data

        expected_output = {
            "brand": self.brands[0].name,
            "nationality": self.brands[0].nationality.name,
            "model": self.mobiles[0].model,
            "country": self.mobiles[0].country.name,
            "color": self.variants[0].color,
            "size": self.variants[0].size,
            "image": self.variants[0].image.url,
            "price": str(self.price_histories[0].price),
            "status": self.price_histories[0].get_status_display(),
            "date": self.price_histories[0].formatted_date(),
        }

        self.assertDictEqual(output[0], expected_output)

    def test_brand_serializer_many_flat(self):
        serializer = BrandSerializer(instance=self.brands, many=True, flat=True)
        output = serializer.data

        expected_output = [
            {
                0: {
                    "brand": brand.name,
                    "nationality": brand.nationality.name,
                    "model": mobile.model,
                    "country": mobile.country.name,
                    "color": variant.color,
                    "size": variant.size,
                    "image": variant.image.url,
                    "price": str(price_history.price),
                    "status": price_history.get_status_display(),
                    "date": price_history.formatted_date(),
                }
            }
            for brand, mobile, variant, price_history in zip(
                self.brands, self.mobiles, self.variants, self.price_histories
            )
        ]

        self.assertListEqual(output, expected_output)

    def test_mobile_serializer_flat(self):
        serializer = MobileSerializer(instance=self.mobiles[0], flat=True)
        output = serializer.data[0]

        expected_output = {
            "brand": self.brands[0].name,
            "model": self.mobiles[0].model,
            "country": self.nationalities[0].name,
            "color": self.variants[0].color,
            "size": self.variants[0].size,
            "image": self.variants[0].image.url,
            "price": str(self.price_histories[0].price),
            "status": self.price_histories[0].get_status_display(),
            "date": self.price_histories[0].formatted_date(),
        }

        self.assertDictEqual(output, expected_output)

    def test_mobile_serializer_many_flat(self):
        serializer = MobileSerializer(instance=self.mobiles, many=True, flat=True)
        output = serializer.data

        expected_output = [
            {
                0: {
                    "brand": brand.name,
                    "model": mobile.model,
                    "country": mobile.country.name,
                    "color": variant.color,
                    "size": variant.size,
                    "image": variant.image.url,
                    "price": str(price_history.price),
                    "status": price_history.get_status_display(),
                    "date": price_history.formatted_date(),
                }
            }
            for brand, mobile, variant, price_history in zip(
                self.brands, self.mobiles, self.variants, self.price_histories
            )
        ]

        self.assertListEqual(output, expected_output)
