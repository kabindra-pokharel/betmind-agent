from typing import TypedDict, Annotated, Optional
import operator

class BettingState(TypedDict):
    messages: Annotated[list, operator.add]
    query: str
    sport: Optional[str]
    home_team: Optional[str]
    away_team: Optional[str]
    bet_type: Optional[str]
    player_mentioned: Optional[list[str]]
    player_context: Optional[str]
    odds_data: Optional[dict]
    best_odds: Optional[dict]
    stats_summary: Optional[str]
    news_factors: Optional[list]
    trends_summary: Optional[list]
    prediction: Optional[str]
    confidence: Optional[str]
    key_factors: Optional[str]
    