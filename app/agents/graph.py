from langgraph.graph import StateGraph, START, END
from app.agents.supervisor import supervisor_node
from app.agents.odds_agent import odds_agent
from app.agents.stats_agent import stats_agent
from app.agents.news_agent import news_agent
from app.agents.trends_agent import trends_agent
from app.agents.prediction import prediction_node
from app.state import BettingState

graph = StateGraph(BettingState)
graph.add_node('supervisor_node', supervisor_node)
graph.add_node('odds_agent', odds_agent)
graph.add_node('stats_agent', stats_agent)
graph.add_node('news_agent', news_agent)
graph.add_node('trends_agent', trends_agent)
graph.add_node('prediction_node', prediction_node)

graph.add_edge(START, 'supervisor_node')
graph.add_edge('supervisor_node', 'odds_agent')
graph.add_edge('supervisor_node', 'stats_agent')
graph.add_edge('supervisor_node', 'news_agent')
graph.add_edge('supervisor_node', 'trends_agent')
graph.add_edge('odds_agent', 'prediction_node')
graph.add_edge('stats_agent', 'prediction_node')
graph.add_edge('news_agent', 'prediction_node')
graph.add_edge('trends_agent', 'prediction_node')
graph.add_edge('prediction_node', END)

graph_builder = graph.compile()
