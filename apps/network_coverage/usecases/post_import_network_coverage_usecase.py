from io import StringIO
import csv
from datetime import datetime

from django.db import transaction

from apps.network_coverage.utils.coordinate_converter import CoordinateConverter
from ..models.network_coverage import NetworkCoverage
from ..serializers.network_coverage_serializer import NetworkCoverageSerializer
from ..utils.dictionaries import OPERATOR_CODES


class PostImportNetworkCoverageUseCase:

    CHUNK_SIZE = 300

    def execute(self, file):
        # Parse CSV
        csv_file = StringIO(file.read().decode('utf-8'))
        reader = csv.DictReader(csv_file, delimiter=';')
        records: [NetworkCoverageSerializer] = []
        row_amount = 0
        for row in reader:
            lat, lon, x_lp93, y_lp93 = self.handle_coordinates(row)
            operator = self.handle_operator(int(row['Operateur']))
            row_amount += 1
            # Prepare data for serialization
            record = {
                'operator': operator,
                'x_lp93': x_lp93,
                'y_lp93': y_lp93,
                'longitude': lon,
                'latitude': lat,
                'g2': bool(int(row['2G'])),
                'g3': bool(int(row['3G'])),
                'g4': bool(int(row['4G'])),
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }

            self.serialize_address(record, records)

            # Save in chunks
            if len(records) >= self.CHUNK_SIZE:
                self.bulk_save(records)
                records.clear()
        # Save any remaining records
        if records:
            self.bulk_save(records)
            records.clear()

        return row_amount

    @transaction.atomic
    def bulk_save(self, records):
        try:
            NetworkCoverage.objects.bulk_create(records, batch_size=self.CHUNK_SIZE)
        except Exception as e:
            print(f"Error during bulk save: {str(e)}")
            raise e

    def serialize_address(self, record, records):
        serializer = NetworkCoverageSerializer(data=record)
        if serializer.is_valid():
            instance = NetworkCoverage(**serializer.validated_data)
            records.append(instance)
        else:
            print(f"Invalid data: {serializer.errors}")
            raise ValueError(f"Invalid data: {serializer.errors}")

    def handle_coordinates(self, row):
        x_lp93 = int(row['x'])
        y_lp93 = int(row['y'])
        lon, lat = CoordinateConverter().lamber93_to_gps(x_lp93, y_lp93)
        return lat, lon, x_lp93, y_lp93

    def handle_operator(self, id: int) -> str:
        return OPERATOR_CODES.get(id, 'Unknown Operator')
