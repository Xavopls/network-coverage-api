from geopy.distance import geodesic
from apps.address_lookup.services import france_address_service
from apps.network_coverage.models.network_coverage import NetworkCoverage


class GetNetworkCoverage:

    def execute(self, address: str) -> dict:
        # Step 1: Get coordinates from the address
        address_data = france_address_service.get_address_details(address)
        if not address_data:
            raise ValueError(f"Coordinates for the given address {address} were not found.")

        # Extract latitude and longitude from the address data
        target_coords = (address_data["latitude"], address_data["longitude"])

        # Step 2: Fetch coverage data from the database
        data = NetworkCoverage.objects.values(
            "id", "latitude", "longitude", "operator", "g2", "g3", "g4"
        )

        # Group records by operator and calculate distances
        operator_closest_records = {}
        for record in data:
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

        # Step 3: Build the final dictionary structure
        result = {
            operator: data["coverage"]
            for operator, data in operator_closest_records.items()
        }

        return result
