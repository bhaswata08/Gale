"""
This module contains the logic for the outline generator agent.
It creates runnables for generating an outline for a Wikipedia page based on a given content.
It also contains feedback logic for the agent to improve its performance.
"""
from typing import List, Optional

from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

SYSTEM_PROMPT = '''
"You are a Wikipedia writer. Write an outline for a Wikipedia page for the given content. Be comprehensive and specific.",
Do not hallucinate or add any information that is not in the content.

Please output your outline in the following format:
{format_instructions}
'''
SYSTEM_PROMPT_WITH_FEEDBACK = '''
You have tried this task before, incorporate the given feedback to improve your Outline.
'''

class Subsection(BaseModel):
    """A subsection of a Wikipedia page."""
    SubSectionTitle : str = Field(description="Title of the subsection")
    description : str = Field(description="Content of the subsection")

    @property
    def as_string(self)->str:
        """Return the subsection as a string."""
        return f"#{self.SubSectionTitle} \n{self.description}\n".strip()

class Section(BaseModel):
    """A section of a Wikipedia page."""
    SectionTitle : str = Field(description="Title of the section")
    description : str = Field(description="A description of the section")
    subsections: Optional[List[Subsection]] = Field(
        default = None,
        title = "Titles and descriptions for each subsection of the wikipedia page",
        )

    @property
    def as_str(self) -> str:
        """Return the section as a string."""
        subsections = "\n\n".join(
            f"### {subsection.SubSectionTitle}\n\n{subsection.description}"
            for subsection in self.subsections or []
        )
        return f"## {self.SectionTitle}\n\n{self.description}\n\n{subsections}".strip()


class Outline(BaseModel):
    """An outline for a Wikipedia page."""
    PageTitle: str = Field(..., title="Title of the Wikipedia page")
    sections: List[Section] = Field(
        default_factory=list,
        title="Titles and descriptions for each section of the Wikipedia page.",
    )

    @property
    def as_str(self) -> str:
        """Return the outline as a string."""
        sections = "\n\n".join(section.as_str for section in self.sections)
        return f"# {self.PageTitle}\n\n{sections}".strip()


parser = PydanticOutputParser(pydantic_object=Outline)

prompt = ChatPromptTemplate.from_messages(
    [
      SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
    ]
).partial(format_instructions=parser.get_format_instructions())


prompt_with_feedback = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
        (
            "user",
            """Here is the output from your last trial: \n\n
            {agent_outline}
            """
        ),
        SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT_WITH_FEEDBACK),
        (
            "user",
            """Here is the contents of the document: \n\n
            {relevant_content}
            """
        )
    ]
).partial(format_instructions=parser.get_format_instructions())
# Choose the LLM that will drive the agent
llm = ChatOpenAI(
    model="gpt-4-turbo-2024-04-09",
    temperature=0.0,
)

outline_gen_runnable = prompt | llm | parser
outline_gen_runnable_with_feedback = prompt_with_feedback | llm | parser
