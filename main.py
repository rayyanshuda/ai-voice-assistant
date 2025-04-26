import re
import ollama
import pyttsx3  
import speech_recognition as sr  
import subprocess
import sys
import os
import json
from datetime import datetime
import string

class AIVoiceAgent:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        voices = self.engine.getProperty('voices')
        #self.engine.setProperty('voice', 'com.apple.speech.synthesis.voice.alex')

        self.full_transcript = [
            {"role": "system", "content": "You are an AI called Charlie. Answer questions in less than 300 characters."},
            {"role": "system", "content": "Keep your tone friendly, clear, and casual."},
        ]
        
    def speak_mac(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen_to_user(self):
        with self.microphone as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
            try:
                print("Recognizing...")
                text = self.recognizer.recognize_google(audio)
                print(f"User Input: {text}")
                return text
            except sr.UnknownValueError:
                print("Sorry, I didn't understand that.")
                return None
            except sr.RequestError:
                print("Sorry, I'm having trouble accessing the speech recognition service.")
                return None

    def generate_ai_response(self, user_text):
        self.full_transcript.append({"role": "user", "content": user_text})

        ollama_response = ollama.chat(
            model="deepseek-r1:7b",
            messages=self.full_transcript
        )

        ai_text = ollama_response["message"]["content"].strip()
        ai_text = re.sub(r'<think>.*?</think>', '', ai_text, flags=re.DOTALL).strip()

        print("Charlie:", ai_text)
        self.speak_mac(ai_text)
        
        self.full_transcript.append({"role": "assistant", "content": ai_text})

    def wait_for_wake_word(self):
        print("Charlie is sleeping... Say 'Hey Charlie' to wake me up.")
        while True:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                try:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
                    phrase = self.recognizer.recognize_google(audio).lower()
                    if "charlie" in phrase:
                        print(f"User Input: {phrase}")
                        print("Charlie: I'm listening.")
                        self.speak_mac("I'm listening.")
                        return
                except (sr.WaitTimeoutError, sr.UnknownValueError, sr.RequestError):
                    continue

    def save_transcript(self):
        os.makedirs("transcripts/JSON", exist_ok=True)
        os.makedirs("transcripts/TXT", exist_ok=True)

        title_prompt = {
            "role": "user",
            "content": (
                "Based on our entire conversation so far, generate a short and intuitive title "
                "(3 to 5 words max) that summarizes what we talked about. Put the title in double quotes."
            )
        }

        try:
            response = ollama.chat(
                model="deepseek-r1:7b",
                messages=self.full_transcript + [title_prompt]
            )
            ai_text = response["message"]["content"].strip()

            # Remove any <think> blocks
            ai_text = re.sub(r'<think>.*?</think>', '', ai_text, flags=re.DOTALL).strip()

            # Extract title in double quotes if present
            match = re.search(r'"([^"]{3,80})"', ai_text)
            if match:
                clean_title = match.group(1)
            else:
                clean_title = ai_text.split("\n")[0]

            clean_title = re.sub(r"[^\w\s-]", "", clean_title)  # remove punctuation
            clean_title = "_".join(clean_title.split()[:5])  # limit to 5 words

            if not clean_title:
                clean_title = "untitled_chat"

        except Exception as e:
            print(f"Failed to generate title, using default. Reason: {e}")
            clean_title = "untitled_chat"

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"{timestamp}_{clean_title}"

        json_path = f"transcripts/JSON/{base_filename}.json"
        txt_path = f"transcripts/TXT/{base_filename}.txt"

        with open(json_path, "w") as f_json:
            json.dump(self.full_transcript, f_json, indent=2)

        with open(txt_path, "w") as f_txt:
            for entry in self.full_transcript:
                f_txt.write(f"{entry['role'].capitalize()}: {entry['content']}\n\n")

        print(f"Transcript saved as:\n→ {json_path}\n→ {txt_path}")

    def start_chat(self):
        print("Hello! I'm Charlie. How can I assist you today?")
        while True:
            self.wait_for_wake_word()
            while True:
                user_input = self.listen_to_user()
                
                if user_input is None:
                    print("No input detected. Going back to sleep...")
                    break

                if "open google" in user_input.lower():
                    self.engine.say("Opening Google.")
                    subprocess.run(["open", "https://www.google.com"])
                    self.engine.runAndWait()
                    continue

                if "open youtube" in user_input.lower():
                    self.engine.say("Opening YouTube.")
                    subprocess.run(["open", "https://www.youtube.com"])
                    self.engine.runAndWait()
                    continue

                if any(kw in user_input.lower() for kw in ["bye", "exit", "quit"]):
                    print("Charlie: Goodbye!")
                    self.engine.say("Goodbye!")
                    self.engine.runAndWait()
                    self.save_transcript()
                    sys.exit(0)

                self.generate_ai_response(user_input)

if __name__ == "__main__":
    ai_voice_agent = AIVoiceAgent()
    ai_voice_agent.start_chat()

#add a message after bye that you're making a transcript and also change ambient background detection