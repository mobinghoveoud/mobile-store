from django.db.models import F
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from mobiles.models import Brand, Mobile
from mobiles.serializers import BrandSerializer, MobileSerializer


class KoreaBrandsView(APIView):
    serializer_class = BrandSerializer

    @extend_schema(
        description="Get a list of brands from Korea along with their related mobiles and variants.",
        parameters=[
            OpenApiParameter(
                name="flat",
                type=int,
                location=OpenApiParameter.QUERY,
                description="Set to 1 to get the flat representation of the data.",
                required=False,
            ),
        ],
        responses={
            200: serializer_class(many=True),
            406: OpenApiResponse(
                response=dict,
                description="Flat parameter is missing.",
                examples=[OpenApiExample("406", {"error": "Parameter 'flat' is invalid!"})],
            ),
        },
    )
    def get(self, request):
        try:
            flat = int(request.GET.get("flat", 0))
        except ValueError:
            return Response({"error": "Parameter 'flat' is invalid!"}, status.HTTP_406_NOT_ACCEPTABLE)

        brands = Brand.objects.filter(nationality__name="Korea").prefetch_related("mobiles__variants__prices")

        serializer = self.serializer_class(brands, many=True, flat=flat)

        return Response(serializer.data, status=status.HTTP_200_OK)


class MobileBrandsView(APIView):
    serializer_class = MobileSerializer

    @extend_schema(
        description="Get a list of mobiles filtered by brand names.",
        parameters=[
            OpenApiParameter(
                name="brands",
                type=str,
                required=True,
                location=OpenApiParameter.QUERY,
                description="Comma-separated brand names to filter mobiles by.",
            ),
            OpenApiParameter(
                name="flat",
                type=int,
                required=False,
                location=OpenApiParameter.QUERY,
                description="Set to 1 to get the flat representation of the data.",
            ),
        ],
        responses={
            200: serializer_class(many=True),
            406: OpenApiResponse(
                response=dict,
                description="Flat parameter is missing.",
                examples=[OpenApiExample("406", {"error": "Parameter 'flat' is invalid!"})],
            ),
            422: OpenApiResponse(
                response=dict,
                description="Brands parameter is missing.",
                examples=[OpenApiExample("406", {"error": "Parameter 'brands' is missing!"})],
            ),
        },
    )
    def get(self, request):
        if "brands" in request.GET:
            brands_name = request.GET["brands"].split(",")
            try:
                flat = int(request.GET.get("flat", 0))
            except ValueError:
                return Response({"error": "Parameter 'flat' is invalid!"}, status.HTTP_406_NOT_ACCEPTABLE)

            mobiles = Mobile.objects.filter(brand__name__in=brands_name).prefetch_related("variants__prices")

            serializer = self.serializer_class(mobiles, many=True, flat=flat)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"error": "Parameter 'brands' is missing!"}, status.HTTP_422_UNPROCESSABLE_ENTITY)


class SameNationalityView(APIView):
    serializer_class = MobileSerializer

    @extend_schema(
        description="Get a list of mobiles with the same brand nationality and country.",
        parameters=[
            OpenApiParameter(
                name="flat",
                type=int,
                location=OpenApiParameter.QUERY,
                description="Set to 1 to get the flat representation of the data.",
                required=False,
            ),
        ],
        responses={
            200: serializer_class(many=True),
            406: OpenApiResponse(
                response=dict,
                description="Flat parameter is missing.",
                examples=[OpenApiExample("406", {"error": "Parameter 'flat' is invalid!"})],
            ),
        },
    )
    def get(self, request):
        try:
            flat = int(request.GET.get("flat", 0))
        except ValueError:
            return Response({"error": "Parameter 'flat' is invalid!"}, status.HTTP_406_NOT_ACCEPTABLE)

        mobiles = Mobile.objects.filter(brand__nationality=F("country")).prefetch_related("variants__prices")
        serializer = self.serializer_class(mobiles, many=True, flat=flat)

        return Response(serializer.data, status=status.HTTP_200_OK)
