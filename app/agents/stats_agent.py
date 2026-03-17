from app.state import BettingState
from app.tools.stats_tools import fetch_team_stats

async def stats_agent(state: BettingState) -> dict:
    sport = state['sport']
    home_team = state['home_team']
    away_team = state['away_team']

    if not sport or not home_team or not away_team:
        return {"stats_summary": None}

    data = await fetch_team_stats(sport, home_team, away_team)

    home = data.get("home_team_stats", {})
    away = data.get("away_team_stats", {})
    h2h = data.get("head_to_head", {})

    home_form = home.get("form", {})
    away_form = away.get("form", {})

    summary = f"""
    HOME TEAM: {home.get('name')}
    - Form (last 5): {home_form.get('last_5')} 
    - Record: {home_form.get('wins')}W {home_form.get('draws')}D {home_form.get('losses')}L
    - Win Rate: {home_form.get('win_rate')}%
    - Form Rating: {home_form.get('form_rating')}
    - Playing: {home.get('home_away')}

    AWAY TEAM: {away.get('name')}
    - Form (last 5): {away_form.get('last_5')}
    - Record: {away_form.get('wins')}W {away_form.get('draws')}D {away_form.get('losses')}L
    - Win Rate: {away_form.get('win_rate')}%
    - Form Rating: {away_form.get('form_rating')}
    - Playing: {away.get('home_away')}

    HEAD TO HEAD:
    - Venue: {h2h.get('venue')}
    - Status: {h2h.get('status')}
    - Date: {h2h.get('date')}
    """

    return {
        "stats_summary": summary.strip()
    }