# # # # Get a new token: https://help.aliyun.com/document_detail/611472.html?spm=a2c4g.2399481.0.0
# # # # from getpass import getpass
# # # #
# # # # DASHSCOPE_API_KEY = getpass()
# # #
# # import os
# #
# # #os.environ["DASHSCOPE_API_KEY"] = "..."
#
# # #
# # # from langchain_community.llms import Tongyi
# # # print(Tongyi().invoke("今天北京天气怎样"))
# #
# # import os
# # from openai import OpenAI
# #
# # client = OpenAI(
# #     # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
# #     api_key=os.getenv("DASHSCOPE_API_KEY"),
# #     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope服务的base_url
# # )
# # completion = client.chat.completions.create(
# #     model="qwen-turbo",
# #     messages=[
# #         {'role': 'system', 'content': 'You are a helpful assistant.'},
# #         {'role': 'user', 'content': 'how many gold that China win in paris Olympic game'}],
# #     extra_body={
# #         "enable_search": True
# #     }
# #     )
# # print(completion.model_dump_json())
#
import os
import dashscope
#
dashscope.api_key = "..."
os.environ["DASHSCOPE_API_KEY"] = "..."
# tools = [
#     {
#         "type": "function",
#         "function": {
#             "name": "get_current_time",
#             "description": "当你想知道现在的时间时非常有用。",
#             "parameters": {}
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "get_current_weather",
#             "description": "当你想查询指定城市的天气时非常有用。",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "location": {
#                         "type": "string",
#                         "description": "城市或县区，比如北京市、杭州市、余杭区等。"
#                     }
#                 }
#             },
#             "required": [
#                 "location"
#             ]
#         }
#     }
# ]
# messages = [{"role": "user", "content": "杭州天气怎么样"}]
# response = dashscope.Generation.call(
#     # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
#     api_key=os.getenv("DASHSCOPE_API_KEY"),
#     model='qwen-turbo',
#     messages=messages,
#     tools=tools,
#     result_format='message'
# )
# print(response)

import os
import dashscope

messages = [
    {'role': 'system', 'content': 'You are a helpful assistant.'},
    {'role': 'user', 'content': 'what day is it today'}
    ]
response = dashscope.Generation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen-plus",
    #messages=messages,
    prompt='what the weather like today',
    enable_search=True,
    #result_format='message'
    )
print(response)