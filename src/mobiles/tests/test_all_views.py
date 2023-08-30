from django.test import Client, TestCase
from django.urls import reverse

from mobiles.models import Brand, Mobile, Nationality, PriceHistory, Variant
from mobiles.tests.util import generate_image_file


class AllMobilesViewTestCase(TestCase):
    nationalities: [Nationality]
    brands: [Brand]
    mobiles: [Mobile]
    variants: [Variant]
    price_histories: [PriceHistory]

    @classmethod
    def setUpTestData(cls):
        cls.nationalities = []
        cls.brands = []
        cls.mobiles = []
        cls.variants = []
        cls.price_histories = []

        for i in range(15):
            nationality = Nationality.objects.create(name=f"Test Nationality {i}")
            brand = Brand.objects.create(name=f"Test Brand {i}", nationality=nationality)
            mobile = Mobile.objects.create(brand=brand, model=f"Test Mobile {i}", country=nationality)
            variant = Variant.objects.create(
                mobile=mobile, color=f"Color {i}", size=5.0 + i, image=generate_image_file()
            )
            price = PriceHistory.objects.create(variant=variant, price=200 + i, status=True)

            cls.nationalities.append(nationality)
            cls.brands.append(brand)
            cls.mobiles.append(mobile)
            cls.variants.append(variant)
            cls.price_histories.append(price)

    def tearDown(self) -> None:
        for variant in self.variants:
            variant.delete()

    def setUp(self):
        self.client = Client()

    def test_all_mobiles_view_pagination_first_page(self):
        response = self.client.get(reverse("mobiles:all-mobiles"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.brands[0].name)
        self.assertContains(response, self.mobiles[0].model)
        self.assertContains(response, self.variants[0].color)
        self.assertContains(response, self.variants[0].size)
        self.assertContains(response, self.nationalities[0].name)
        self.assertContains(response, self.price_histories[0].price)
        self.assertContains(response, self.variants[0].image.name)
        self.assertNotContains(response, self.brands[10].name)
        self.assertNotContains(response, self.mobiles[10].model)

    def test_all_mobiles_view_pagination_second_page(self):
        response = self.client.get(reverse("mobiles:all-mobiles"), {"page": 2})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.brands[10].name)
        self.assertContains(response, self.mobiles[10].model)
        self.assertContains(response, self.variants[10].color)
        self.assertContains(response, self.variants[10].size)
        self.assertContains(response, self.nationalities[10].name)
        self.assertContains(response, self.price_histories[10].price)
        self.assertContains(response, self.variants[10].image.name)
        self.assertNotContains(response, self.brands[9].name)
        self.assertNotContains(response, self.mobiles[9].model)
