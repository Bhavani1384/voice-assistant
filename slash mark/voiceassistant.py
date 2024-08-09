import speech_recognition as sr
import pyttsx3
import requests
import datetime


engine = pyttsx3.init()


engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print("Sorry, there was an error with the request.")
            return None

def get_weather(city):
    api_key = 'YOUR_OWM_API_KEY'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    if data['cod'] == 200:
        main = data['main']
        weather_description = data['weather'][0]['description']
        temperature = main['temp']
        return f"The weather in {city} is {weather_description} with a temperature of {temperature}°C."
    else:
        return "Sorry, I couldn't retrieve the weather information."

def get_time():
    now = datetime.datetime.now()
    return f"The current time is {now.strftime('%H:%M')}."

def get_date():
    now = datetime.datetime.now()
    return f"Today's date is {now.strftime('%Y-%m-%d')}."

def perform_task(command):
    if 'weather' in command:
        city = command.split('weather in')[-1].strip()
        weather_info = get_weather(city)
        speak(weather_info)
    elif 'time' in command:
        time_info = get_time()
        speak(time_info)
    elif 'date' in command:
        date_info = get_date()
        speak(date_info)
    elif 'exit' in command:
        speak("Goodbye!")
        return False
    else:
        speak("Sorry, I don't understand that command.")
    return True

def main():
    speak("Hello, how can I assist you today?")
    while True:
        command = recognize_speech()
        if command:
            if not perform_task(command.lower()):
                break

if __name__ == "__main__":
    main()
