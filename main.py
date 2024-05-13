from dotenv import load_dotenv
load_dotenv()
from tests.test1 import content
from src.graphs.gale_graph import gale_graph

inputs = {
    "iter_count" : 1,
    "initial_content" : content.page_content
}

#### VERY IMPORTANT:
# EDIT `config.yaml` file and change iter_count to something reasonable like 10. 
# Each iter count has around 2~3 llm calls

for event in gale_graph.with_config(
    {"run_name": "Gale"}
).stream(
    inputs,
    {"recursion_limit" : 100},
):
    print(event)