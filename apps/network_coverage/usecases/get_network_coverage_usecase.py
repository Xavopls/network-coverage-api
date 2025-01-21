from geopy.distance import geodesic
from apps.address_lookup.services import france_address_service
from apps.network_coverage.models.network_coverage import NetworkCoverage


class GetNetworkCoverage:

    def execute(self, address: str) -> dict:

        target_coords = self.__fetch_coords(address)

        db_data = NetworkCoverage.objects.values(
            "id", "latitude", "longitude", "operator", "g2", "g3", "g4"
        )

        operator_closest_records = self.__get_closest_operators(db_data, target_coords)

        result = {
            operator: data["coverage"]
            for operator, data in operator_closest_records.items()
        }

        return result

    def __get_closest_operators(self, db_data, target_coords):
        # Group records by operator and calculate distances
        operator_closest_records = {}
        for record in db_data:
            record_coords = (record["latitude"], record["longitude"])
            distance = geodesic(target_coords, record_coords).meters

            # Update the closest record for the operator if it's closer
            operator = record["operator"]
            if (
                    operator not in operator_closest_records
                    or distance < operator_closest_records[operator]["distance"]
            ):
                operator_closest_records[operator] = {
                    "distance": distance,
                    "coverage": {
                        "2G": record["g2"],
                        "3G": record["g3"],
                        "4G": record["g4"],
                    },
                }
        return operator_closest_records

    def __fetch_coords(self, address):
        # Step 1: Get coordinates from the address
        address_data = france_address_service.get_address_details(address)
        if not address_data:
            raise ValueError(f"Coordinates for the given address {address} were not found.")
        # Extract latitude and longitude from the address data
        target_coords = (address_data["latitude"], address_data["longitude"])
        return target_coords
