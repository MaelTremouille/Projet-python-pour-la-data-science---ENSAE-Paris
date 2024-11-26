import requests

def get_airfare_prices(api_key, origin, destination, departure_date, return_date=None):
    api_key = 'cjszgbd7n97ednjmpxhvjnqa'
    url = 'https://api.airfranceklm.com/opendata/offers/v3/reference-data/deals' 

    # En-têtes requis par l'API
    headers = {
        'AFKL-TRAVEL-Host': 'KL',
        'API-Key': api_key,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/hal+json'
    }

    # Paramètres de la requête
    params = {
        'origin': origin,           # Code IATA de l'aéroport de départ
        'destination': destination,  # Code IATA de l'aéroport de destination
        'departureDate': departure_date,  # Date de départ
        'returnDate': return_date    # Date de retour, si applicable
    }

    # Envoi de la requête
    response = requests.get(url, headers=headers, params=params)
    
    # Vérification du statut de la réponse
    if response.status_code == 200:
        return response.json()  # Réponse JSON contenant les prix
    else:
        print(f"Erreur {response.status_code}: {response.text}")
        return None

# Utilisation de la fonction avec des exemples de paramètres
api_key = 'YOUR_API_KEY'
origin = 'CDG'
destination = 'JFK'
departure_date = '2024-12-10'
return_date = '2024-12-20'

prices = get_airfare_prices(api_key, origin, destination, departure_date, return_date)
print(prices['destinationsByZone'][0]['cabins'][0]['priceRangeByTripType'][0]['range'])
# dict_keys(['market', 'currency', 'origins', 'destinationsByZone', 
# 'tripTypes', 'cabins', 'defaultValues'])