from typing import List

from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

SYSTEM_PROMPT = '''
Based on the information given, your task is to critique the given review and the corresponding sections.\
You are to provide a detailed analysis of the review and the sections, and provide feedback on the review.\
You are to be thorough and detailed in your critique, and provide feedback on the review and the sections.\

Be detail centric and outline what information the previous agent might have missed.\
Give information on how it can improve its writing style and the content of the review.\

if the review is perfect, set isperfect field to true, else set it to false.\

Here is the context you from which you may refer the ground truth from:\
{context}

Here is the content you need to critique:\
{content}

Here is the format instructions for your output:\
{format_instructions}

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
llm = ChatOpenAI(
    model="gpt-4-turbo-2024-04-09",
    temperature=0.0,
)

critique_runnable = prompt | llm | parser
