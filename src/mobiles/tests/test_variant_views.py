from django.test import Client, TestCase
from django.urls import reverse

from mobiles.forms import VariantForm
from mobiles.models import Brand, Mobile, Nationality, Variant
from mobiles.tests.util import generate_image_file


class VariantListViewTestCase(TestCase):
    nationality: Nationality
    brand: Brand
    mobile: Mobile

    @classmethod
    def setUpTestData(cls):
        cls.nationality = Nationality.objects.create(name="Test Nationality")
        cls.brand = Brand.objects.create(name="Test Brand", nationality=cls.nationality)
        cls.mobile = Mobile.objects.create(brand=cls.brand, model="Test Model", country=cls.nationality)
        for i in range(15):
            Variant.objects.create(mobile=cls.mobile, color=f"Color {i}", size=5.5, image=generate_image_file())

    @classmethod
    def tearDownClass(cls):
        for variant in Variant.objects.all():
            variant.image.delete()

        super().tearDownClass()

    def setUp(self):
        self.client = Client()

    def test_pagination_first_page(self):
        response = self.client.get(reverse("mobiles:variant-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Color 0")
        self.assertContains(response, "Color 9")
        self.assertNotContains(response, "Color 10")

    def test_pagination_second_page(self):
        response = self.client.get(reverse("mobiles:variant-list"), {"page": 2})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Color 10")
        self.assertContains(response, "Color 14")
        self.assertNotContains(response, "Color 0")

    def test_pagination_invalid_page_number(self):
        response = self.client.get(reverse("mobiles:variant-list"), {"page": 3})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Color 10")
        self.assertContains(response, "Color 14")
        self.assertNotContains(response, "Color 0")


class VariantCreateViewTestCase(TestCase):
    nationality: Nationality
    brand: Brand
    mobile: Mobile

    @classmethod
    def setUpTestData(cls):
        cls.nationality = Nationality.objects.create(name="Test Nationality")
        cls.brand = Brand.objects.create(name="Test Brand", nationality=cls.nationality)
        cls.mobile = Mobile.objects.create(brand=cls.brand, model="Test Model", country=cls.nationality)
        cls.variant_data = {"mobile": cls.mobile.pk, "color": "Test Color", "size": 5.5, "image": generate_image_file()}

    @classmethod
    def tearDownClass(cls):
        Brand.objects.all().delete()
        super().tearDownClass()

    def tearDown(self) -> None:
        for variant in Variant.objects.all():
            variant.image.delete()

    def test_variant_create_view_get(self):
        response = self.client.get(reverse("mobiles:variant-create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mobiles/variant/form.html")
        self.assertIsInstance(response.context["form"], VariantForm)

    def test_variant_create_view_post_valid_data(self):
        response = self.client.post(reverse("mobiles:variant-create"), data=self.variant_data, follow=True)

        self.assertRedirects(response, reverse("mobiles:variant-list"))
        self.assertEqual(Variant.objects.count(), 1)
        self.assertEqual(str(list(response.context["messages"])[0]), "Variant created successfully.")
        last_obj = Variant.objects.last()
        self.assertEqual(last_obj.color, self.variant_data["color"])
        self.assertEqual(last_obj.size, self.variant_data["size"])

    def test_variant_create_view_post_empty_data(self):
        response = self.client.post(reverse("mobiles:variant-create"), data={})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mobiles/variant/form.html")
        self.assertIsInstance(response.context["form"], VariantForm)
        self.assertEqual(
            dict(response.context["form"].errors.get_context()["errors"])["color"][0], "This field is required."
        )
        self.assertEqual(
            dict(response.context["form"].errors.get_context()["errors"])["size"][0], "This field is required."
        )
        self.assertEqual(
            dict(response.context["form"].errors.get_context()["errors"])["image"][0], "This field is required."
        )


class VariantUpdateViewTestCase(TestCase):
    brand: Brand

    def setUp(self):
        self.client = Client()
        self.nationality = Nationality.objects.create(name="Test Nationality")
        self.brand = Brand.objects.create(name="Test Brand", nationality=self.nationality)
        self.mobile = Mobile.objects.create(brand=self.brand, model="Test Model", country=self.nationality)
        self.variant_data = {"mobile": self.mobile, "color": "Test Color", "size": 5.5, "image": generate_image_file()}
        self.variant = Variant.objects.create(**self.variant_data)

    def tearDown(self) -> None:
        self.variant.image.delete()

    def test_variant_update_view_get(self):
        response = self.client.get(reverse("mobiles:variant-edit", args=(self.variant.pk,)))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mobiles/variant/form.html")
        self.assertIsInstance(response.context["form"], VariantForm)
        self.assertEqual(response.context["form"].instance, self.variant)

    def test_variant_update_view_get_invalid_instance(self):
        response = self.client.get(reverse("mobiles:variant-edit", args=(5,)))

        self.assertEqual(response.status_code, 404)

    def test_variant_update_view_post_valid_data(self):
        updated_data = {"mobile": self.mobile.pk, "color": "Updated Color", "size": 5.5}
        response = self.client.post(
            reverse("mobiles:variant-edit", args=(self.variant.pk,)), data=updated_data, follow=True
        )

        self.assertRedirects(response, reverse("mobiles:variant-list"))
        self.variant.refresh_from_db()
        self.assertEqual(self.variant.color, updated_data["color"])
        self.assertEqual(self.variant.size, updated_data["size"])
        self.assertEqual(str(list(response.context["messages"])[0]), "Variant updated successfully.")

    def test_variant_update_view_post_invalid_data(self):
        response = self.client.post(reverse("mobiles:variant-edit", args=(self.variant.pk,)), data={})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mobiles/variant/form.html")
        self.assertIsInstance(response.context["form"], VariantForm)
        self.assertEqual(
            dict(response.context["form"].errors.get_context()["errors"])["color"][0], "This field is required."
        )
        self.assertEqual(
            dict(response.context["form"].errors.get_context()["errors"])["size"][0], "This field is required."
        )
        self.assertEqual(
            dict(response.context["form"].errors.get_context()["errors"])["mobile"][0], "This field is required."
        )

    def test_variant_update_view_post_invalid_instance(self):
        updated_data = {"mobile": self.mobile.pk, "color": "Updated Color", "size": 5.5}
        response = self.client.post(reverse("mobiles:variant-edit", args=(5,)), data=updated_data)

        self.assertEqual(response.status_code, 404)


class VariantDeleteViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.nationality = Nationality.objects.create(name="Test Nationality")
        self.brand = Brand.objects.create(name="Test Brand", nationality=self.nationality)
        self.mobile = Mobile.objects.create(brand=self.brand, model="Test Model", country=self.nationality)
        self.variant = Variant.objects.create(
            mobile=self.mobile, color="Test Color", size=5.5, image=generate_image_file()
        )

    def tearDown(self) -> None:
        self.variant.image.delete()

    def test_variant_delete_view_post(self):
        response = self.client.post(reverse("mobiles:variant-delete", args=(self.variant.pk,)), follow=True)

        self.assertRedirects(response, reverse("mobiles:variant-list"))
        self.assertEqual(Variant.objects.count(), 0)
        self.assertEqual(str(list(response.context["messages"])[0]), "Variant deleted successfully.")

    def test_variant_delete_view_post_invalid_instance(self):
        response = self.client.post(reverse("mobiles:variant-delete", args=(5,)), follow=True)

        self.assertEqual(response.status_code, 404)
