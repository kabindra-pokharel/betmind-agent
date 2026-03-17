from app.state import BettingState
from app.tools.odds_tools import fetch_odds, find_best_odds

async def odds_agent(state: BettingState) -> dict:
    sport = state['sport']
    home_team = state['home_team']
    away_team = state['away_team']    
    if not sport or not home_team or not away_team:
        return {
            "odds_data": {},
            "best_odds": {}
        }
    
    data = await fetch_odds(sport)
    best = find_best_odds(data, home_team, away_team)
    return {
        'odds_data': data,
        'best_odds': best
    }

