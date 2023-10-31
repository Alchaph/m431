import speech_recognition as sr
import openai
from gtts import gTTS
import os

# Set up your OpenAI API key
openai.api_key = 'Your API Key for Chat GPT'

# Initialize the recognizer
r = sr.Recognizer()

def get_voice_input(timeout=5):
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = r.listen(source, timeout=timeout)
            print("Processing...")
            command = r.recognize_google(audio)
            print("You said: " + command)
            return command
        except sr.WaitTimeoutError:
            print("No speech input detected within the specified timeout.")
            return ""
        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said.")
            return ""
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            return ""

# Initialize a conversation variable to store the ongoing conversation
conversation = []

while True:
    command = get_voice_input(timeout=5)  # Adjust the timeout as needed

    if command.lower() == "exit":
        break  # Exit the loop if "exit" is said.

    if command:
        # Add the user's message to the conversation
        conversation.append({"role": "user", "content": command})

        try:
            # Use Chat models for conversation
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation
            )
           
            if response["choices"] and response["choices"][0]["message"]["content"]:
                text_response = response["choices"][0]["message"]["content"]
                print("Response: " + text_response)

                # Use gTTS for text-to-speech
                tts = gTTS(text_response)
                tts.save("response.mp3")
                os.system("mpg321 response.mp3")
            else:
                print("No valid response from the Chat model.")
        except Exception as e:
            print("An error occurred while processing your request:", e)

        # Add the AI's message to the conversation
        conversation.append({"role": "assistant", "content": text_response})
