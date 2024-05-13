from typing import List
import os
import yaml

from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

SYSTEM_PROMPT = '''
As a helpful and efficient AI agent, your task is to analyze the given input context, or "ground truth," \
in combination with the criticism or feedback provided by the previous agent. Your primary goal is to act \
as a retriever, specifically focused on extracting the most crucial and relevant information from the ground truth.
Extract the most amount of possible detail from the ground truth. Any and all information that might be relavant \
to the criticism should be extracted.\

To accomplish this, you should carefully consider the criticism offered by the previous agent and use it to\
guide your extraction process. Your output should be a well-curated selection of the most pertinent content\
from the original ground truth, tailored to address the concerns or issues highlighted in the criticism.

Remember to demonstrate your ability to accurately identify and retrieve the most valuable information, \
even when faced with complex or nuanced criticism. Your precision and effectiveness in this task will be \
the key measures of your success.

Remember, the structures for context and critique are delimited by xml tags
Given context (ground truth): 
<CONTEXT>
{context}
</CONTEXT>
Criticism from previous agent: 
<CRITIQUE>
{critique}
</CRITIQUE>
Please output only and only according to the format instructions given below:

{format_instructions}


Your task: Extract the most relevant content from the given context according to the criticism.
'''

class BlackBoxRetriever(BaseModel):
    relevantcontent: str = Field(..., title="The relevant content")
    cotreasing: str = Field(..., title="The reasoning behind the the extraction and why the data is relevant")

class Information(BaseModel):
    info : List[BlackBoxRetriever] = Field(..., title="List of extarcted contents")

parser = PydanticOutputParser(pydantic_object=Information)

prompt = ChatPromptTemplate.from_messages(
    [
      SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
    ]
).partial(format_instructions=parser.get_format_instructions())

# Choose the LLM that will drive the agent
if config['retriever_config']['together']:
    from src.utils.togetherchain import TogetherLLM
    llm = TogetherLLM(
        model=config['retriever_config']['together_llm'],
        together_api_key=str(os.environ.get("TOGETHER_API_KEY")),
        temperature=0.5,
        max_tokens=int(config['retriever_config']['tokens']),
    )
else:
    llm = ChatOpenAI(
        model = config['retriever_config']['llm'],
        temperature=0.5,
    )

extractor_runnable = prompt | llm | parser
