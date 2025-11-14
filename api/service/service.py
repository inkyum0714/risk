from api.data.Symbol import country_cities

def find_country_by_city(city_name):
    root = country_cities.get("children", []) if isinstance(country_cities, dict) else country_cities[0]["children"]
    for country in root:
        for city in country.get("children", []):
            if city.get("name") == city_name:
                return city.get("groupNm")
    return "해당 지역을 찾을 수 없습니다."

