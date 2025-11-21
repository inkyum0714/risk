import re

def map_to_city(query):
    query = query.lower().strip()  
    pattern = r"\b(los\s*angel|los\s*a|la|엘\s*에이)\b"
    
    match = re.search(pattern, query)
    if match:
        return "로스엔젤레스"
    return query

while True:
    t = input()
    print(t, "→", map_to_city(t))
