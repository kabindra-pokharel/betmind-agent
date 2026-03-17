from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage
from app.state import BettingState
from app.tools.search_tools import search_team_news
import asyncio

llm = ChatAnthropic(model="claude-sonnet-4-5-20250929")

async def news_agent(state: BettingState) -> dict:
    sport = state.get('sport')
    home_team = state.get('home_team')
    away_team = state.get('away_team')

    if not sport or not home_team or not away_team:
        return {"news_factors": []}

    news_data = await search_team_news(home_team, away_team, sport)

    all_news = ""
    for item in news_data.get("injury_news", []):
        all_news += f"\nTitle: {item['title']}\nContent: {item['content']}\n"
    for item in news_data.get("home_team_news", []):
        all_news += f"\nTitle: {item['title']}\nContent: {item['content']}\n"
    for item in news_data.get("away_team_news", []):
        all_news += f"\nTitle: {item['title']}\nContent: {item['content']}\n"

    if not all_news:
        return {"news_factors": ["No recent news found"]}

    for attempt in range(3):
        try:
            response = llm.invoke([
                SystemMessage(content="""You are a sports news analyst. 
                Extract only the most relevant facts for betting prediction from the news provided.
                Focus on:
                - Key injuries or suspensions
                - Lineup changes
                - Player returns from injury
                - Team morale or recent issues
                - Any other factors that could affect the match outcome
                
                Return a clean bullet point list of facts only.
                Maximum 8 bullet points.
                Be concise — one line per point.
                Return ONLY the bullet points, no intro or conclusion."""),
                HumanMessage(content=f"""
                Match: {home_team} vs {away_team}
                Sport: {sport}
                
                News articles:
                {all_news}
                """)
            ])

            raw = response.content.strip()
            factors = [
                line.strip().lstrip("•-*").strip()
                for line in raw.split("\n")
                if line.strip()
            ]

            return {
                "news_factors": factors,
                "messages": [response]
            }

        except Exception as e:
            if "overloaded" in str(e).lower() and attempt < 2:
                print(f"Claude overloaded, retrying in 10 seconds... (attempt {attempt + 1}/3)")
                await asyncio.sleep(10)
            else:
                print(f"News agent error: {e}")
                return {"news_factors": ["News analysis temporarily unavailable"]}