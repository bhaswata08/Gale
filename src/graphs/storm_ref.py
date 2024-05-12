import os
import operator
import random
import logging
from typing import TypedDict, Any

from dotenv import load_dotenv
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage
)
from langchain_core.documents import Document
from langchain.pydantic_v1 import BaseModel, Field
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
    outline_gen_runnable_with_feedback,
    parser as outline_parser
)

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(filename="storm_v2", level=logging.INFO)


class AgentState(TypedDict):
    initial_content : Document
    content : Any
    feedback : Critique
    iter_count : int


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
        "content": state["initial_content"].content
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
    try:
        inputs = {
            "content": state["content"]
        }
        outputs = outline_gen_runnable.with_config(
            {
                'run_name': 'outline_gen'
            }
        ).invoke(inputs)
    except Exception as e:
        formatter_inputs = {
            "format_instructions": outline_parser.get_format_instructions(),
            "agent_output": e,
        }
        temp_runnable = formatter_runnable | outline_parser
        extracted_memories = temp_runnable.with_config(
            {
                "run_name": "outline_gen passed through formatter",
            }
        ).invoke(formatter_inputs)

    return {
        'content': outputs
    }

def call_criticizer(state : AgentState):
    inputs = {
        "context": state["initial_content"],
        'content': state["content"]
    }
    outputs = critique_runnable.with_config(
        {
            'run_name': 'criticizer'
        }
    ).invoke(inputs)
    return {
        'content': outputs
    }