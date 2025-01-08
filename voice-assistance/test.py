# import pyaudio
#
# p = pyaudio.PyAudio()
#
# # 列出所有可用的音频设备
# for i in range(p.get_device_count()):
#     info = p.get_device_info_by_index(i)
#     print(f"Device {i}: {info['name']}")
#
# # 确保你选择的设备ID是正确的
# stream = p.open(format=pyaudio.paInt16,
#                 channels=1,
#                 rate=44100,
#                 input=True,
#                 frames_per_buffer=1024,
#                 input_device_index=0)  # 确认设备ID

import pyaudio


def list_supported_sample_rates(device_index):
    p = pyaudio.PyAudio()
    device_info = p.get_device_info_by_index(device_index)
    supported_rates = []

    # 测试常见的采样率
    test_rates = [8000, 16000, 22050, 32000, 44100, 48000, 96000]

    for rate in test_rates:
        try:
            p.is_format_supported(rate, input_device=device_index, input_format=pyaudio.paInt16, input_channels=1)
            supported_rates.append(rate)
        except ValueError:
            continue

    print(f"设备 {device_index}: {device_info['name']} 支持的采样率: {supported_rates}")

    p.terminate()


def list_audio_devices():
    p = pyaudio.PyAudio()
    device_count = p.get_device_count()

    print("可用的音频设备:")
    for i in range(device_count):
        device_info = p.get_device_info_by_index(i)
        print(f"设备 {i}: {device_info['name']}")

    p.terminate()


if __name__ == "__main__":
    # list_audio_devices()
    # device_index = int(input("请输入要查询的设备索引: "))
    # list_supported_sample_rates(device_index)

    import pyttsx3

    engine = pyttsx3.init()
    text = "中文"
    # temp_file = "temp_audio.wav"
    # engine.save_to_file(text, temp_file)
    # 设置中文语音
    voices = engine.getProperty('voices')

    for voice in voices:
        print(f"Voice ID: {voice.id}, Name: {voice.name}")
        print(voice.languages)
    # 尝试设置中文语音
    found_chinese_voice = False
    for voice in voices:
        if voice.name == "Microsoft Huihui Desktop - Chinese (Simplified)":
            print(voice.name)
            engine.setProperty('voice', voice.id)
            found_chinese_voice = True
            break

    engine.say(text)
    engine.runAndWait()
    # import win32com.client
    #
    # # Initialize the SAPI5 speech engine
    # speaker = win32com.client.Dispatch("SAPI.SpVoice")
    #
    # # Text to speak
    # text = "这个是中文"
    #
    # # Speak the text
    # speaker.Speak(text)