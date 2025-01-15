import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import os
import random
import pyautogui
import pyjokes

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)


def speak(audio) -> None:
    engine.say(audio)
    engine.runAndWait()


def time() -> None:
    """현재 시간을 알려줍니다."""
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    speak("The current time is")
    speak(current_time)
    print("The current time is", current_time)


def date() -> None:
    """현재 날짜를 알려줍니다."""
    now = datetime.datetime.now()
    speak("The current date is")
    speak(f"{now.day} {now.strftime('%B')} {now.year}")
    print(f"The current date is {now.day}/{now.month}/{now.year}")


def wishme() -> None:
    """시간대에 따라 사용자를 인사합니다."""
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
    img_path = os.path.join(os.path.expanduser("~"), "Pictures", "screenshot.png")
    img.save(img_path)
    speak(f"Screenshot saved as {img_path}.")
    print(f"Screenshot saved as {img_path}.")


def takecommand() -> str:
    """사용자로부터 한국어 음성 입력을 받아 텍스트로 반환합니다."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1

        try:
            audio = r.listen(source, timeout=5)
        except sr.WaitTimeoutError:
            speak("Timeout occurred. Please try again.")
            return None

    try:
        print("Recognizing...")

        query = r.recognize_google(audio, language="ko-KR")
        print(f"Recognized Korean Query: {query}")
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
    song_dir = os.path.join(os.path.expanduser("~"), "Music")
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
    """어시스턴트의 새로운 이름을 설정합니다."""
    speak("What would you like to name me?")
    name = takecommand()
    if name:
        with open("assistant_name.txt", "w") as file:
            file.write(name)
        speak(f"Alright, I will be called {name} from now on.")
    else:
        speak("Sorry, I couldn't catch that.")


def load_name() -> str:
    """어시스턴트의 이름을 파일에서 불러오거나 기본 이름을 사용합니다."""
    try:
        with open("assistant_name.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "Jarvis"


def search_wikipedia(query):
    """위키피디아를 검색하고 요약을 반환합니다."""
    try:
        speak("Searching Wikipedia...")
        result = wikipedia.summary(query, sentences=2)
        speak(result)
        print(result)
    except wikipedia.exceptions.DisambiguationError:
        speak("Multiple results found. Please be more specific.")
    except Exception:
        speak("I couldn't find anything on Wikipedia.")


if __name__ == "__main__":
    wishme()

    while True:
        query = takecommand()
        if not query:
            continue

        if "시간 알려줘" in query:
            time()

        elif "날짜 알려줘" in query:
            date()

        elif "위키피디아 검색" in query:
            speak("What would you like to search on Wikipedia?")
            search_query = takecommand()
            if search_query:
                search_wikipedia(search_query)

        elif "음악 틀어" in query:
            speak("Which song would you like to play?")
            song_name = takecommand()
            play_music(song_name)

        elif "유튜브 열어" in query:
            wb.open("https://youtube.com")
            speak("I have opened YouTube.")

        elif "구글 열어" in query:
            wb.open("https://google.com")
            speak("I have opened Google.")

        elif "이름 바꿔" in query:
            set_name()

        elif "스크린샷 찍어" in query:
            screenshot()
            speak("I've taken a screenshot, please check it.")

        elif "농담 해줘" in query:
            joke = pyjokes.get_joke()
            speak(joke)
            print(joke)

        elif "시스템 종료" in query:
            speak("Shutting down the system, goodbye!")
            os.system("shutdown /s /f /t 1")
            break

        elif "시스템 재시작" in query:
            speak("Restarting the system, please wait!")
            os.system("shutdown /r /f /t 1")
            break

        elif "종료해" in query or "오프라인" in query:
            speak("Going offline. Have a good day!")
            break
