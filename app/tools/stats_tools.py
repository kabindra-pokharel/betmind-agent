import httpx

ESPN_ENDPOINTS = {
    "nfl":        ("football", "nfl"),
    "nba":        ("basketball", "nba"),
    "mlb":        ("baseball", "mlb"),
    "nhl":        ("hockey", "nhl"),
    "soccer_ucl": ("soccer", "uefa.champions"),
    "soccer_epl": ("soccer", "eng.1"),
    "soccer_mls": ("soccer", "usa.1"),
    "soccer":     ("soccer", "uefa.champions"),
    "ncaafb":     ("football", "college-football"),
    "ncaabb":     ("basketball", "mens-college-basketball"),
    "mma":        ("mma", "ufc"),
}

def parse_form(form_string: str) -> dict:
    if not form_string:
        return {
            "last_5": "N/A",
            "wins": 0,
            "losses": 0,
            "draws": 0,
            "win_rate": 0.0,
            "form_rating": "unknown"
        }

    results = list(form_string.upper())
    total = len(results)
    wins = results.count('W')
    losses = results.count('L')
    draws = results.count('D')

    if wins >= 4:
        rating = "excellent"
    elif wins >= 3:
        rating = "good"
    elif wins >= 2:
        rating = "average"
    else:
        rating = "poor"

    return {
        "last_5": form_string,
        "wins": wins,
        "losses": losses,
        "draws": draws,
        "win_rate": round(wins / total * 100, 1) if total > 0 else 0.0,
        "form_rating": rating
    }

async def fetch_scoreboard(sport: str) -> dict:
    endpoint = ESPN_ENDPOINTS.get(sport.lower())
    if not endpoint:
        return {}

    sport_type, league = endpoint
    url = f"https://site.api.espn.com/apis/site/v2/sports/{sport_type}/{league}/scoreboard"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=10)

    if response.status_code != 200:
        print(f"ESPN scoreboard error: {response.status_code}")
        return {}

    return response.json()

async def fetch_team_stats(sport: str, home_team: str, away_team: str) -> dict:
    endpoint = ESPN_ENDPOINTS.get(sport.lower())
    if not endpoint:
        return {"error": f"Sport {sport} not supported"}

    scoreboard = await fetch_scoreboard(sport)
    events = scoreboard.get("events", [])

    home_stats = {}
    away_stats = {}
    h2h = {"found": False}

    for event in events:
        competitions = event.get("competitions", [])
        for competition in competitions:
            competitors = competition.get("competitors", [])
            team_names = [
                c.get("team", {}).get("displayName", "").lower()
                for c in competitors
            ]

            home_match = any(home_team.lower() in name for name in team_names)
            away_match = any(away_team.lower() in name for name in team_names)

            if home_match and away_match:
                for competitor in competitors:
                    team_name = competitor.get("team", {}).get("displayName", "")
                    form_string = competitor.get("form", "")
                    form_data = parse_form(form_string)

                    team_stats = {
                        "name": team_name,
                        "form": form_data,
                        "home_away": competitor.get("homeAway", ""),
                        "logo": competitor.get("team", {}).get("logo", ""),
                        "rank": competitor.get("curatedRank", {}).get("current", "N/A"),
                    }

                    if home_team.lower() in team_name.lower():
                        home_stats = team_stats
                    elif away_team.lower() in team_name.lower():
                        away_stats = team_stats

                status = event.get("status", {}).get("type", {})
                h2h = {
                    "found": True,
                    "date": event.get("date", ""),
                    "status": status.get("description", ""),
                    "completed": status.get("completed", False),
                    "venue": competition.get("venue", {}).get("fullName", "Unknown"),
                    "name": event.get("name", "")
                }

    return {
        "home_team_stats": home_stats,
        "away_team_stats": away_stats,
        "head_to_head": h2h,
        "sport": sport,
        "home_team": home_team,
        "away_team": away_team
    }