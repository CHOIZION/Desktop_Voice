import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import os
import random
import pyautogui
import pyjokes
import openai
from googletrans import Translator

# 명령어 트리거 정의
COMMANDS = {
    "time": ["시간", "몇 시", "현재 시간", "지금 몇 시야"],
    "date": ["날짜", "오늘 날짜", "오늘은 몇 월 며칠", "오늘은 무슨 날"],
    "wikipedia": ["위키피디아", "위키", "위키 검색", "백과사전 검색"],
    "play_music": ["음악 재생", "노래 틀어", "음악 틀어", "노래 재생"],
    "open_youtube": ["유튜브 열어", "유튜브 켜", "유튜브 열기", "유튜브로 이동"],
    "open_google": ["구글 열어", "구글 켜", "구글 열기", "구글로 이동"],
    "set_name": ["이름 바꿔", "너 이름 바꿔", "내 이름 설정", "너의 이름을 변경해"],
    "screenshot": ["스크린샷", "화면 캡처", "화면 찍어", "스크린 캡쳐"],
    "joke": ["농담 해", "날 웃게 해봐", "재밌는 농담 해줘", "농담 해줘", "웃겨"],
    "shutdown": ["시스템 종료", "종료", "컴퓨터 끄기", "시스템을 꺼"],
    "restart": ["재시작", "시스템 재부팅", "컴퓨터 다시 시작"],
    "offline": ["오프라인", "나가", "종료해", "서비스 중지"]
}

# 초기 설정
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

# OpenAI API 키 설정
openai.api_key = 'YOUR_OPENAI_API_KEY'

translator = Translator()

def speak(audio) -> None:
    engine.say(audio)
    engine.runAndWait()

def time_func() -> None:
    """현재 시간을 알려줍니다."""
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    speak("The current time is")
    speak(current_time)
    print("The current time is", current_time)

def date_func() -> None:
    """현재 날짜를 알려줍니다."""
    now = datetime.datetime.now()
    speak("The current date is")
    speak(f"{now.day} {now.strftime('%B')} {now.year}")
    print(f"The current date is {now.day}/{now.month}/{now.year}")

def wishme() -> None:
    """시간대에 따라 사용자에게 인사합니다."""
    speak("Welcome back, sir!")
    print("Welcome back, sir!")

    hour = datetime.datetime.now().hour
    if 4 <= hour < 12:
        speak("Good morning!")
        print("Good morning!")
    elif 12 <= hour < 16:
        speak("Good afternoon!")
        print("Good afternoon!")
    elif 16 <= hour < 24:
        speak("Good evening!")
        print("Good evening!")
    else:
        speak("Good night, see you tomorrow.")

    assistant_name = load_name()
    speak(f"{assistant_name} at your service. Please tell me how may I assist you.")
    print(f"{assistant_name} at your service. Please tell me how may I assist you.")

def screenshot() -> None:
    """스크린샷을 찍고 저장합니다."""
    img = pyautogui.screenshot()
    img_path = os.path.expanduser("~\\Pictures\\screenshot.png")
    img.save(img_path)
    speak(f"Screenshot saved as {img_path}.")
    print(f"Screenshot saved as {img_path}.")

