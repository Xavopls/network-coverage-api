from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .usecases.get_network_coverage_usecase import GetNetworkCoverage
from .usecases.post_import_network_coverage_usecase import PostImportNetworkCoverageUseCase


class NetworkCoverageView(APIView):
    def get_network_coverage(request):
        query = request.GET.get("q")
        if not query:
            return JsonResponse({"error": "Missing address query parameter"}, status=400)

        use_case = GetNetworkCoverage()
        try:
            coverage_data = use_case.execute(query)
            return JsonResponse(coverage_data)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


    def post_import_network_coverage(request):
        @extend_schema(
            operation_id="Import Network Coverage",
            summary="Upload CSV to import network coverage data",
            description=(
                    "This endpoint accepts a CSV file with network coverage data. "
                    "It parses the file, validates the data, converts Lambert93 coordinates to GPS, "
                    "and saves it to the database."
            ),
            request={"multipart/form-data": {"file": "file"}},
            responses={201: "Successfully imported data.", 400: "Bad Request."},
        )
        def post(self, request):
            file = request.FILES.get('file')

            if not file:
                return Response(
                    {"detail": "File not provided."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                usecase = PostImportNetworkCoverageUseCase()
                records_imported = usecase.execute(file)
                return Response(
                    {"detail": f"Successfully imported {records_imported} records."},
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return Response(
                    {"detail": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
