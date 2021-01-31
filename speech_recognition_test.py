import speech_recognition as SR
from gtts import gTTS
from mutagen.mp3 import MP3 as mp3
import pygame
import time
from io import BytesIO
import datetime

def recognizing():
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        speech = r.recognize_google(audio, language="en-EN")
        return speech
    except SR.UnknownValueError:
        return None
    except SR.RequestError as e:
        print("could not request results from google speech recognition service: {0}".format(e))
        return None
        
def speech(text):
    if text is not None:
        tts = gTTS(text)
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        pygame.mixer.music.load(fp) #音源を読み込み
        mp3_length = mp3(fp).info.length #音源の長さ取得
        pygame.mixer.music.play() #再生開始。1の部分を変えるとn回再生(その場合は次の行の秒数も×nすること)
        time.sleep(mp3_length) #再生開始後、音源の長さだけ待つ(0.25待つのは誤差解消)
        pygame.mixer.music.stop() #音源の長さ待ったら再生停止


if __name__ == '__main__':
    r = SR.Recognizer()
    mic = SR.Microphone()
    pygame.mixer.init()

    speech("hi i'm vanessa")

    while True:
        text = recognizing()
        #print(text)

        # ここで話した内容を切り分ける
        """
        １．vanessaと最初に発話したかどうか
        ２．コマンドになる言葉を発したかどうか
        ３．固有のセリフを発したか
        """
        if text == None:
            continue

        data = text.split(" ")
        #print(data)
        if data[0] == "Vanessa" and len(data) > 1:
            text = " ".join(data[1:])
            if text == None:
                text = "I can't understand what you say"
            if text == "goodbye":
                speech("see you")
                break
            if text == "bye-bye":
                speech("bye-bye")
                break
            if text == "what day is it today":
                current_time = datetime.datetime.now()
                text = current_time.strftime("%B") + " " + str(current_time.month) 
            if text == "what time is it now":
                current_time = datetime.datetime.now()
                text = str(current_time.hour) + " : " + str(current_time.minute)

            speech(text)

# r = SR.Recognizer()
# mic = SR.Microphone()
# pygame.mixer.init()

# while True:
#     print("say something ...")

#     with mic as source:
#         r.adjust_for_ambient_noise(source)
#         audio = r.listen(source)

#     try:
#         speech = r.recognize_google(audio, language="en-EN")

#         if speech == "goodbye":
#             break
#         if speech == "bye-bye":
#             break
#         if speech == "what day is it today":
#             current_time = datetime.datetime.now()
#             speech = current_time.strftime("%B") + " " + str(current_time.month) 
#         if speech == "what time is it now":
#             current_time = datetime.datetime.now()
#             speech = str(current_time.hour) + " : " + str(current_time.minute)
            
#     except SR.UnknownValueError:
#         print("could not understand audio")
#     except SR.RequestError as e:
#         print("could not request results from google speech recognition service: {0}".format(e))
