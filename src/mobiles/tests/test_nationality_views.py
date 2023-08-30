from django.test import TestCase
from django.urls import reverse

from mobiles.forms import NationalityForm
from mobiles.models import Nationality


class NationalityListViewTestCase(TestCase):
    def setUp(self):
        for i in range(15):
            Nationality.objects.create(name=f"Nationality {i}")

    def test_pagination_first_page(self):
        response = self.client.get(reverse("mobiles:nationality-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nationality 0")
        self.assertContains(response, "Nationality 9")
        self.assertNotContains(response, "Nationality 10")

    def test_pagination_second_page(self):
        response = self.client.get(reverse("mobiles:nationality-list"), {"page": 2})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nationality 10")
        self.assertContains(response, "Nationality 14")
        self.assertNotContains(response, "Nationality 0")

    def test_pagination_invalid_page_number(self):
        response = self.client.get(reverse("mobiles:nationality-list"), {"page": 3})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nationality 10")
        self.assertContains(response, "Nationality 14")
        self.assertNotContains(response, "Nationality 0")


class NationalityCreateViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.nationality_data = {"name": "Test Nationality"}

    def test_nationality_create_view_get(self):
        response = self.client.get(reverse("mobiles:nationality-create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mobiles/nationality/form.html")
        self.assertIsInstance(response.context["form"], NationalityForm)

    def test_nationality_create_view_post_valid_data(self):
        response = self.client.post(reverse("mobiles:nationality-create"), data=self.nationality_data, follow=True)

        self.assertRedirects(response, reverse("mobiles:nationality-list"))
        self.assertEqual(Nationality.objects.count(), 1)
        self.assertEqual(Nationality.objects.last().name, self.nationality_data["name"])
        self.assertEqual(str(list(response.context["messages"])[0]), "Nationality created successfully.")

    def test_nationality_create_view_post_empty_data(self):
        response = self.client.post(reverse("mobiles:nationality-create"), data={})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mobiles/nationality/form.html")
        self.assertIsInstance(response.context["form"], NationalityForm)
        self.assertEqual(
            dict(response.context["form"].errors.get_context()["errors"])["name"][0], "This field is required."
        )


class NationalityUpdateViewTestCase(TestCase):
    def setUp(self):
        self.nationality_data = {"name": "Test Nationality"}
        self.nationality = Nationality.objects.create(name="Test Nationality")

    def test_nationality_update_view_get(self):
        response = self.client.get(reverse("mobiles:nationality-edit", args=(self.nationality.pk,)))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mobiles/nationality/form.html")
        self.assertIsInstance(response.context["form"], NationalityForm)
        self.assertEqual(response.context["form"].instance, self.nationality)

    def test_nationality_update_view_get_invalid_instance(self):
        response = self.client.get(reverse("mobiles:nationality-edit", args=(5,)))

        self.assertEqual(response.status_code, 404)

    def test_nationality_update_view_post_valid_data(self):
        updated_data = {"name": "Updated Nationality"}
        response = self.client.post(
            reverse("mobiles:nationality-edit", args=(self.nationality.pk,)), data=updated_data, follow=True
        )

        self.assertRedirects(response, reverse("mobiles:nationality-list"))
        self.nationality.refresh_from_db()
        self.assertEqual(self.nationality.name, updated_data["name"])
        self.assertEqual(str(list(response.context["messages"])[0]), "Nationality updated successfully.")

    def test_nationality_update_view_post_invalid_data(self):
        response = self.client.post(reverse("mobiles:nationality-edit", args=(self.nationality.pk,)), data={})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mobiles/nationality/form.html")
        self.assertIsInstance(response.context["form"], NationalityForm)
        self.assertEqual(
            dict(response.context["form"].errors.get_context()["errors"])["name"][0], "This field is required."
        )

    def test_nationality_update_view_post_invalid_instance(self):
        updated_data = {"name": "Updated Nationality"}
        response = self.client.post(reverse("mobiles:nationality-edit", args=(5,)), data=updated_data)

        self.assertEqual(response.status_code, 404)


class NationalityDeleteViewTestCase(TestCase):
    def setUp(self):
        self.nationality_data = {"name": "Test Nationality"}
        self.nationality = Nationality.objects.create(name="Test Nationality")

    def test_nationality_delete_view_post(self):
        response = self.client.post(reverse("mobiles:nationality-delete", args=(self.nationality.pk,)), follow=True)

        self.assertRedirects(response, reverse("mobiles:nationality-list"))
        self.assertEqual(Nationality.objects.count(), 0)
        self.assertEqual(str(list(response.context["messages"])[0]), "Nationality deleted successfully.")

    def test_nationality_delete_view_post_invalid_instance(self):
        response = self.client.post(reverse("mobiles:nationality-delete", args=(5,)), follow=True)

        self.assertEqual(response.status_code, 404)
