from gtts import gTTS
from playsound import playsound
import pyaudio
import wave
from pydub import AudioSegment
import vosk
import pyaudio
import json
import pygame
import time
from tempfile import NamedTemporaryFile
import pyttsx3
import os


engine = pyttsx3.init()
def tts_win(text):
    if text:
        voices = engine.getProperty('voices')
        # 尝试设置中文语音
        for voice in voices:
            if voice.name.find("Chinese")!=-1:
                print(voice.name)
                engine.setProperty('voice', voice.id)
                found_chinese_voice = True
                break
        engine.say(text)
        engine.runAndWait()

def convert_mp3_to_temp_wav(mp3_file):
    # 使用pydub将MP3文件转换为WAV格式
    audio = AudioSegment.from_mp3(mp3_file)

    # 创建一个临时文件
    with NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_file_name = temp_file.name
        audio.export(temp_file_name, format="wav")

    return temp_file_name

def text_to_speech(text):
    if text:
        # 创建gTTS对象
        tts = gTTS(text=text, lang='zh-cn')

        # 保存为MP3文件
        filename = "output.mp3"
        tts.save(filename)
        temp_wav_file = convert_mp3_to_temp_wav(filename)

        # 播放MP3文件
        #playsound(filename)
        #play_audio_file(filename, 16)
        try:
            play_mp3(temp_wav_file)
        finally:
            # 删除MP3文件
            os.remove(temp_wav_file)




# audiosegment and wave
def play_audio_file(file_path, output_device_index):
    chunk = 1024  # 每次读取的字节数
    audio = AudioSegment.from_mp3(file_path)
    # 将音频转换为WAV格式
    wav_file = "temp.wav"
    audio.export(wav_file, format="wav")

    # 打开WAV文件
    wf = wave.open(wav_file, 'rb')

    p = pyaudio.PyAudio()

    # 打开音频流
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=44100,
                    output=True,
                    output_device_index=output_device_index)

    # 读取数据并播放
    data = wf.readframes(chunk)
    while data:
        stream.write(data)
        data = wf.readframes(chunk)

    # 停止和关闭流
    stream.stop_stream()
    stream.close()
    p.terminate()

# def play_mp3(file_path):
#     # 创建一个新的VLC实例
#     instance = vlc.Instance()
#
#     # 创建一个新的媒体播放器
#     player = instance.media_player_new()
#
#     # 加载MP3文件
#     media = instance.media_new(file_path)
#     player.set_media(media)
#
#     # 开始播放
#     player.play()
#
#     # 等待音频播放完毕
#     while player.is_playing():
#         pass

# pygame modul
def play_mp3(file_path):
    # 初始化pygame混音器
    pygame.mixer.init()

    # 加载MP3文件
    pygame.mixer.music.load(file_path)

    # 开始播放
    pygame.mixer.music.play()
    #pygame.mixer.music.stop()

    # 等待音频播放完毕
    while pygame.mixer.music.get_busy():
        time.sleep(1)

    pygame.mixer.music.stop()
    pygame.mixer.quit()
    # os.remove(file_path)
