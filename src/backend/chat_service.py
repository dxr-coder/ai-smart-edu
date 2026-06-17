from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_deepseek import ChatDeepSeek
from neo4j import GraphDatabase
from src.configuration.dependency import *
from src.agent.prompts import SYSTEM_PROMPT
from src.agent import tools_def

client = ChatDeepSeek(
    model='deepseek-v4-flash',
    api_key=get_deepseek_config().API_KEY,
    base_url=get_deepseek_config().BASE_URL,
).bind_tools([tools_def.QUERY_NEO4J_TOOL])


def chat(message: str) -> str:
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=message),
    ]
    response = client.invoke(messages)
    while response.tool_calls:
        for tool_call in response.tool_calls:
            cypher = tool_call['args']['cypher']
            driver = GraphDatabase.driver(Neo4jConfig.URI, auth=(Neo4jConfig.USER, Neo4jConfig.PASSWORD))
            result = driver.execute_query(cypher)
            rows = [dict(r) for r in result.records]
            driver.close()
            messages.append(response)
            messages.append(ToolMessage(content=str(rows), tool_call_id=tool_call['id']))
        response = client.invoke(messages)
    return response.content
