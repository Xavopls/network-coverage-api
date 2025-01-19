from drf_spectacular.utils import extend_schema, OpenApiTypes, OpenApiParameter
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from ..usecases.get_network_coverage_usecase import GetNetworkCoverage


class AddressView(APIView):

    permission_classes = (permissions.AllowAny,)

    @extend_schema(
        operation_id="Get Network Coverage by Address",
        summary="Retrieve network coverage data by address",
        description=(
                "Retrieve network coverage data for a given query parameter. "
                "The query parameter `q` should contain the address or location to search for coverage."
        ),
        parameters=[
            OpenApiParameter(
                name="q",
                description="Query parameter for searching network coverage by address",
                required=True,
                type=OpenApiTypes.STR,
            )
        ],
        responses={
            200: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
            500: OpenApiTypes.OBJECT,
        },
    )
    def get(self, request):
        query = request.GET.get("q")
        if not query:
            return Response({"error": "Missing address query parameter."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            use_case = GetNetworkCoverage()
            coverage_data = use_case.execute(query)
            return Response(coverage_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

