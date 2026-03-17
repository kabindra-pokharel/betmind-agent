from dotenv import load_dotenv
load_dotenv()

import asyncio
from tkinter import Image
from app.agents.graph import graph_builder
from app.agents.supervisor import supervisor_node, llm
from app.state import BettingState
from app.tools.odds_tools import find_best_odds, fetch_odds
from app.tools.stats_tools import fetch_team_stats
from app.tools.search_tools import search_team_news

# async def test():
#     state = BettingState(
#         query="Give me a prediction of match today between Manchester City vs Real Madrid in soccer_ucl. Which is favorite?",
#         messages=[]
#     )
    
#     result = await graph_builder.ainvoke(state)
#     print("Best odds:", result['best_odds'])
#     print("Stats summary:", result['stats_summary'])
#     print(graph_builder.get_graph().draw_ascii())

# asyncio.run(test())
# print(graph_builder.get_graph().draw_ascii())

# async def test_stats():
#     stats = await fetch_team_stats("soccer_ucl", "Manchester City", "Real Madrid")
#     print("Home stats:", stats["home_team_stats"])
#     print("Away stats:", stats["away_team_stats"])
#     print("H2H:", stats["head_to_head"])

# asyncio.run(test_stats())

# async def test_odds():
#     data = await fetch_odds("soccer_ucl")
#     print("Games found:", len(data))
    
#     # Print all available games
#     for game in data:
#         print(f"  {game.get('home_team')} vs {game.get('away_team')}")
    
#     if data:
#         best = find_best_odds(data, "Manchester City", "Real Madrid")
#         print("Best odds:", best)

# asyncio.run(test_odds())

# async def test_search():
#     results = await search_team_news(
#         "Manchester City", 
#         "Real Madrid", 
#         "soccer_ucl"
#     )
#     print("Injury news:")
#     for item in results["injury_news"]:
#         print(f"\nTitle: {item['title']}")
#         print(f"Content: {item['content']}")
#         print(f"URL: {item['url']}")

# asyncio.run(test_search())

# async def test():
#     state = BettingState(
#         query="Give me a prediction of match today between Real Madrid and Manchester City. Which is favorite?",
#         messages=[]
#     )

#     result = await graph_builder.ainvoke(state)
#     print("Best odds:", result['best_odds'])
#     print("\nStats summary:", result['stats_summary'])
#     print("\nNews factors:")
#     for factor in result['news_factors']:
#         print(f"  - {factor}")
#     print("\n", graph_builder.get_graph().draw_ascii())

# asyncio.run(test())

# async def test():
#     state = BettingState(
#         query="Give me a prediction of match today between Real Madrid and Manchester City. Which is favorite?",
#         messages=[]
#     )

#     result = await graph_builder.ainvoke(state)
#     print("Best odds:", result['best_odds'])
#     print("\nStats summary:", result['stats_summary'])
#     print("\nNews factors:")
#     for factor in result['news_factors']:
#         print(f"  - {factor}")
#     print("\nTrends:")
#     for trend in result['trends_summary']:
#         print(f"  - {trend}")
#     print("\n", graph_builder.get_graph().draw_ascii())

# asyncio.run(test())

async def test():
    state = BettingState(
        query="Give me a prediction of match today between Real Madrid and Manchester City. Which is favorite?",
        messages=[]
    )

    result = await graph_builder.ainvoke(state)

    print("=" * 60)
    print("BETMIND PREDICTION")
    print("=" * 60)
    print(result['prediction'])
    print("=" * 60)
    print("Confidence:", result['confidence'])
    print("Key factors:", result['key_factors'])
    print("\n", graph_builder.get_graph().draw_ascii())

asyncio.run(test())