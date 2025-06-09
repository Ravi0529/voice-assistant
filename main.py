# Take user input (Speech)

import speech_recognition as sr
from speech.stt import refined_stt
import json


def main():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 3

        while True:
            print("Listening...")
            audio = r.listen(source)

            print("Processing Audio...")
            try:
                stt = r.recognize_google(audio)
                print("User: ", stt)

                refined_json = refined_stt(stt)
                refined = json.loads(refined_json)

                refined_input = refined["refined_input"]
                print("Refined text: ", refined_input)

                if refined_input.strip().upper() == "EXIT":
                    print("Exiting as requested. Goodbye!")
                    break
            except sr.UnknownValueError:
                print("Apologies, the audio wasn't clear enough. Try Again!")
            except sr.RequestError as e:
                print("There was an issue retrieving results. Error: {0}".format(e))


if __name__ == "__main__":
    main()
