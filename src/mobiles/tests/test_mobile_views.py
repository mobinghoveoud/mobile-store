from django.test import TestCase
from django.urls import reverse

from mobiles.forms import MobileForm
from mobiles.models import Brand, Mobile, Nationality


class MobileListViewTestCase(TestCase):
    def setUp(self):
        for i in range(15):
            nationality = Nationality.objects.create(name=f"Nationality {i}")
            brand = Brand.objects.create(name=f"Brand {i}", nationality=nationality)
            Mobile.objects.create(brand=brand, model=f"Model {i}", country=nationality)

    def test_pagination_first_page(self):
        response = self.client.get(reverse("mobiles:mobile-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Model 0")
        self.assertContains(response, "Model 9")
        self.assertNotContains(response, "Model 10")

    def test_pagination_second_page(self):
        response = self.client.get(reverse("mobiles:mobile-list"), {"page": 2})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Model 10")
        self.assertContains(response, "Model 14")
        self.assertNotContains(response, "Model 0")

    def test_pagination_invalid_page_number(self):
        response = self.client.get(reverse("mobiles:mobile-list"), {"page": 3})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Model 10")
        self.assertContains(response, "Model 14")
        self.assertNotContains(response, "Model 0")


class MobileCreateViewTestCase(TestCase):
    brand: Brand
    nationality: Nationality

    @classmethod
    def setUpTestData(cls):
        cls.nationality = Nationality.objects.create(name="Test Nationality")
        cls.brand = Brand.objects.create(name="Test Brand", nationality=cls.nationality)
        cls.mobile_data = {"brand": cls.brand.pk, "model": "Test Model", "country": cls.nationality.pk}

    def test_mobile_create_view_get(self):
        response = self.client.get(reverse("mobiles:mobile-create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mobiles/mobile/form.html")
        self.assertIsInstance(response.context["form"], MobileForm)

    def test_mobile_create_view_post_valid_data(self):
        response = self.client.post(reverse("mobiles:mobile-create"), data=self.mobile_data, follow=True)

        self.assertRedirects(response, reverse("mobiles:mobile-list"))
        self.assertEqual(Mobile.objects.count(), 1)
        self.assertEqual(str(list(response.context["messages"])[0]), "Mobile created successfully.")
        last_obj = Mobile.objects.last()
        self.assertEqual(last_obj.model, self.mobile_data["model"])
        self.assertEqual(last_obj.brand.pk, self.mobile_data["brand"])
        self.assertEqual(last_obj.country.pk, self.mobile_data["country"])

    def test_mobile_create_view_post_empty_data(self):
        response = self.client.post(reverse("mobiles:mobile-create"), data={})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mobiles/mobile/form.html")
        self.assertIsInstance(response.context["form"], MobileForm)
        self.assertEqual(
            dict(response.context["form"].errors.get_context()["errors"])["model"][0], "This field is required."
        )
        self.assertEqual(
            dict(response.context["form"].errors.get_context()["errors"])["country"][0], "This field is required."
        )
        self.assertEqual(
            dict(response.context["form"].errors.get_context()["errors"])["brand"][0], "This field is required."
        )


class MobileUpdateViewTestCase(TestCase):
    def setUp(self):
        self.nationality = Nationality.objects.create(name="Test Nationality")
        self.brand = Brand.objects.create(name="Test Brand", nationality=self.nationality)
        self.mobile_data = {"brand": self.brand.pk, "model": "Test Model", "country": self.nationality.pk}
        self.mobile = Mobile.objects.create(brand=self.brand, model="Test Model", country=self.nationality)

    def test_mobile_update_view_get(self):
        response = self.client.get(reverse("mobiles:mobile-edit", args=(self.mobile.pk,)))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mobiles/mobile/form.html")
        self.assertIsInstance(response.context["form"], MobileForm)
        self.assertEqual(response.context["form"].instance, self.mobile)

    def test_mobile_update_view_get_invalid_instance(self):
        response = self.client.get(reverse("mobiles:mobile-edit", args=(5,)))

        self.assertEqual(response.status_code, 404)

    def test_mobile_update_view_post_valid_data(self):
        updated_data = {"brand": self.brand.pk, "model": "Updated Model", "country": self.nationality.pk}
        response = self.client.post(
            reverse("mobiles:mobile-edit", args=(self.mobile.pk,)), data=updated_data, follow=True
        )

        self.assertRedirects(response, reverse("mobiles:mobile-list"))
        self.mobile.refresh_from_db()
        self.assertEqual(self.mobile.model, updated_data["model"])
        self.assertEqual(self.mobile.country.pk, updated_data["country"])
        self.assertEqual(self.mobile.brand.pk, updated_data["brand"])
        self.assertEqual(str(list(response.context["messages"])[0]), "Mobile updated successfully.")

    def test_mobile_update_view_post_invalid_data(self):
        response = self.client.post(reverse("mobiles:mobile-edit", args=(self.mobile.pk,)), data={})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mobiles/mobile/form.html")
        self.assertIsInstance(response.context["form"], MobileForm)
        self.assertEqual(
            dict(response.context["form"].errors.get_context()["errors"])["model"][0], "This field is required."
        )
        self.assertEqual(
            dict(response.context["form"].errors.get_context()["errors"])["country"][0], "This field is required."
        )
        self.assertEqual(
            dict(response.context["form"].errors.get_context()["errors"])["brand"][0], "This field is required."
        )

    def test_mobile_update_view_post_invalid_instance(self):
        updated_data = {"brand": self.brand.pk, "model": "Updated Model", "country": self.nationality.pk}
        response = self.client.post(reverse("mobiles:mobile-edit", args=(5,)), data=updated_data)

        self.assertEqual(response.status_code, 404)


class MobileDeleteViewTestCase(TestCase):
    def setUp(self):
        self.nationality = Nationality.objects.create(name="Test Nationality")
        self.brand = Brand.objects.create(name="Test Brand", nationality=self.nationality)
        self.mobile_data = {"brand": self.brand.pk, "model": "Test Model", "country": self.nationality.pk}
        self.mobile = Mobile.objects.create(brand=self.brand, model="Test Model", country=self.nationality)

    def test_mobile_delete_view_post(self):
        response = self.client.post(reverse("mobiles:mobile-delete", args=(self.mobile.pk,)), follow=True)

        self.assertRedirects(response, reverse("mobiles:mobile-list"))
        self.assertEqual(Mobile.objects.count(), 0)
        self.assertEqual(str(list(response.context["messages"])[0]), "Mobile deleted successfully.")

    def test_mobile_delete_view_post_invalid_instance(self):
        response = self.client.post(reverse("mobiles:mobile-delete", args=(5,)), follow=True)

        self.assertEqual(response.status_code, 404)
