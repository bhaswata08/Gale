import yaml
import os

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
Based on the information given, your task is to critique the given review and the corresponding sections.\
You are to provide a detailed analysis of the review and the sections, and provide feedback on the review.\
You are to be thorough and detailed in your critique, and provide feedback on the review and the sections.\

Be detail centric, descriptive and outline what information the previous agent might have missed.\
Check if model has missed any information, statistics and numbers.\
Give information on how it can improve its writing style and the content of the review.\

if the review is perfect, set isperfect field to true, else set it to false.\

Here is the context you from which you may refer the ground truth from:\
-----------------------------------------\
{context}
-----------------------------------------\
Do not output criticism or feedback outside the context of the review.\
if a technical detail is missing outside the context of the review, do not provide it.\

Here is the content you need to critique:\
-----------------------------------------\
{content}
-----------------------------------------\
Here is the format instructions for your output:\
-----------------------------------------\
{format_instructions}
-----------------------------------------\

do not output outside your format instructions.
'''

class Critique(BaseModel):
    isperfect: bool = Field(..., title="Whether the review is perfect or not")
    critique: str = Field(..., title="The critique of the review")
    cotreasoning: str = Field(..., title="The reasoning behind the critique")

parser = PydanticOutputParser(pydantic_object=Critique)

prompt = ChatPromptTemplate.from_messages(
    [
      SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
    ]
).partial(format_instructions=parser.get_format_instructions())

# Choose the LLM that will drive the agent
if config['critic_config']['together']:
    from src.utils.togetherchain import TogetherLLM
    llm = TogetherLLM(
        model=config['critic_config']['together_llm'],
        together_api_key=str(os.environ.get("TOGETHER_API_KEY")),
        temperature=0.0,
        max_tokens=int(config['critic_config']['tokens']),
    )
else:
    llm = ChatOpenAI(
        model = config['critic_config']['llm'],
        temperature=0.0,
    )

critique_runnable = prompt | llm | parser
