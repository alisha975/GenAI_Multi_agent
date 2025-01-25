## data process
from tools import data_generation,generate_graph
from prompts import Supervisor_prompt_chain,Analysis_prompt_chain,Summary_prompt_chain
from langgraph.graph import END,StateGraph
from typing_extensions import TypedDict
from langchain_core.messages import HumanMessage
# from main import student_id

# #data prepararion
# data=data_generation.invoke({"user_id":student_id})
# ###for the graph 
# #graph_result=generate_graph({"student_data":data})

# #GRAPH Settings
# GRAPH_SETTINGS={"configurable":{"thread_id":"5"},"recursion_limit":50,"stream_mode":True}


#start Graph implementaiom
class GraphState(TypedDict):
    """ 
    Represent the state of Graph.

    Attributes:
        user_query: query
        query_category : query category
        num_steps : number of steps

    """
    user_query:str
    analysis_output:str
    summary:str
    call_node :str
    last_call_node: str
    graph :dict

# supervisior node 
def supervisior_node(state):
    last_call_node =""
    print("Supervisior......")
    user_query=state["user_query"]
    members=["Analysis","Summary"]
    call_node = Supervisor_prompt_chain.invoke(
        {
            "user_query":user_query,
            "members":members,
            "last_call_node":last_call_node,
        }
      
    )
    return{
            "call_node":call_node,
        }

#Analysis Node
def analysis_node(state,student_data):
    print("Analysis ......")
    student_data=student_data
    analysis_output=Analysis_prompt_chain.invoke(
        {
            "student_data":student_data
        }
    )
    user_query="Analysis is completed"

    return{"analysis_output":analysis_output,"user_query":user_query}

#Summary Node
def summary_node(state):
    print("Summary........")
    analysis_output=state["analysis_output"]
    summary=Summary_prompt_chain.invoke(
        {
            "analysis_output":analysis_output


        }
    )
    user_query="Summary is completed"
    return{"summary":summary,"user_query":user_query}


#Graph Node
def graph_node(state,student_data):
    print("Graph........")
    student_data=student_data
    graph=generate_graph.invoke({"student_data":student_data})
    user_query="Graph is completed"
    return{"graph":graph,"user_query":user_query}



# Clal_Node
def call_node(state):
    call_node=state["call_node"]
    if "Analysis" in call_node:
        last_call_node="Analysis"
        return "Analysis"
    elif "Summary" in call_node:
        last_call_node="Summary"
        return "Summary"
    elif "Graph" in call_node:
        last_call_node="Graph"
        return "Graph"
    
    else:
        last_call_node="Finish"
        return "Finish"
    



# Defining student Graph
def student_staregraph(student_data,query):
    workflow=StateGraph(GraphState)
    workflow.set_entry_point("Supervisor")
    workflow.add_node("Supervisor",supervisior_node)
    workflow.add_node(
        "Analysis", lambda state:analysis_node(state,student_data)
    )
    workflow.add_node("Summary",summary_node)
    workflow.add_node(
        "Graph", lambda state:graph_node(state,student_data)
    )
    workflow.add_conditional_edges(
        "Supervisor",
        call_node,
        {
            "Analysis":"Analysis",
            "Summary":"Summary",
            "Graph":"Graph",
            "Finish":END,

        },

        )
   
    workflow.add_edge("Analysis","Supervisor")
    workflow.add_edge("Summary","Supervisor")
    workflow.add_edge("Graph","Supervisor")

    app=workflow.compile()

    print(app.get_graph().print_ascii())
    return app

# id=5
# #user query define
# user_query=f"Give me details of student whos id is {id}"

# #create object of state graph
# app=student_staregraph(data,user_query)













