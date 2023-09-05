import speech_recognition as sr
import webcolors
from govee import control_govee_lights

def listen():
    recognizer = sr.Recognizer()


    with sr.Microphone() as source:
        print("Listening")
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                print(command)
                if "off" in command:
                    print("Turning off")
                    control_govee_lights({"name": "turn","value":"off"})
                else:
                    try:
                        colour = webcolors.name_to_rgb(command)
                        print(colour)
                    except ValueError:
                        continue

                    print(f"Changing to {command} colour")
                    control_govee_lights({"name":"color","value":{"r": colour.red, "g": colour.green, "b": colour.blue}})
                
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print("error:", str(e))

if __name__ == "__main__":
    listen()