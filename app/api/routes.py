from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from app.agents.graph import graph_builder
from app.state import BettingState

router = APIRouter()

class PredictRequest(BaseModel):
    query: str
    sport: Optional[str] = None

@router.post("/predict")
async def predict(req: PredictRequest):
    try:
        state = BettingState(
            query=req.query,
            messages=[]
        )

        result = await graph_builder.ainvoke(state)

        return {
            "success": True,
            "match": f"{result.get('home_team')} vs {result.get('away_team')}",
            "sport": result.get('sport'),
            "prediction": result.get('prediction'),
            "confidence": result.get('confidence'),
            "key_factors": result.get('key_factors', []),
            "best_odds": result.get('best_odds', {}),
            "stats_summary": result.get('stats_summary'),
            "news_factors": result.get('news_factors', []),
            "trends_summary": result.get('trends_summary', [])
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/odds/{sport}")
async def get_odds(sport: str):
    from app.tools.odds_tools import fetch_odds
    data = await fetch_odds(sport)
    return {"sport": sport, "games": len(data), "data": data}

@router.get("/sports")
async def list_sports():
    from app.tools.odds_tools import SPORT_KEYS
    return {"sports": list(SPORT_KEYS.keys())}