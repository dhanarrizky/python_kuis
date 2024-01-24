from geopy.geocoders import Nominatim

def get_current_location():
    try:
        geolocator = Nominatim(user_agent="my_geocoder")
        location = geolocator.geocode("0,0", language="en", exactly_one=True)

        return location

    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    current_location = get_current_location()

    if current_location:
        print("Latitude:", current_location.latitude)
        print("Longitude:", current_location.longitude)
        print("City:", current_location.address.split(",")[-3].strip())

    else:
        print("Tidak dapat mendapatkan informasi lokasi.")

if __name__ == "__main__":
    main()
