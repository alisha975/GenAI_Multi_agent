from langchain_core.messages import HumanMessage

#Chat Messages
def get_chat_messages(user_query,state_graph,config):
    user_query=user_query
    chat_messages=[HumanMessage(content=user_query)]
    chat_messages=state_graph.invoke({"user_query":chat_messages},config)
    return chat_messages