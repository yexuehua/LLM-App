from langchain_core.language_models.llms import LLM
import dashscope
from typing import Any
import os

class QwenLLM2(LLM):
    dashscope2: Any
    def __init__(self, dashscope):
        super().__init__()
        self.dashscope2 = dashscope

    def _call(self, prompt: str, stop=None):
        response = self.call_qwen_api(prompt)
        if response.status_code == 200:
            assistant_response = response.output.text
            #self.session_id = response.output.session_id
            return assistant_response
        else:
            return f"Error: {response.message}"

    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "tongyi"

    def call_qwen_api(self, prompt):
        response = self.dashscope2.Generation.call(
            api_key=os.getenv('DASHSCOPE_API_KEY'),
            model="qwen-plus",
            prompt=prompt,
            # parameters={"maxlength": 200, "temperature": 0.7},
            enable_search=True,
            # options={'session_id': session_id}
        )
        return response