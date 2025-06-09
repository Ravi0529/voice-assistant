# Take user input (Speech)

import speech_recognition as sr


def main():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        # r.pause_threshold = 3

        while True:
            print("Listening...")
            audio = r.listen(source)

            print("Processing Audio...")
            try:
                stt = r.recongize_google(audio)
                print("User: ", stt)
            except sr.UnknownValueError:
                print("Apologies, the audio wasn't clear enough.")
            except sr.RequestError as e:
                print("There was an issue retrieving results. Error: {0}".format(e))


if __name__ == "__main__":
    main()
