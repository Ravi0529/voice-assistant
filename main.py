# Take user input (Speech)

import speech_recognition as sr
from speech.stt import refined_stt
import asyncio
from openai.helpers import LocalAudioPlayer
from openai import AsyncOpenAI
from langgraph_flow import graph
import json

openai = AsyncOpenAI()


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
                    # asyncio.run(speak(text="Exiting as requested. Goodbye!"))
                    break

                input_state = {"message": [{"role": "user", "content": refined_input}]}
                result = graph.invoke(input_state)

                final_message = result["messages"][-1].content
                print("Assistant: ", final_message)
            except sr.UnknownValueError:
                print("Apologies, the audio wasn't clear enough. Try Again!")
                # asyncio.run(speak(text="Apologies, the audio wasn't clear enough. Try again!"))
            except sr.RequestError as e:
                print("There was an issue retrieving results. Error: {0}".format(e))


async def speak(text: str):
    async with openai.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",  # try other voices
        input=text,
        instructions="Speak in a cheerful and positive tone.",
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)


if __name__ == "__main__":
    main()
