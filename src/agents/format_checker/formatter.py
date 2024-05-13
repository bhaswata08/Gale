"""Format Checker"""
import configparser
import os

from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
)
config = configparser.ConfigParser()
config.read('config.ini')

system_prompt_initial = '''
The previous task from the LLM failed. It can either lack the necessary information or the information is not in the correct format. Please provide the information in the correct format. 
You may eliminate the information that is not necessary.
Strictly adhere to the formats provided in the instructions.


When you are invoked you quietly do the following:
1. Analyse the information provided by the LLM.
2. Analyse and understand the format instructions.
3. Provide the information in the correct format.

Make sure of that output field only contains the following:
1. No fields missing
2. No preamble or explaination
3. No extra information

If the output is already correct, just pass it through while removing the extra information.

This is a bad example from you:
<example>
YOUR RESPONSE:
Here is the original schema:
```json
 # Some schema here
```
and the response
```json
# Some response here
```
</example>
This example violates two rules:
1. It contains extra information
2. It contains the original schema

The better example would be:
<example>
YOUR RESPONSE:
```json
# Some response
```
</example>
This example is correct because it only contains the response and nothing else.

The format for the information is as follows:
{format_instructions}

Here is the output from the LLM:
{agent_output}

Adjust your output accordingly.

Take a deep breath and start working on the task.

'''

prompt = ChatPromptTemplate.from_messages(
    [
      SystemMessagePromptTemplate.from_template(system_prompt_initial),
    ]
)

# Choose the LLM that will drive the agent
if config['FORMAT_CHECKER']['format_checker_together']:
    from src.utils.togetherchain import TogetherLLM
    llm = TogetherLLM(
        model=config['FORMAT_CHECKER']['format_checker_together_llm'],
        together_api_key=str(os.environ.get("TOGETHER_API_KEY")),
        temperature=0.0,
        max_tokens=int(config['FORMAT_CHECKER']['format_checker_tokens']),
    )
else:
    llm = ChatOpenAI(
        model = config['FORMAT_CHECKER']['format_checker_llm'],
        temperature=0.0,
    )

formatter_runnable = prompt | llm
