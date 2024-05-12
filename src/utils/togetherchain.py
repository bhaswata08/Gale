"""
This module contains the TogetherLLM class, which represents a language model that integrates 
ChatTogetherAI with LangChain.
"""
import os
from typing import Any, List, Optional

from dotenv import load_dotenv
from langchain_core.callbacks import AsyncCallbackManagerForLLMRun
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from pydantic import Field

from together import Together, AsyncTogether

load_dotenv()



class TogetherLLM(LLM):
    """
    Integrates ChatTogetherAI Properly with LangChain.

    This class represents a language model that integrates ChatTogetherAI with LangChain.
    It extends the LLM (Language Learning Model) class from langchain_core.

    Attributes:
        model (str): The model to use for the Together LLM.
        together_api_key (str): The API key for the Together API.
        temperature (float): The temperature to use for the Together LLM.
        max_tokens (int): The maximum number of tokens to generate for the Together LLM.
    """

    model: str = Field(...,
                       description="The model to use for the Together LLM.")
    together_api_key: str = Field(os.environ.get('TOGETHER_API_KEY'),
                                  description="The API key for the Together API.")
    temperature: float = Field(...,
                               description="The temperature to use for the Together LLM.")
    max_tokens: int = Field(...,
                            description="The maximum number of tokens to \
                                generate for the Together LLM.")

    @property
    def _llm_type(self) -> str:
        return "together"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """
        Generate a completion for the given prompt using the Together API.

        Args:
            prompt (str): The prompt to generate a completion for.
            stop (Optional[List[str]]): A list of stop words to stop the completion at.
            run_manager (Optional[CallbackManagerForLLMRun]): The callback manager for LLM run.

        Returns:
            str: The generated completion.

        Raises:
            Exception: If there is an error while generating the completion.
        """

        try:
            client = Together(api_key=self.together_api_key)
            response = client.chat.completions.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content
        except Exception as e:
            raise e
    async def _acall(
            self, 
            prompt: str,
            stop: Optional[List[str]] = None, 
            run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
            **kwargs: Any) -> str:
        async_client = AsyncTogether(api_key=self.together_api_key)
        response = await async_client.chat.completions.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content

# Usage:
# llm = TogetherLLM(
#     model="togethercomputer/llama-2-7b-chat",
#     max_tokens=256,
#     temperature=0.8,
#     together_api_key=os.environ.get("TOGETHER_API_KEY"),
# )
