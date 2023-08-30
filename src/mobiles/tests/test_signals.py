from django.test import TestCase

from mobiles.models import Brand, Mobile, Nationality, Variant
from mobiles.tests.util import generate_image_file


class VariantSignalsTestCase(TestCase):
    def setUp(self):
        self.nationality = Nationality.objects.create(name="Test Nationality")
        self.brand = Brand.objects.create(name="Test Brand", nationality=self.nationality)
        self.mobile = Mobile.objects.create(brand=self.brand, model="Test Model", country=self.nationality)
        self.variant = Variant.objects.create(mobile=self.mobile, color="Red", size=5.5, image=generate_image_file())

    def tearDown(self):
        if self.variant.pk:
            self.variant.delete()

    def test_auto_delete_image_on_delete_signal(self):
        image_path = self.variant.image.path

        self.assertTrue(self.variant.image.storage.exists(image_path))
        self.variant.delete()
        self.assertFalse(self.variant.image.storage.exists(image_path))

    def test_auto_delete_image_on_change_signal(self):
        old_image_path = self.variant.image.path
        updated_image = generate_image_file("updated_image.jpg")
        self.variant.image = updated_image
        self.variant.save()

        self.assertFalse(self.variant.image.storage.exists(old_image_path))

    def test_auto_delete_image_on_change_signal_no_change(self):
        old_image_path = self.variant.image.path
        self.variant.save()

        self.assertTrue(self.variant.image.storage.exists(old_image_path))

    def test_auto_delete_image_on_change_signal_no_old_file(self):
        image_path = self.variant.image.path
        self.assertTrue(self.variant.image.storage.exists(image_path))
