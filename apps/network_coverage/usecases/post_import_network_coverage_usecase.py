from io import StringIO
import csv
from datetime import datetime

from apps.network_coverage.utils.coordinate_converter import CoordinateConverter
from ..serializers.network_coverage_serializer import NetworkCoverageSerializer
from ..utils.dictionaries import OPERATOR_CODES


class PostImportNetworkCoverageUseCase:

    def execute(self, file):
        # Parse CSV
        csv_file = StringIO(file.read().decode('utf-8'))
        reader = csv.DictReader(csv_file, delimiter=';')
        records: [NetworkCoverageSerializer] = []

        for row in reader:
            lat, lon, x_lp93, y_lp93 = self.handle_coordinates(row)
            operator = self.handle_operator(int(row['Operateur']))

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

        # Save all valid records to the DB
        for serializer in records:
            try:
                serializer.save()
            except Exception as e:
                print(f"Error saving record {serializer.validated_data}: {str(e)}")
                raise e

        return len(records)

    def serialize_address(self, record, records):
        serializer = NetworkCoverageSerializer(data=record)
        if serializer.is_valid():
            records.append(serializer)
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
