from apps.address_lookup.services import france_address_service


class GetNetworkCoverage:

    def execute(self, address: str) -> dict:
        # Step 1: Get coordinates from the address
        address_data = france_address_service.get_address_details(address)
        if not address_data:
            raise ValueError(f"Coordinates for the given address {address} was not found.")



        # Step 2: Fetch coverage data from the database
        lat, lon = coordinates
        coverage_data = CoverageRepository.get_coverage_by_coordinates(lat, lon)
        if not coverage_data:
            raise ValueError("No coverage data found for the given coordinates")


        return {}

        #
        # # Step 3: Return formatted data
        # return coverage_data
