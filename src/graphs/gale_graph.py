"""
This is a simple example of a graph that uses the langgraph library 
to create a state machine for the GALE agent. 

The agent is a simple agent that takes in a piece of text and then runs it 
through a series of agents to generate an outline. 

The outline is then critiqued and the process is repeated until 
the outline is perfect or the number of iterations exceeds a 
certain limit. The agent is then done and the final outline is returned.
"""
import yaml
import logging
from typing import TypedDict, Any
from json import JSONDecodeError

from dotenv import load_dotenv
from langchain_core.exceptions import OutputParserException
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
    outline_gen_runnable_with_feedback,
    parser as outline_parser
)


load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(filename="storm_v2.log", level=logging.INFO)

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

class AgentState(TypedDict):
    initial_content : str
    content : Any
    feedback : Critique
    iter_count : int


# Nodes
def should_retry(state : AgentState)->str:
    is_perfect = state["feedback"].isperfect
    if (
        is_perfect == True
        or state['iter_count'] > config['graphs']['iter_count']
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
        except (OutputParserException, JSONDecodeError) as e:
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
                "relevant_content": state['feedback'].relevantcontent,
                "agent_outline": state['content'],
                "feedback" : repr(state['feedback'].critique)
            }
            outputs = outline_gen_runnable_with_feedback.with_config(
                {
                    'run_name': 'outline_gen_with_feedback'
                }
            ).invoke(inputs)
        except (OutputParserException, JSONDecodeError) as e:
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

        except Exception as e:
            print(type(Exception))
            print(type(e))

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
    except (OutputParserException, JSONDecodeError) as e:
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
    except Exception as e:
        print(type(Exception))
        print(type(e))

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
