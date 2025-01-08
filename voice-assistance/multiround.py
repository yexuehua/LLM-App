from http import HTTPStatus

import dashscope
from dashscope import Generation
from langchain_community.llms import Tongyi
from langchain_core.language_models import LLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
import os

#os.environ["DASHSCOPE_API_KEY"] = "..."
os.environ["DASHSCOPE_API_KEY"] = "..."
dashscope.api_key = "..."

def multi_round():
    messages = [{'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': '如何做西红柿炖牛腩？'}]
    response = Generation.call(model="qwen-turbo",
                               messages=messages,
                               # 将输出设置为"message"格式
                               result_format='message')
    if response.status_code == HTTPStatus.OK:
        print(response)
        # 将assistant的回复添加到messages列表中
        messages.append({'role': response.output.choices[0]['message']['role'],
                         'content': response.output.choices[0]['message']['content']})
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
        # 如果响应失败，将最后一条user message从messages列表里删除，确保user/assistant消息交替出现
        messages = messages[:-1]
    # 将新一轮的user问题添加到messages列表中
    messages.append({'role': 'user', 'content': '不放糖可以吗？'})
    # 进行第二轮模型的响应
    response = Generation.call(model="qwen-turbo",
                               messages=messages,
                               result_format='message',  # 将输出设置为"message"格式
                               )
    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))


def call_qwen_api(prompt, session_id=None):
    response = dashscope.Generation.call(
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        model="qwen-plus",
        prompt=prompt,
        #parameters={"maxlength": 200, "temperature": 0.7},
        enable_search=True,
        #options={'session_id': session_id}
    )
    return response


prompt_template = PromptTemplate(
    input_variables=["history", "content"],
    template = "History: {history}\n user:{content}\n system:"
)

# create the session memory buffer
memory = ConversationBufferMemory(memory_key="history")

class QwenLLM2(LLM):
    #def __init__(self):
        #self.session_id = None

    def _call(self, prompt: str, stop=None):
        response = call_qwen_api(prompt)
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



llm_chain = LLMChain(prompt=prompt_template, llm=QwenLLM2(), memory=memory)


# 多轮对话函数
def multi_round_conversation():
    print("Start a conversation with the AI. Type 'exit' to end the conversation.")

    while True:
        user_input = input("User: ")

        if user_input.lower() == "exit":
            break

        # 生成回复
        response = llm_chain.run(user_input)

        # 打印回复
        print(f"Assistant: {response}")

if __name__ == '__main__':
    multi_round_conversation()