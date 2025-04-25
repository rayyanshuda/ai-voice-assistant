import re
import ollama
import pyttsx3  
import speech_recognition as sr  
import subprocess
import sys

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
        ]
        
    
    def speak_mac(self, text):
        #subprocess.run(["say", "-v", "Samantha", "-r", "200", text])
        self.engine.say(text)
        self.engine.runAndWait()

    def listen_to_user(self):
        with self.microphone as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1.5)
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
        #print(f"\nUser: {user_text}")

        ollama_response = ollama.chat(
            model="deepseek-r1:7b",
            messages=self.full_transcript
        )

        ai_text = ollama_response["message"]["content"].strip()
        #print("TARS:", ai_text)

        # Remove content between <think> and </think> tags
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
                    #print(f"Heard: {phrase}")
                    if "charlie" in phrase:
                        print(f"User Input: {phrase}")
                        print("Charlie: I'm listening.")
                        self.speak_mac("I'm listening.")
                        return  # exit sleep mode
                except (sr.WaitTimeoutError, sr.UnknownValueError, sr.RequestError):
                    continue  # keep listening

    def start_chat(self):
        print("Hello! I'm Charlie. How can I assist you today?")
        while True:
            self.wait_for_wake_word()  # Wait until user says "Hey Charlie"
            while True:
                user_input = self.listen_to_user()
                
                
                if user_input is None:
                    print("No input detected. Going back to sleep...")
                    break  # go back to sleep mode
                    #continue

                if "open google" in user_input.lower():
                    self.engine.say("Opening Google.")
                    subprocess.run(["open", "https://www.google.com"])
                    self.engine.runAndWait()
                    continue #or break?

                if "open youtube" in user_input.lower():
                    self.engine.say("Opening YouTube.")
                    subprocess.run(["open", "https://www.youtube.com"])
                    self.engine.runAndWait()
                    continue #or break?
                
                #if user_input.lower() in ["exit", "quit", "bye"]: #only works if the user says "exit", "quit", or "bye" not if it's in the middle of a sentence
                if any(kw in user_input.lower() for kw in ["bye", "exit", "quit"]):
                    print("Charlie: Goodbye!")
                    self.engine.say("Goodbye!")
                    self.engine.runAndWait()
                    sys.exit(0)
                
                self.generate_ai_response(user_input)

"""
    def start_chat(self):
        print("Charlie is starting up...")
        while True:
            self.wait_for_wake_word()  # Wait until user says "Hey Charlie"
            
            while True:
                user_input = self.listen_to_user()
                if user_input is None:
                    print("No input detected. Going back to sleep...")
                    break  # go back to sleep mode

                if any(kw in user_input.lower() for kw in ["bye", "exit", "quit"]):
                    print("Charlie: Goodbye!")
                    self.speak_mac("Goodbye!")
                    return
                
                self.generate_ai_response(user_input)
"""

ai_voice_agent = AIVoiceAgent()
ai_voice_agent.start_chat()
