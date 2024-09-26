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


# Ejecuta la función para obtener todos los partidos
partidos = get_all_partidos()
print(f"Numero total de partidos obtenidos: {len(partidos)}")

# Ejecuta la función para crear un nuevo partido (método POST)
create_partido(
    home_team="West ham",
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
