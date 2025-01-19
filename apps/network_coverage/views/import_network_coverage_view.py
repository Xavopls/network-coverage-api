from drf_spectacular.utils import extend_schema, OpenApiTypes, OpenApiParameter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..usecases.post_import_network_coverage_usecase import PostImportNetworkCoverageUseCase
from rest_framework import permissions


class ImportNetworkCoverageView(APIView):

    permission_classes = (permissions.AllowAny,)

    @extend_schema(
        operation_id="Import Network Coverage",
        summary="Upload CSV to import network coverage data",
        description=(
                "This endpoint accepts a CSV file with network coverage data. "
                "It parses the file, validates the data, converts Lambert93 coordinates to GPS, "
                "and saves it to the database."
        ),
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'file': {
                        'type': 'string',
                        'format': 'binary'
                    }
                }
            }
        },
        responses={
            201: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
        },
    )
    def post(self, request):
        file = request.FILES.get('file')

        if not file:
            return Response(
                {"detail": "File not provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            import_networks_usecase = PostImportNetworkCoverageUseCase()
            records_imported = import_networks_usecase.execute(file)
            return Response(
                {"detail": f"Successfully imported {records_imported} records."},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )