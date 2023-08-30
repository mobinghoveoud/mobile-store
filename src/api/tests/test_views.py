from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from mobiles.models import Brand, Mobile, Nationality, PriceHistory, Variant
from mobiles.serializers import BrandSerializer, MobileSerializer
from mobiles.tests.util import generate_image_file


class KoreaBrandsViewTestCase(APITestCase):
    def setUp(self):
        self.nationality_korea = Nationality.objects.create(name="Korea")
        self.nationality_usa = Nationality.objects.create(name="USA")

        self.brand1 = Brand.objects.create(name="Brand1", nationality=self.nationality_korea)
        self.brand2 = Brand.objects.create(name="Brand2", nationality=self.nationality_usa)

        self.mobile1 = Mobile.objects.create(brand=self.brand1, model="Model1", country=self.nationality_korea)
        self.mobile2 = Mobile.objects.create(brand=self.brand2, model="Model2", country=self.nationality_usa)

        self.variant1 = Variant.objects.create(mobile=self.mobile1, color="Red", size=5.5, image=generate_image_file())
        self.variant2 = Variant.objects.create(mobile=self.mobile1, color="Blue", size=6.0, image=generate_image_file())
        self.variant3 = Variant.objects.create(
            mobile=self.mobile2, color="Green", size=6.5, image=generate_image_file()
        )

        self.price_history1 = PriceHistory.objects.create(variant=self.variant1, price=1000, status=True)
        self.price_history2 = PriceHistory.objects.create(variant=self.variant1, price=1200, status=False)
        self.price_history3 = PriceHistory.objects.create(variant=self.variant2, price=800, status=True)

    def tearDown(self) -> None:
        Brand.objects.all().delete()

    def test_get_korea_brands(self):
        response = self.client.get(reverse("api:korea-brands"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertListEqual(response.data, BrandSerializer([self.brand1], many=True).data)

    def test_get_korea_brands_multiple(self):
        brand3 = Brand.objects.create(name="Brand3", nationality=self.nationality_korea)
        brand4 = Brand.objects.create(name="Brand4", nationality=self.nationality_korea)

        response = self.client.get(reverse("api:korea-brands"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertListEqual(response.data, BrandSerializer([self.brand1, brand3, brand4], many=True).data)

    def test_get_korea_brands_flat(self):
        url = reverse("api:korea-brands") + "?flat=1"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, BrandSerializer([self.brand1], many=True, flat=1).data)

    def test_get_korea_brands_multiple_flat(self):
        brand3 = Brand.objects.create(name="Brand3", nationality=self.nationality_korea)
        brand4 = Brand.objects.create(name="Brand4", nationality=self.nationality_korea)

        url = reverse("api:korea-brands") + "?flat=1"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertListEqual(response.data, BrandSerializer([self.brand1, brand3, brand4], many=True, flat=1).data)

    def test_invalid_flat_parameter(self):
        url = reverse("api:korea-brands") + "?flat=True"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertDictEqual(response.data, {"error": "Parameter 'flat' is invalid!"})

    def test_missing_flat_parameter(self):
        response = self.client.get(reverse("api:korea-brands"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MobileBrandsViewTestCase(APITestCase):
    def setUp(self):
        self.nationality_korea = Nationality.objects.create(name="Korea")
        self.nationality_usa = Nationality.objects.create(name="USA")

        self.brand1 = Brand.objects.create(name="Brand1", nationality=self.nationality_korea)
        self.brand2 = Brand.objects.create(name="Brand2", nationality=self.nationality_usa)

        self.mobile1 = Mobile.objects.create(brand=self.brand1, model="Model1", country=self.nationality_korea)
        self.mobile2 = Mobile.objects.create(brand=self.brand2, model="Model2", country=self.nationality_usa)

        self.variant1 = Variant.objects.create(mobile=self.mobile1, color="Red", size=5.5)
        self.variant2 = Variant.objects.create(mobile=self.mobile1, color="Blue", size=6.0)
        self.variant3 = Variant.objects.create(mobile=self.mobile2, color="Green", size=6.5)

        self.price_history1 = PriceHistory.objects.create(variant=self.variant1, price=1000, status=True)
        self.price_history2 = PriceHistory.objects.create(variant=self.variant1, price=1200, status=False)
        self.price_history3 = PriceHistory.objects.create(variant=self.variant2, price=800, status=True)

    def tearDown(self) -> None:
        Brand.objects.all().delete()

    def test_get_mobiles_by_brand(self):
        url = reverse("api:mobile-brands")
        response = self.client.get(url + "?brands=Brand1")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertListEqual(response.data, MobileSerializer([self.mobile1], many=True).data)

    def test_get_mobiles_by_brands(self):
        url = reverse("api:mobile-brands")
        response = self.client.get(url + "?brands=Brand1,Brand2")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertListEqual(response.data, MobileSerializer([self.mobile1, self.mobile2], many=True).data)

    def test_get_mobiles_by_brand_flat(self):
        url = reverse("api:mobile-brands") + "?brands=Brand1&flat=1"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertListEqual(response.data, MobileSerializer([self.mobile1], many=True, flat=1).data)

    def test_get_mobiles_by_brands_flat(self):
        url = reverse("api:mobile-brands") + "?brands=Brand1,Brand2&flat=1"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertListEqual(response.data, MobileSerializer([self.mobile1, self.mobile2], many=True, flat=1).data)

    def test_get_mobiles_by_brand_missing_brands_parameter(self):
        response = self.client.get(reverse("api:mobile-brands"))

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertDictEqual(response.data, {"error": "Parameter 'brands' is missing!"})

    def test_get_mobiles_by_brand_invalid_brand(self):
        url = reverse("api:mobile-brands")
        response = self.client.get(url + "?brands=InvalidBrand")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_mobiles_by_brand_invalid_brand_separation(self):
        url = reverse("api:mobile-brands")
        response = self.client.get(url + "?brands=Brand1|Brand2")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_invalid_flat_parameter(self):
        url = reverse("api:korea-brands") + "?flat=True"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertDictEqual(response.data, {"error": "Parameter 'flat' is invalid!"})


class SameNationalityViewTestCase(APITestCase):
    def setUp(self):
        self.nationality_korea = Nationality.objects.create(name="Korea")
        self.nationality_usa = Nationality.objects.create(name="USA")

        self.brand1 = Brand.objects.create(name="Brand1", nationality=self.nationality_korea)
        self.brand2 = Brand.objects.create(name="Brand2", nationality=self.nationality_usa)

        self.mobile1 = Mobile.objects.create(brand=self.brand1, model="Model1", country=self.nationality_korea)
        self.mobile2 = Mobile.objects.create(brand=self.brand1, model="Model2", country=self.nationality_usa)
        self.mobile3 = Mobile.objects.create(brand=self.brand2, model="Model3", country=self.nationality_korea)
        self.mobile4 = Mobile.objects.create(brand=self.brand2, model="Model4", country=self.nationality_usa)

    def test_get_mobiles_same_nationality(self):
        response = self.client.get(reverse("api:same-nationality"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertListEqual(response.data, MobileSerializer([self.mobile1, self.mobile4], many=True).data)

    def test_get_mobiles_same_nationality_flat(self):
        url = reverse("api:same-nationality") + "?flat=1"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertListEqual(response.data, MobileSerializer([self.mobile1, self.mobile4], many=True, flat=1).data)

    def test_invalid_flat_parameter(self):
        url = reverse("api:same-nationality") + "?flat=True"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertDictEqual(response.data, {"error": "Parameter 'flat' is invalid!"})
