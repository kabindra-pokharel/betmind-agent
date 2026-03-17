import httpx
import os

ODDS_API_KEY = os.getenv("ODDS_API_KEY")
BASE_URL = os.getenv("BASE_URL")

SPORT_KEYS = {
    "soccer": "soccer_uefa_champs_league",
    "nfl": "americanfootball_nfl",
    "nba": "basketball_nba",
    "mlb": "baseball_mlb",
    "nhl": "icehockey_nhl",
    "ncaafb": "americanfootball_ncaaf",
    "ncaabb": "basketball_ncaab",
    "mma": "mma_mixed_martial_arts",
    "soccer_mls": "soccer_usa_mls",
    "soccer_ucl": "soccer_uefa_champs_league",
}

async def fetch_odds(sport: str) -> dict:
    sport_key = SPORT_KEYS.get(sport.lower(), sport)
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/sports/{sport_key}/odds",
            params={
                "apiKey": ODDS_API_KEY,
                "regions": "us,uk,eu",
                "markets": "h2h,spreads,totals",
                "oddsFormat": "american"
            }
        )
    
    if response.status_code != 200:
        print(f"Odds API error: {response.status_code}")
        return {}
    
    return response.json()

def find_best_odds(odds_data: list, home_team: str, away_team: str) -> dict:
    best = {
        "home": None,
        "away": None,
        "home_book": "",
        "away_book": "",
        "home_team": home_team,
        "away_team": away_team
    }

    for game in odds_data:
        api_home = game.get("home_team", "").lower()
        api_away = game.get("away_team", "").lower()
        team1 = home_team.lower()
        team2 = away_team.lower()

        match = (
            (team1 in api_home or team1 in api_away) and
            (team2 in api_home or team2 in api_away)
        )

        if not match:
            continue

        for bookmaker in game.get("bookmakers", []):
            for market in bookmaker.get("markets", []):
                if market["key"] == "h2h":
                    for outcome in market.get("outcomes", []):
                        price = outcome["price"]
                        name = outcome["name"].lower()

                        if team1 in name:
                            if best["home"] is None or price > best["home"]:
                                best["home"] = price
                                best["home_book"] = bookmaker["title"]
                        elif team2 in name:
                            if best["away"] is None or price > best["away"]:
                                best["away"] = price
                                best["away_book"] = bookmaker["title"]

    return best