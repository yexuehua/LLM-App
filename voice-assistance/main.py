import dashscope
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import pyaudio
import wave
import os
from langchain_community.llms import Tongyi
from pydub import AudioSegment
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_core.language_models.llms import LLM
from language_model import *

import vosk
import pyaudio
import json
import pygame
import time
from tts import *

def offline_listen_and_recognize(language="CN"):
    # 加载模型
    # English model
    if language == "EN":
        model_path = "vosk-model-small-en-us-0.15"
    # Chinese model
    elif language == "CN":
        model_path = "vosk-model-small-cn-0.22"
    else:
        print("Language not supported")
        return

    model = vosk.Model(model_path)

    # 初始化 PyAudio
    p = pyaudio.PyAudio()

    # 打开麦克风流
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=8000)

    # 创建识别器
    rec = vosk.KaldiRecognizer(model, 16000)

    print("开始实时监听...")

    # 实时监听并识别
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            if result['text']:
                if language == "CN":
                    if result['text'][:2] == "你好":
                        print("识别结果:", result['text'][2:])
                        feedback = llm_chain.run(result['text'])
                        print(f"回答: {feedback}")
                        tts_win(feedback)
                elif language == "EN":
                    if result['text'][:2] == "hello":
                        print("识别结果:", result['text'][5:])
                        feedback = llm_chain.run(result['text'])
                        print(f"回答: {feedback}")
                        tts_win(feedback)
            else:
                print("无法理解您说的话")


# # Online tts
# def listen_and_recognize():
#     # 创建一个Recognizer实例
#     recognizer = sr.Recognizer()

#     # 使用默认麦克风作为音频源
#     with sr.Microphone() as source:
#         print("请开始说话...")

#         # 调整环境噪音
#         recognizer.adjust_for_ambient_noise(source)

#         # 监听音频输入
#         audio = recognizer.listen(source)

#         try:
#             # 尝试将音频转换为文本
#             text = recognizer.recognize_google(audio, language='zh-CN')
#             #feedback = Tongyi().invoke(text)
#             feedback = llm_chain.run(text)
#             print(f"您说的是: {text}")
#             print(f"回答: {feedback}")
#             tts_win(feedback)

#         except sr.UnknownValueError:
#             print("Google Speech Recognition无法理解您说的话")
#         except sr.RequestError as e:
#             print(f"请求错误; {e}")


if __name__ == "__main__":
	# replace "..." with your api key
    os.environ["DASHSCOPE_API_KEY"] = "..."
    dashscope.api_key = "..."

    prompt_template = PromptTemplate(
        input_variables=["history", "content"],
        template="History: {history}\n user:{content}\n system:"
    )

    # create the session memory buffer
    memory = ConversationBufferMemory(memory_key="history")

    llm_chain = LLMChain(prompt=prompt_template, llm=QwenLLM2(dashscope), memory=memory)
    while True:
        offline_listen_and_recognize(language="CN")