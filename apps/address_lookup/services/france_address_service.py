import requests

def get_address_details(query: str) -> dict:
    base_url = 'https://data.geopf.fr/geocodage/search'

    params = {
        'q': query,
        'autocomplete': '1',
        'index': 'address',
        'limit': '10',
        'returntruegeometry': 'false'
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()

        data = response.json()

        # Extract the first latitude and longitude
        features = data.get("features", [])
        if features:
            first_feature = features[0]
            latitude = first_feature["geometry"]["coordinates"][1]
            longitude = first_feature["geometry"]["coordinates"][0]
            return {"latitude": latitude, "longitude": longitude}
        else:
            return {"error": "No results found"}

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return {"error": "Failed to fetch address details"}
