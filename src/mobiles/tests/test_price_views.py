from django.test import Client, TestCase
from django.urls import reverse

from mobiles.forms import PriceHistoryForm
from mobiles.models import Brand, Mobile, Nationality, PriceHistory, Variant
from mobiles.tests.util import generate_image_file


class PriceHistoryListViewTestCase(TestCase):
    nationality: Nationality
    brand: Brand
    mobile: Mobile
    variant: Variant

    @classmethod
    def setUpTestData(cls):
        cls.nationality = Nationality.objects.create(name="Test Nationality")
        cls.brand = Brand.objects.create(name="Test Brand", nationality=cls.nationality)
        cls.mobile = Mobile.objects.create(brand=cls.brand, model="Test Mobile", country=cls.nationality)
        cls.variant = Variant.objects.create(mobile=cls.mobile, color="Red", size=6.2, image=generate_image_file())

    @classmethod
    def tearDownClass(cls):
        cls.variant.delete()
        super().tearDownClass()

    def setUp(self):
        self.client = Client()
        for i in range(15):
            PriceHistory.objects.create(variant=self.variant, price=100 + i, status=True, date="2023-07-27")

    def test_price_history_list_view_pagination_first_page(self):
        response = self.client.get(reverse("mobiles:price-history-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "100")
        self.assertContains(response, "109")
        self.assertNotContains(response, "110")

    def test_price_history_list_view_pagination_second_page(self):
        response = self.client.get(reverse("mobiles:price-history-list"), {"page": 2})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "110")
        self.assertContains(response, "114")
        self.assertNotContains(response, "100")

    def test_price_history_list_view_pagination_invalid_page_number(self):
        response = self.client.get(reverse("mobiles:price-history-list"), {"page": 3})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "110")
        self.assertContains(response, "114")
        self.assertNotContains(response, "100")

    def test_price_history_list_view_with_no_price_histories(self):
        PriceHistory.objects.all().delete()
        response = self.client.get(reverse("mobiles:price-history-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No price histories found.")


class PriceHistoryCreateViewTestCase(TestCase):
    nationality: Nationality
    brand: Brand
    mobile: Mobile
    variant: Variant

    @classmethod
    def setUpTestData(cls):
        cls.nationality = Nationality.objects.create(name="Test Nationality")
        cls.brand = Brand.objects.create(name="Test Brand", nationality=cls.nationality)
        cls.mobile = Mobile.objects.create(brand=cls.brand, model="Test Mobile", country=cls.nationality)
        cls.variant = Variant.objects.create(mobile=cls.mobile, color="Red", size=6.2, image=generate_image_file())

    @classmethod
    def tearDownClass(cls):
        cls.variant.delete()
        super().tearDownClass()

    def setUp(self):
        self.client = Client()

    def test_price_history_create_view_get(self):
        response = self.client.get(reverse("mobiles:price-history-create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mobiles/price_history/form.html")
        self.assertIsInstance(response.context["form"], PriceHistoryForm)

    def test_price_history_create_view_post_valid_data(self):
        price_history_data = {"variant": self.variant.pk, "price": 999, "status": True, "date": "2023-07-27"}
        response = self.client.post(reverse("mobiles:price-history-create"), data=price_history_data, follow=True)

        self.assertRedirects(response, reverse("mobiles:price-history-list"))
        self.assertEqual(PriceHistory.objects.count(), 1)
        price_history = PriceHistory.objects.first()
        self.assertEqual(price_history.variant, self.variant)
        self.assertEqual(price_history.price, 999)
        self.assertEqual(price_history.status, True)
        self.assertEqual(price_history.date.strftime("%Y-%m-%d"), "2023-07-27")
        self.assertEqual(str(list(response.context["messages"])[0]), "Price History created successfully.")

    def test_price_history_create_view_post_invalid_data(self):
        response = self.client.post(reverse("mobiles:price-history-create"), data={})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mobiles/price_history/form.html")
        self.assertIsInstance(response.context["form"], PriceHistoryForm)
        self.assertEqual(
            dict(response.context["form"].errors.get_context()["errors"])["variant"][0], "This field is required."
        )
        self.assertEqual(
            dict(response.context["form"].errors.get_context()["errors"])["price"][0], "This field is required."
        )
        self.assertEqual(
            dict(response.context["form"].errors.get_context()["errors"])["date"][0], "This field is required."
        )


class PriceHistoryUpdateViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.nationality = Nationality.objects.create(name="Test Nationality")
        self.brand = Brand.objects.create(name="Test Brand", nationality=self.nationality)
        self.mobile = Mobile.objects.create(brand=self.brand, model="Test Mobile", country=self.nationality)
        self.variant = Variant.objects.create(mobile=self.mobile, color="Red", size=6.2, image=generate_image_file())
        self.price_history = PriceHistory.objects.create(
            variant=self.variant, price=999, status=True, date="2023-07-27"
        )

    def tearDown(self) -> None:
        self.variant.delete()

    def test_price_history_update_view_get(self):
        response = self.client.get(reverse("mobiles:price-history-edit", args=(self.price_history.pk,)))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mobiles/price_history/form.html")
        self.assertIsInstance(response.context["form"], PriceHistoryForm)
        self.assertEqual(response.context["form"].instance, self.price_history)

    def test_price_history_update_view_get_invalid_instance(self):
        response = self.client.get(reverse("mobiles:price-history-edit", args=(5,)))

        self.assertEqual(response.status_code, 404)

    def test_price_history_update_view_post_valid_data(self):
        updated_data = {"variant": self.variant.pk, "price": 899, "status": False, "date": "2023-07-28"}
        response = self.client.post(
            reverse("mobiles:price-history-edit", args=(self.price_history.pk,)), data=updated_data, follow=True
        )

        self.assertRedirects(response, reverse("mobiles:price-history-list"))
        self.price_history.refresh_from_db()
        self.assertEqual(self.price_history.price, 899)
        self.assertEqual(self.price_history.status, False)
        self.assertEqual(self.price_history.date.strftime("%Y-%m-%d"), "2023-07-28")
        self.assertEqual(str(list(response.context["messages"])[0]), "Price History updated successfully.")

    def test_price_history_update_view_post_invalid_data(self):
        response = self.client.post(reverse("mobiles:price-history-edit", args=(self.price_history.pk,)), data={})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mobiles/price_history/form.html")
        self.assertIsInstance(response.context["form"], PriceHistoryForm)
        self.assertEqual(
            dict(response.context["form"].errors.get_context()["errors"])["variant"][0], "This field is required."
        )
        self.assertEqual(
            dict(response.context["form"].errors.get_context()["errors"])["price"][0], "This field is required."
        )
        self.assertEqual(
            dict(response.context["form"].errors.get_context()["errors"])["date"][0], "This field is required."
        )

    def test_price_history_update_view_post_invalid_instance(self):
        updated_data = {"variant": self.variant.pk, "price": 899, "status": False, "date": "2023-07-28"}
        response = self.client.post(reverse("mobiles:price-history-edit", args=(5,)), data=updated_data)

        self.assertEqual(response.status_code, 404)


class PriceHistoryDeleteViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.nationality = Nationality.objects.create(name="Test Nationality")
        self.brand = Brand.objects.create(name="Test Brand", nationality=self.nationality)
        self.mobile = Mobile.objects.create(brand=self.brand, model="Test Mobile", country=self.nationality)
        self.variant = Variant.objects.create(mobile=self.mobile, color="Red", size=6.2, image=generate_image_file())
        self.price_history = PriceHistory.objects.create(
            variant=self.variant, price=999, status=True, date="2023-07-27"
        )

    def tearDown(self) -> None:
        self.variant.delete()

    def test_price_history_delete_view_post(self):
        response = self.client.post(reverse("mobiles:price-history-delete", args=(self.price_history.pk,)), follow=True)

        self.assertRedirects(response, reverse("mobiles:price-history-list"))
        self.assertEqual(PriceHistory.objects.count(), 0)
        self.assertEqual(str(list(response.context["messages"])[0]), "Price History deleted successfully.")

    def test_price_history_delete_view_post_invalid_instance(self):
        response = self.client.post(reverse("mobiles:price-history-delete", args=(5,)), follow=True)

        self.assertEqual(response.status_code, 404)
