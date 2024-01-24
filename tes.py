# # import requests

# # response = requests.get('https://api64.ipify.org?format=json')
# # data = response.json()
# # public_ip = data.get('ip', '')
# # response = requests.get('http://apiip.net/api/check?ip='+public_ip+'&accessKey=5d67333e-8775-434b-8b31-7fe4a5e3da3a')
# # data = response.json()
# # city = data['city']
# # country_code = data['countryCode']

# # print(city)
# # print(country_code)



# from geopy.geocoders import Nominatim
# import geocoder

# # def get_city_from_coordinates(latitude, longitude):
# #     # Buat objek geolocator
# #     geolocator = Nominatim(user_agent="my_geocoder")

# #     # Dapatkan informasi lokasi berdasarkan koordinat
# #     location = geolocator.reverse((latitude, longitude), language="en")

# #     if location:
# #         address = location.address
# #         # Ambil informasi kota dari alamat
# #         city = location.raw.get("address", {}).get("city", "")
# #         city = location.raw.get("address", {}).get("city", "")
# #         return city
# #     else:
# #         return None

# def main():
    
#     g = geocoder.ip('me')
#     t = g.latlng
#     latitude, longitude = t[0], t[1]

#     # Dapatkan informasi kota dari koordinat
#     geolocator = Nominatim(user_agent="my_geocoder")

#     # Dapatkan informasi lokasi berdasarkan koordinat
#     location = geolocator.reverse((latitude, longitude), language="en")

#     print(location)

# if __name__ == "__main__":
#     main()

from geopy.geocoders import Nominatim

def get_current_location():
    geolocator = Nominatim(user_agent="my_geocoder")

    try:
        # Mendapatkan lokasi saat ini berdasarkan GPS atau Wi-Fi
        location = geolocator.geocode(" ", timeout=50)
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
