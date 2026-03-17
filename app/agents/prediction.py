from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage
from app.state import BettingState
import asyncio

llm = ChatAnthropic(model="claude-sonnet-4-5-20250929")

async def prediction_node(state: BettingState) -> dict:
    home_team = state.get('home_team')
    away_team = state.get('away_team')
    sport = state.get('sport')
    bet_type = state.get('bet_type')
    best_odds = state.get('best_odds', {})
    stats_summary = state.get('stats_summary', 'No stats available')
    news_factors = state.get('news_factors', [])
    trends_summary = state.get('trends_summary', [])
    player_context = state.get('player_context', None)

    news_text = "\n".join([f"- {f}" for f in news_factors]) if news_factors else "No news available"
    trends_text = "\n".join([f"- {t}" for t in trends_summary]) if trends_summary else "No trends available"

    odds_text = f"""
    {home_team}: {best_odds.get('home')} at {best_odds.get('home_book')}
    {away_team}: {best_odds.get('away')} at {best_odds.get('away_book')}
    """

    for attempt in range(3):
        try:
            response = llm.invoke([
                SystemMessage(content="""You are an expert sports betting analyst.
                Analyze all the provided data and generate a structured prediction.
                
                Your response MUST follow this exact format:

                PREDICTION: [Home Win / Away Win / Draw / Over / Under / No Bet]
                CONFIDENCE: [Low / Medium / High]
                RECOMMENDED BET: [specific bet recommendation]
                BEST ODDS: [best available odds and where to find them]
                
                KEY FACTORS:
                - [factor 1]
                - [factor 2]
                - [factor 3]
                
                REASONING: [2-3 sentences explaining the prediction]
                
                DISCLAIMER: This is for analysis purposes only. Not financial advice. Please bet responsibly."""),
                HumanMessage(content=f"""
                Match: {home_team} vs {away_team}
                Sport: {sport}
                Bet Type: {bet_type}
                Player Context: {player_context or 'None provided'}

                ODDS:
                {odds_text}

                TEAM STATS:
                {stats_summary}

                NEWS AND INJURIES:
                {news_text}

                BETTING TRENDS:
                {trends_text}

                Based on all this data, provide your prediction.
                """)
            ])

            return {
                "prediction": response.content,
                "confidence": extract_confidence(response.content),
                "key_factors": extract_key_factors(response.content),
                "messages": [response]
            }

        except Exception as e:
            if "overloaded" in str(e).lower() and attempt < 2:
                print(f"Claude overloaded, retrying in 10 seconds... (attempt {attempt + 1}/3)")
                await asyncio.sleep(10)
            else:
                print(f"Prediction error: {e}")
                return {
                    "prediction": "Prediction temporarily unavailable",
                    "confidence": "Low",
                    "key_factors": []
                }

def extract_confidence(prediction_text: str) -> str:
    """Extract confidence level from prediction text."""
    lines = prediction_text.upper().split("\n")
    for line in lines:
        if "CONFIDENCE:" in line:
            if "HIGH" in line:
                return "High"
            elif "MEDIUM" in line:
                return "Medium"
            else:
                return "Low"
    return "Medium"

def extract_key_factors(prediction_text: str) -> list:
    """Extract key factors from prediction text."""
    factors = []
    lines = prediction_text.split("\n")
    in_factors = False

    for line in lines:
        if "KEY FACTORS:" in line.upper():
            in_factors = True
            continue
        if in_factors:
            if line.strip().startswith("-"):
                factors.append(line.strip().lstrip("-").strip())
            elif line.strip() == "":
                continue
            else:
                break

    return factors