def takecommand() -> str:
    """사용자의 마이크 입력을 받아 텍스트로 반환합니다."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1

        try:
            audio = r.listen(source, timeout=5)  # 타임아웃 설정
        except sr.WaitTimeoutError:
            speak("Timeout occurred. Please try again.")
            return None

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="ko-KR")  # 한국어 인식
        print(f"User said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
        return None
    except Exception as e:
        speak(f"An error occurred: {e}")
        print(f"Error: {e}")
        return None

def play_music(song_name=None) -> None:
    """사용자의 음악 디렉토리에서 음악을 재생합니다."""
    song_dir = os.path.expanduser("~\\Music")
    songs = os.listdir(song_dir)

    if song_name:
        songs = [song for song in songs if song_name.lower() in song.lower()]

    if songs:
        song = random.choice(songs)
        os.startfile(os.path.join(song_dir, song))
        speak(f"Playing {song}.")
        print(f"Playing {song}.")
    else:
        speak("No song found.")
        print("No song found.")

def set_name() -> None:
    """어시스턴트의 새 이름을 설정합니다."""
    speak("What would you like to name me?")
    name = takecommand()
    if name:
        with open("assistant_name.txt", "w") as file:
            file.write(name)
        speak(f"Alright, I will be called {name} from now on.")
    else:
        speak("Sorry, I couldn't catch that.")

def load_name() -> str:
    """파일에서 어시스턴트의 이름을 불러오거나 기본 이름을 사용합니다."""
    try:
        with open("assistant_name.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "Jarvis"  # 기본 이름

def search_wikipedia(query):
    """위키피디아를 검색하고 요약을 반환합니다."""
    try:
        speak("Searching Wikipedia...")
        wikipedia.set_lang("ko")  # 한국어 위키피디아 설정
        result = wikipedia.summary(query, sentences=2)
        speak(result)
        print(result)
    except wikipedia.exceptions.DisambiguationError:
        speak("Multiple results found. Please be more specific.")
    except Exception:
        speak("I couldn't find anything on Wikipedia.")

def get_gpt_response(prompt: str) -> str:
    """GPT-3 API를 호출하여 응답을 반환합니다."""
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # 사용하고자 하는 모델 선택
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        answer = response.choices[0].text.strip()
        return answer
    except Exception as e:
        speak("Sorry, I couldn't process that request.")
        print(f"GPT API Error: {e}")
        return ""

def translate_to_english(text: str) -> str:
    """텍스트를 영어로 번역합니다."""
    try:
        translation = translator.translate(text, src='ko', dest='en')
        return translation.text
    except Exception as e:
        speak("Translation error.")
        print(f"Translation Error: {e}")
        return ""

def match_command(query: str) -> str:
    """쿼리를 분석하여 해당 명령어를 반환합니다."""
    for command, triggers in COMMANDS.items():
        for trigger in triggers:
            if trigger in query:
                return command
    return "unknown"

if __name__ == "__main__":
    wishme()

    while True:
        query = takecommand()
        if not query:
            continue

        command = match_command(query)

        if command == "time":
            time_func()

        elif command == "date":
            date_func()

        elif command == "wikipedia":
            # "위키피디아" 또는 "위키" 다음에 오는 검색어 추출
            search_term = query
            for trigger in COMMANDS["wikipedia"]:
                search_term = search_term.replace(trigger, "").strip()
            search_wikipedia(search_term)

        elif command == "play_music":
            # "음악 재생" 또는 "노래 틀어" 다음에 오는 노래 이름 추출
            song_name = query
            for trigger in COMMANDS["play_music"]:
                song_name = song_name.replace(trigger, "").strip()
            play_music(song_name)

        elif command == "open_youtube":
            wb.open("https://www.youtube.com")
            speak("Opening YouTube.")
            print("Opening YouTube.")

        elif command == "open_google":
            wb.open("https://www.google.com")
            speak("Opening Google.")
            print("Opening Google.")

        elif command == "set_name":
            set_name()

        elif command == "screenshot":
            screenshot()
            speak("I've taken a screenshot, please check it.")

        elif command == "joke":
            joke = pyjokes.get_joke()
            speak(joke)
            print(joke)

        elif command == "shutdown":
            speak("Shutting down the system, goodbye!")
            os.system("shutdown /s /f /t 1")
            break

        elif command == "restart":
            speak("Restarting the system, please wait!")
            os.system("shutdown /r /f /t 1")
            break

        elif command == "offline":
            speak("Going offline. Have a good day!")
            break

        else:
            # 일반적인 질문을 처리 (GPT 연동)
            english_query = translate_to_english(query)
            if not english_query:
                continue

            speak("Processing your request with GPT.")
            print(f"GPT Query: {english_query}")
            gpt_response = get_gpt_response(english_query)
            if gpt_response:
                speak(gpt_response)
                print(f"GPT Response: {gpt_response}")
