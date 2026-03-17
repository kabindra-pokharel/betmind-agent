from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage
from app.state import BettingState
from app.tools.search_tools import search_betting_trends
import asyncio

llm = ChatAnthropic(model="claude-sonnet-4-5-20250929")

async def trends_agent(state: BettingState) -> dict:
    sport = state.get('sport')
    home_team = state.get('home_team')
    away_team = state.get('away_team')
    bet_type = state.get('bet_type')

    if not sport or not home_team or not away_team:
        return {"trends_summary": None}

    trends_data = await search_betting_trends(home_team, away_team)

    if not trends_data:
        return {"trends_summary": "No trends data found"}

    trends_text = ""
    for item in trends_data:
        trends_text += f"\nTitle: {item['title']}\nContent: {item['content']}\n"

    for attempt in range(3):
        try:
            response = llm.invoke([
                SystemMessage(content="""You are a sports betting trends analyst.
                Extract the most relevant betting trends and patterns from the articles.
                Focus on:
                - Historical head to head betting trends
                - Over/under patterns
                - Home/away betting performance
                - Line movement and sharp money signals
                - Public betting percentages if available
                - Any relevant ATS (against the spread) records
                
                Return a clean bullet point list.
                Maximum 6 bullet points.
                Be concise — one line per point.
                Return ONLY the bullet points, no intro or conclusion."""),
                HumanMessage(content=f"""
                Match: {home_team} vs {away_team}
                Sport: {sport}
                Bet type: {bet_type}

                Trends articles:
                {trends_text}
                """)
            ])

            raw = response.content.strip()
            trends = [
                line.strip().lstrip("•-*").strip()
                for line in raw.split("\n")
                if line.strip()
            ]

            return {
                "trends_summary": trends,
                "messages": [response]
            }

        except Exception as e:
            if "overloaded" in str(e).lower() and attempt < 2:
                print(f"Claude overloaded, retrying in 10 seconds... (attempt {attempt + 1}/3)")
                await asyncio.sleep(10)
            else:
                print(f"Trends agent error: {e}")
                return {"trends_summary": ["Trends analysis temporarily unavailable"]}