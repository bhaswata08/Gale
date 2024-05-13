import os
import operator
import random
import logging
from typing import TypedDict, Any

from dotenv import load_dotenv
from pydantic.v1 import ValidationError
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage
)
from langchain_core.documents import Document
from langchain.pydantic_v1 import BaseModel, Field
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, END

from src.agents.criticizer.critic import (
    Critique,
    critique_runnable,
    parser as critique_parser
    )
from src.agents.format_checker.formatter import formatter_runnable
from src.agents.initial_summarizer.initial_summarizer import(
    initial_summarizer_runnable
)
from src.agents.outline_generator.outline_gen import (
    outline_gen_runnable,
    outline_gen_runnable_with_feedback, #TODO: Implement this
    parser as outline_parser
)


load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(filename="storm_v2", level=logging.INFO)
memory = SqliteSaver.from_conn_string(":memory:")

class AgentState(TypedDict):
    initial_content : str
    content : Any
    feedback : Critique
    iter_count : int # TODO: Need to implement this


# Nodes
def should_retry(state : AgentState)->str:
    is_perfect = state["feedback"].isperfect
    if (
        is_perfect == True
        or state['iter_count'] > 4
    ):
        return "continue"
    else:
        return "retry"

def call_initial_summarizer(state : AgentState):
    inputs = {
        "content": state["initial_content"]
    }
    outputs = initial_summarizer_runnable.with_config(
        {
            'run_name': 'initial_summarizer'
        }
    ).invoke(inputs)
    return {
        'content': outputs
    }

def call_outline_generator(state : AgentState):
    if state["feedback"] is None:
        try:
            inputs = {
                "content": state["content"]
            }
            outputs = outline_gen_runnable.with_config(
                {
                    'run_name': 'outline_gen_without_feedback'
                }
            ).invoke(inputs)
        except ValidationError as e:
            formatter_inputs = {
                "format_instructions": outline_parser.get_format_instructions(),
                "agent_output": e,
            }
            temp_runnable = formatter_runnable | outline_parser
            outputs = temp_runnable.with_config(
                {
                    "run_name": "outline_gen_without_feedback passed through formatter",
                }
            ).invoke(formatter_inputs)
    else:
        try:
            inputs = {
                "relevant_content": state["initial_content"],
                "agent_outline": state['content'],
                "feedback" : repr(state['feedback'])
            }
            outputs = outline_gen_runnable_with_feedback.with_config(
                {
                    'run_name': 'outline_gen_with_feedback'
                }
            ).invoke(inputs)
        except ValidationError as e:
            formatter_inputs = {
                "format_instructions": outline_parser.get_format_instructions(),
                "agent_output": e,
            }
            temp_runnable = formatter_runnable | outline_parser
            outputs = temp_runnable.with_config(
                {
                    "run_name": "outline_gen_with_feedback passed through formatter",
                }
            ).invoke(formatter_inputs)

    return {
        'content': outputs
    }

def call_criticizer(state : AgentState):
    try:
        inputs = {
            "context": state["initial_content"],
            'content': state["content"]
        }
        outputs = critique_runnable.with_config(
            {
                'run_name': 'criticizer'
            }
        ).invoke(inputs)
    except ValidationError as e:
        formatter_inputs = {
            "format_instructions": critique_parser.get_format_instructions(),
            "agent_output": e,
        }
        temp_runnable = formatter_runnable | critique_parser
        outputs = temp_runnable.with_config(
            {
                "run_name": "criticizer passed through formatter",
            }
        ).invoke(formatter_inputs)

    return {
        'feedback': outputs,
        "iter_count" : state["iter_count"] + 1
    }

# Initialize a new graph
graph = StateGraph(AgentState)

# Define the nodes
graph.add_node("initial_summarizer", call_initial_summarizer)
graph.add_node("outline_gen", call_outline_generator)
graph.add_node("criticizer", call_criticizer)

# Set the starting edge
graph.set_entry_point("initial_summarizer")

# Define the graph logic
graph.add_edge("initial_summarizer", "outline_gen")
graph.add_edge("outline_gen", "criticizer")
graph.add_conditional_edges(
    "criticizer",
    should_retry,
    {
        "retry": "outline_gen",
        "continue": END
    }
)

# Compile the graph
gale_graph = graph.compile()
