from django.test import TestCase
from django.urls import reverse

from mobiles.forms import BrandForm
from mobiles.models import Brand, Nationality


class BrandListViewTestCase(TestCase):
    def setUp(self):
        for i in range(15):
            nationality = Nationality.objects.create(name=f"Nationality {i}")
            Brand.objects.create(name=f"Brand {i}", nationality=nationality)

    def test_pagination_first_page(self):
        response = self.client.get(reverse("mobiles:brand-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brand 0")
        self.assertContains(response, "Brand 9")
        self.assertNotContains(response, "Brand 10")

    def test_pagination_second_page(self):
        response = self.client.get(reverse("mobiles:brand-list"), {"page": 2})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brand 10")
        self.assertContains(response, "Brand 14")
        self.assertNotContains(response, "Brand 0")

    def test_pagination_invalid_page_number(self):
        response = self.client.get(reverse("mobiles:brand-list"), {"page": 3})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brand 10")
        self.assertContains(response, "Brand 14")
        self.assertNotContains(response, "Brand 0")


class BrandCreateViewTestCase(TestCase):
    nationality: Nationality

    @classmethod
    def setUpTestData(cls):
        cls.nationality = Nationality.objects.create(name="Test Nationality")
        cls.brand_data = {"name": "Test Brand", "nationality": cls.nationality.pk}

    def test_brand_create_view_get(self):
        response = self.client.get(reverse("mobiles:brand-create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mobiles/brand/form.html")
        self.assertIsInstance(response.context["form"], BrandForm)

    def test_brand_create_view_post_valid_data(self):
        response = self.client.post(reverse("mobiles:brand-create"), data=self.brand_data, follow=True)

        self.assertRedirects(response, reverse("mobiles:brand-list"))
        self.assertEqual(Brand.objects.count(), 1)
        self.assertEqual(str(list(response.context["messages"])[0]), "Brand created successfully.")
        last_obj = Brand.objects.last()
        self.assertEqual(last_obj.name, self.brand_data["name"])
        self.assertEqual(last_obj.nationality.pk, self.brand_data["nationality"])

    def test_brand_create_view_post_empty_data(self):
        response = self.client.post(reverse("mobiles:brand-create"), data={})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mobiles/brand/form.html")
        self.assertIsInstance(response.context["form"], BrandForm)
        self.assertEqual(
            dict(response.context["form"].errors.get_context()["errors"])["name"][0], "This field is required."
        )
        self.assertEqual(
            dict(response.context["form"].errors.get_context()["errors"])["nationality"][0], "This field is required."
        )


class BrandUpdateViewTestCase(TestCase):
    def setUp(self):
        self.nationality = Nationality.objects.create(name="Test Nationality")
        self.brand_data = {"name": "Test Brand", "nationality": self.nationality.pk}
        self.brand = Brand.objects.create(name="Test Brand", nationality=self.nationality)

    def test_brand_update_view_get(self):
        response = self.client.get(reverse("mobiles:brand-edit", args=(self.brand.pk,)))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mobiles/brand/form.html")
        self.assertIsInstance(response.context["form"], BrandForm)
        self.assertEqual(response.context["form"].instance, self.brand)

    def test_brand_update_view_get_invalid_instance(self):
        response = self.client.get(reverse("mobiles:brand-edit", args=(5,)))

        self.assertEqual(response.status_code, 404)

    def test_brand_update_view_post_valid_data(self):
        updated_data = {"name": "Updated Brand", "nationality": self.nationality.pk}
        response = self.client.post(
            reverse("mobiles:brand-edit", args=(self.brand.pk,)), data=updated_data, follow=True
        )

        self.assertRedirects(response, reverse("mobiles:brand-list"))
        self.brand.refresh_from_db()
        self.assertEqual(self.brand.name, updated_data["name"])
        self.assertEqual(self.brand.nationality.pk, updated_data["nationality"])
        self.assertEqual(str(list(response.context["messages"])[0]), "Brand updated successfully.")

    def test_brand_update_view_post_invalid_data(self):
        response = self.client.post(reverse("mobiles:brand-edit", args=(self.brand.pk,)), data={})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mobiles/brand/form.html")
        self.assertIsInstance(response.context["form"], BrandForm)
        self.assertEqual(
            dict(response.context["form"].errors.get_context()["errors"])["name"][0], "This field is required."
        )

    def test_brand_update_view_post_invalid_instance(self):
        updated_data = {"name": "Updated Brand", "nationality": self.nationality.pk}
        response = self.client.post(reverse("mobiles:brand-edit", args=(5,)), data=updated_data)

        self.assertEqual(response.status_code, 404)


class BrandDeleteViewTestCase(TestCase):
    def setUp(self):
        self.nationality = Nationality.objects.create(name="Test Nationality")
        self.brand_data = {"name": "Test Brand", "nationality": self.nationality.pk}
        self.brand = Brand.objects.create(name="Test Brand", nationality=self.nationality)

    def test_brand_delete_view_post(self):
        response = self.client.post(reverse("mobiles:brand-delete", args=(self.brand.pk,)), follow=True)

        self.assertRedirects(response, reverse("mobiles:brand-list"))
        self.assertEqual(Brand.objects.count(), 0)
        self.assertEqual(str(list(response.context["messages"])[0]), "Brand deleted successfully.")

    def test_brand_delete_view_post_invalid_instance(self):
        response = self.client.post(reverse("mobiles:brand-delete", args=(5,)), follow=True)

        self.assertEqual(response.status_code, 404)
