from django.core.exceptions import ValidationError
from django.test import TestCase

from mobiles.models import Brand, Mobile, Nationality, PriceHistory, Variant
from mobiles.tests.util import generate_image_file


class VariantModelTestCase(TestCase):
    def setUp(self):
        self.nationality = Nationality.objects.create(name="Test Nationality")
        self.brand = Brand.objects.create(name="Test Brand", nationality=self.nationality)
        self.mobile = Mobile.objects.create(brand=self.brand, model="Test Mobile", country=self.nationality)

    def test_variant_size_validation_with_invalid_data(self):
        invalid_sizes = [-1.5, 0.9, 0]

        for size in invalid_sizes:
            with self.subTest(size=size):
                with self.assertRaises(ValidationError):
                    variant = Variant(mobile=self.mobile, color="Red", size=size, image=generate_image_file())
                    variant.full_clean()

    def test_variant_size_validation_with_valid_data(self):
        valid_sizes = [1.5, 3.0, 10.0]
        for size in valid_sizes:
            with self.subTest(size=size):
                try:
                    variant = Variant(mobile=self.mobile, color="Red", size=size, image=generate_image_file())
                    variant.full_clean()
                except ValidationError:
                    self.fail("Validation Error raised unexpectedly.")


class PriceHistoryModelTestCase(TestCase):
    def setUp(self):
        self.nationality = Nationality.objects.create(name="Test Nationality")
        self.brand = Brand.objects.create(name="Test Brand", nationality=self.nationality)
        self.mobile = Mobile.objects.create(brand=self.brand, model="Test Mobile", country=self.nationality)
        self.variant = Variant.objects.create(mobile=self.mobile, color="Red", size=5.5, image=generate_image_file())

    def tearDown(self) -> None:
        self.variant.delete()

    def test_price_history_price_validation_with_invalid_data(self):
        invalid_prices = [0, 0.5, -1, -5.5]
        for price in invalid_prices:
            with self.subTest(price=price):
                with self.assertRaises(ValidationError):
                    price_history = PriceHistory(variant=self.variant, price=price)
                    price_history.full_clean()

    def test_price_history_price_validation_with_valid_data(self):
        valid_prices = [1, 100, 1000]
        for price in valid_prices:
            with self.subTest(price=price):
                price_history = PriceHistory(variant=self.variant, price=price)
                price_history.full_clean()
                price_history.save()
                self.assertIsNotNone(price_history.pk)

    def test_get_status_display(self):
        available_price_history = PriceHistory.objects.create(variant=self.variant, price=1000, status=True)
        self.assertEqual(available_price_history.get_status_display(), "Available")

        not_available_price_history = PriceHistory.objects.create(variant=self.variant, price=1500, status=False)
        self.assertEqual(not_available_price_history.get_status_display(), "Not Available")
