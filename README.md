# **Charlie - Voice AI Assistant using DeepSeek R1**

Charlie is a real-time voice-based AI assistant powered by the DeepSeek R1 model via Ollama. It listens for a wake word, understands voice commands, responds in a friendly tone, and saves full conversation transcripts locally.

## **Features**

* Wake word detection ("Charlie") to activate the assistant.  
* Real-time speech recognition using `speech_recognition`.  
* AI-powered responses from DeepSeek R1 (7B model) via Ollama.  
* Text-to-speech output using `pyttsx3`.  
* Saves conversation transcripts as `.json` and `.txt` files.  
* Fully offline operation (no API keys required).  
* Automatically generates a custom title for each saved transcript.

## **Prerequisites**
### **Install Dependencies**
Run the following command to install the required Python libraries:

> *pip install speechrecognition pyttsx3 ollama*

*You may need to run pip3 depending on your version of Python installed.*

### **Install PortAudio (Required for SpeechRecognition)**
* Debian/Ubuntu:
> *sudo apt install portaudio19-dev*

* MacOS:
> *brew install portaudio*

### **Install PyAudio**
> *pip install pyaudio*
### **Download DeepSeek R1 Model**
Since this script uses DeepSeek R1 via [Ollama](https://ollama.com/), install Ollama and pull the model:
> *ollama pull deepseek-r1:7b*

## **Usage**
Run the script to start Charlie:
> *python main.py*

*You may need to run python3 depending on your version of Python installed.*

> ⚠️ Note: If you're using a virtual environment, make sure it's activated before installing and running the script.
You may encounter an error that says you're not in the same virtual environment as your dependencies (e.g. ModuleNotFoundError).
To fix this, activate your virtual environment again or reinstall dependencies inside the correct environment.

### **How It Works**
1\. Charlie waits until it hears the "Charlie" keyword in your input.

2\. Listens to your voice, converts it to text.

3\. Sends the text to DeepSeek R1 to generate a response.

4\. Speaks the response back to you using pyttsx3.

5\. When you say "exit", "quit", or "bye" in your input, it ends the session and saves a transcript with a unique title.

6\. Check out the transcript of your conversation in the folder!

## Why Is There a Delay After Speaking?

You may notice a few seconds of lag between your speech input and the program’s response. This is expected and happens due to several factors:

### Causes of Delay

1. **Ambient Noise Calibration**
   - The program uses `recognizer.adjust_for_ambient_noise(source)` to adapt to background sounds. This takes about 1 second and must be done before speech begins.
   - If you speak during this adjustment period, the input may be misinterpreted or missed.

2. **Listening Time**
   - The microphone continues listening until a moment of silence is detected. This ensures your full sentence is captured before processing.

3. **Speech Recognition**
   - The audio is sent to Google's speech-to-text API, which adds processing and network delay.
   - This external API can take a second or two to return your transcribed speech.

4. **Response Generation**
   - Using a large language model to generate a reply, there is an additional delay for inference and response construction.

## **Customization**
* **Change the AI's personality:**
Edit the initial `system` messages inside `self.full_transcript` to set tone and behavior.

* **Adjust voice settings:**
Modify `pyttsx3` properties (rate, volume, voice) in `__init__()`.

* **Use a different AI model:**
Replace `deepseek-r1:7b` with any other model supported by Ollama.

* **Implement a GUI for the program:**:
Use a web framework like `Flask` or GUI libraries like `Pygame` or `Tkinter` for an interface to interact with.

## **Notes**
* No API keys are required — works fully offline for transcription and TTS.

* Accuracy depends on your mic quality and ambient noise.

* When running the program, wait about 1–2 seconds before speaking to allow it to adjust to ambient noise. Speak clearly and at a moderate volume for best results.

## **License**
* This project is open-source and free to use. 🙂






