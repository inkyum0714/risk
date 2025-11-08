from api.data.Symbol import country_cities

def find_country_by_city(city_name):
    # country_cities가 리스트가 아니라면 아래처럼 수정
    root = country_cities.get("children", []) if isinstance(country_cities, dict) else country_cities[0]["children"]
    for country in root:
        for city in cosuntry.get("children", []):
            if city.get("name") == city_name:
                return city.get("groupNm")
    return "해당 지역을 찾을 수 없습니다."

