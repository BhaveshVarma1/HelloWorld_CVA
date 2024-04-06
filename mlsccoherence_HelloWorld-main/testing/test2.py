from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
# Callbacks support token-wise streaming
import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import shutil

def stt():
    r = sr.Recognizer()
 
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("You may speak.........")
        audio = r.listen(source)
 
        print("Recognizing Now .... ")
 
 
        # recognize speech using google
 
        try:
            text = r.recognize_google(audio)
            print("You have said \n" + text)
            return text
            print("Audio Recorded successfully \n ")
        except Exception as e:
            print("Error :  " + str(e))
 
 
        # write audio
        # with open("recorded.wav", "wb") as f:
        #     f.write(audio.get_wav_data())

def tts(input, language='en', filename='./output/temp/output.mp3'):
    tts = gTTS(text=input, lang=language, slow=False, tld="co.in")
    tts.save(filename)
    print(f"Text converted to speech and saved as {filename}")
    playsound.playsound(filename)
    return filename

def dir_maker(dir_name):
    try:
        os.makedirs(dir_name)
        return dir_name
    except Exception as e:
        print(f"Encountered the following error {e}")


MODEL_PATH = "h.gguf"

def load_model() -> LlamaCpp:
    """Loads Llama Models"""
    callback_manager: CallbackManager = CallbackManager([StreamingStdOutCallbackHandler()])

    Llama_model: LlamaCpp = LlamaCpp(model_path=MODEL_PATH,
                           temperature=0.5, 
                           max_tokens= 100, 
                           top_p= 1, 
                           callback_manager = callback_manager, 
                           verbose=True)
    return Llama_model



# while True:

#     llm = load_model()

#     model_prompt: str = 'Question' + input("Question : ")
#     response: str = llm(model_prompt)
#     print(response)









def main():
    count= 1
    while(1):
        #create new directory for each new 
        current_output_dir = dir_maker(f'./output/o_{count}')



        llm = load_model()
        textInput = stt()
        model_prompt = "assume you are a customer care agent and you have to answer their queries in shortest and quickest format . answer this following one :" + textInput
        response: str = llm(model_prompt)

        audioOutputTempDir = tts(input=response, language='en',filename=f'{current_output_dir}/o_{count}.mp3') 



        # os.rename("./output/temp/output.mp3", f"{current_output_dir}/o_{count}.mp3")
        f = open(f"./{current_output_dir}/o_{count}.txt", "a")
        f.write(textInput)
        f.close()

        count = count + 1
        




 
 
if __name__ == "__main__":
    main()