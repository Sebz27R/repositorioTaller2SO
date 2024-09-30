import requests

def get_all_partidos():
    url = "http://localhost:8000/partidos"
    skip = 0
    limit = 100
    all_partidos = []

    while True:
        params = {"skip": skip, "limit": limit}
        response = requests.get(url, params=params)
        data = response.json()

        partidos = data["Partidos"]
        all_partidos.extend(partidos)

        print(f"Fetched {len(partidos)} partidos, skipping {skip} records")

        if len(partidos) < limit:
            break

        skip += limit 

    return all_partidos


def create_partido(home_team, away_team, home_goals, away_goals, result, season):
    url = "http://localhost:8000/partido/"
    payload = [{
        "home_team": home_team,
        "away_team": away_team,
        "home_goals": home_goals,
        "away_goals": away_goals,
        "result": result,
        "season": season
    }]

    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        print(f"Partido creado exitosamente: {response.json()}")
    else:
        print(f"Error al crear partido: {response.status_code}, {response.text}")


def filtrar_partidos(temporada_exacta=None, temporada_desde=None, temporada_hasta=None):
    url = "http://localhost:8000/partidos/filtrar/"
    params = {}

    if temporada_exacta:
        params["temporada_exacta"] = temporada_exacta
    if temporada_desde:
        params["temporada_desde"] = temporada_desde
    if temporada_hasta:
        params["temporada_hasta"] = temporada_hasta

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        print(f"Partidos encontrados: {len(data['Partidos'])}")
        for partido in data["Partidos"]:
            print(partido)
    else:
        print(f"Error al filtrar partidos: {response.status_code}, {response.text}")



# Ejecuta la función para obtener todos los partidos
# partidos = get_all_partidos()
# print(f"Numero total de partidos obtenidos: {len(partidos)}")

# Ejecuta la función para crear un nuevo partido (método POST)
create_partido(
    home_team="West Ham United",
    away_team="Brentford",
    home_goals=0,
    away_goals=2,
    result="A",
    season="2022-2023"
)

#Intentando crear un partido con resultado negativo
create_partido(
    home_team="Team A",
    away_team="Team B",
    home_goals=-2,
    away_goals=1,
    result="A",
    season="2021-2022"
)

#Intentando crear un partido con dos equipos de igual nombre
create_partido(
    home_team="Team A",
    away_team="Team A",
    home_goals=0,
    away_goals=1,
    result="A",
    season="2021-2022"
)

#Intentando crear un partido con formato de temporada incorrecta
create_partido(
    home_team="Team A",
    away_team="Team B",
    home_goals=0,
    away_goals=1,
    result="A",
    season="2021"
)

#Filtrando por temporada exacta 2016-2017
filtrar_partidos(temporada_exacta="2016-2017")

#Filtrando partidos desde la temporada 2015-2016 hasta 2016-2017
filtrar_partidos(temporada_desde="2015-2016", temporada_hasta="2016-2017")

#Intentando filtrar usando todos los parametros
filtrar_partidos(temporada_exacta="2014-2015", temporada_desde="2019-2020", temporada_hasta="2022-2023")



