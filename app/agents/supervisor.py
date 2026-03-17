import json
from app.state import BettingState
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage
import re

llm = ChatAnthropic(model="claude-sonnet-4-5-20250929")

def supervisor_node(state: BettingState) -> dict:
    users_request = state['query']
    
    response = llm.invoke([
        SystemMessage(content="""Extract betting details from the query and return ONLY a JSON object:
        {
            "sport": "nfl/nba/mlb/nhl/soccer_epl/soccer_ucl/soccer_mls/mma or best match",
            "home_team": "team name or null",
            "away_team": "team name or null",
            "bet_type": "moneyline/spread/total or null",
            "players_mentioned": ["player names"] or [],
            "player_context": "brief context or null"
        }
        For soccer, be specific about the league: soccer_epl, soccer_ucl, soccer_mls etc.
        Return ONLY JSON. No explanation, no markdown, no backticks."""),
        HumanMessage(content=users_request)
    ])
    
    content = response.content.strip()
    content = re.sub(r'^```json\s*', '', content)
    content = re.sub(r'^```\s*', '', content)
    content = re.sub(r'```$', '', content)
    content = content.strip()

    # print("Claude raw response:", content)

    parsed = json.loads(content)
    
    return {
        "sport": parsed.get("sport"),
        "home_team": parsed.get("home_team"),
        "away_team": parsed.get("away_team"),
        "bet_type": parsed.get("bet_type"),
        "players_mentioned": parsed.get("players_mentioned", []),
        "player_context": parsed.get("player_context"),
        "messages": [response]
    }