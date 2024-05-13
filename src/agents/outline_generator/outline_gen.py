"""
This module contains the logic for the outline generator agent.
It creates runnables for generating an outline for a Wikipedia page based on a given content.
It also contains feedback logic for the agent to improve its performance.
"""
import os
from typing import List, Optional
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
You are WikiExpert, an AI assistant highly skilled at writing comprehensive, well-structured, and informative Wikipedia articles on any topic. 
Your task is to generate a complete Wikipedia article based on the provided outline schema.

The outline will include:

    * The title of the Wikipedia page
    * A list of sections, each with:
        * A title and description of the section
        * The main content of the section with details and information
        * Optional statistics or numerical data about the section, which can be in the form of markdown tables or descriptions
        * An optional list of subsections, each with their own title, description and content

Your generated Wikipedia article should meet the following criteria:

    * Accurate and factual information from the given sources/context
    * Neutral, unbiased tone that presents information objectively
    * Clear, concise and well-organized writing that is easy to understand
    * Proper use of headers to clearly delineate sections and subsections
    * Smooth transitions between sections and subsections
    * Inclusion of relevant statistics, data, examples, and citations where appropriate

Please output your outline in the following format:
{format_instructions}
'''

SYSTEM_PROMPT_WITH_FEEDBACK = '''
You have tried this task before, incorporate the given feedback to improve your Article.
'''

class Subsection(BaseModel):
    """A subsection of a Wikipedia page."""
    SubSectionTitle : str = Field(description="Title of the subsection")
    description : str = Field(description="Detailed description of the subsection")
    content: str = Field(description="Content of the subsection, details and information about the subsection.")
    stats: Optional[str] = Field(description="Statistics and numbers about the subsection if any.\
                                 Can be in the form of markdown tables or just descriptions.")

    @property
    def as_string(self)->str:
        """Return the subsection as a string."""
        return f"#{self.SubSectionTitle} \n{self.description}\n {self.content}".strip()

class Section(BaseModel):
    """A section of a Wikipedia page."""
    SectionTitle : str = Field(description="Title of the section")
    description : str = Field(description="A Detialed description of the section")
    content: str = Field(description="Content of the section, details and information about the section.")
    stats: Optional[str] = Field(description="Statistics and numbers about the Section if any.\
                                 Can be in the form of markdown tables or just descriptions.")
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
        return f"## {self.SectionTitle}\n\n{self.description}\n\n{self.content}\n\n{subsections}".strip()


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
      (
            "user",
            """Here is the content you need to create an outline for: \n\n
            -----------------------------------------
            {content}
            -----------------------------------------
            """
      )
    ]
).partial(format_instructions=parser.get_format_instructions())


prompt_with_feedback = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
        (
            "user",
            """Here is the output from your last trial: \n\n
            -----------------------------------------
            {agent_outline}
            -----------------------------------------
            """
        ),
        SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT_WITH_FEEDBACK),
        (
            "user",
            """Here is the contents of the document: \n\n
            -----------------------------------------
            {relevant_content}
            -----------------------------------------
            """
        ),
        (
            "user",
            """Here is the feedback you need to incorporate: \n\n
            -----------------------------------------
            {feedback}
            -----------------------------------------
            """
        )
    ]
).partial(format_instructions=parser.get_format_instructions())
# Choose the LLM that will drive the agent
if config['outline_generator_config']['together']:
    from src.utils.togetherchain import TogetherLLM
    llm = TogetherLLM(
        model=config['outline_generator_config']['together_llm'],
        together_api_key=str(os.environ.get("TOGETHER_API_KEY")),
        temperature=0.0,
        max_tokens=int(config['outline_generator_config']['tokens']),
    )
else:
    llm = ChatOpenAI(
        model = config['outline_generator_config']['llm'],
        temperature=0.0,
    )

outline_gen_runnable = prompt | llm | parser
outline_gen_runnable_with_feedback = prompt_with_feedback | llm | parser
