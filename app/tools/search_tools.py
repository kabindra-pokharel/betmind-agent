from tavily import TavilyClient
import os

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

async def search_news(query: str, max_results: int = 5) -> list:
    """Search for news articles using Tavily."""
    try:
        response = client.search(
            query=query,
            max_results=max_results,
            search_depth="basic"
        )
        results = response.get("results", [])
        return [
            {
                "title": r.get("title", ""),
                "content": r.get("content", ""),
                "url": r.get("url", ""),
                "published_date": r.get("published_date", "")
            }
            for r in results
        ]
    except Exception as e:
        print(f"Tavily search error: {e}")
        return []

async def search_team_news(home_team: str, away_team: str, sport: str) -> dict:
    """Search for injuries, lineups and news for both teams."""

    injury_results = await search_news(
        f"{home_team} vs {away_team} injury lineup news 2026"
    )

    home_results = await search_news(
        f"{home_team} latest news form 2026"
    )

    away_results = await search_news(
        f"{away_team} latest news form 2026"
    )

    return {
        "injury_news": injury_results,
        "home_team_news": home_results,
        "away_team_news": away_results
    }

async def search_betting_trends(home_team: str, away_team: str) -> list:
    """Search for betting trends and predictions."""
    return await search_news(
        f"{home_team} vs {away_team} betting prediction odds analysis 2026",
        max_results=5
    )