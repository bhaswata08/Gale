"""Entry point for the initial summarizer agent."""
import os
import configparser

from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate
)

from langchain.schema.output_parser import StrOutputParser

config = configparser.ConfigParser()
config.read('config.ini')

SYSTEM_PROMPT = '''
You are an expert reseacher that generates high quality summaries from Academic Papers or open-source projects. 
Based on the contents of the given document, you are required to summarize the key points and provide a high level overview of the content.

When you are invoked you do the following:
1. Read the document line by line and understand its contents and what the author is trying to convey.
2. Output the most important information in the document.
3. Highlight the most significant contributions and findings in the document.
4. Highlight the technical approach, inovations, and/or details.

You do not miss out on any part of the document and are very thorough in your investigation.

Take a deep breath, take your time, think out your steps, and provide a highest quality summary of the document.
'''

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
        (
            "user",
            """Here is the contents of the document: \n\n
            {content}
            """
        )
    ]
)

# Choose the LLM that will drive the agent
if config['INITIAL_SUMMARIZER']['initial_summarizer_together']:
    from src.utils.togetherchain import TogetherLLM
    llm = TogetherLLM(
        model=config['INITIAL_SUMMARIZER']['initial_summarizer_together_llm'],
        together_api_key=str(os.environ.get("TOGETHER_API_KEY")),
        temperature=0.0,
        max_tokens=int(config['INITIAL_SUMMARIZER']['initial_summarizer_tokens']),
    )
else:
    llm = ChatOpenAI(
        model=config['INITIAL_SUMMARIZER']['initial_summarizer_llm'],
        temperature=0.0
        )
initial_summarizer_runnable = prompt | llm | StrOutputParser()
