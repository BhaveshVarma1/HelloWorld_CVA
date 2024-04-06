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
            text = r.recognize_whisper(audio)
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



def main():
    count= 1
    while(1):
        #create new directory for each new 
        current_output_dir = dir_maker(f'./output/o_{count}')



        textOutput = stt()
        audioOutputTempDir = tts(input=textOutput, language='en',filename=f'{current_output_dir}/o_{count}.mp3')



        # os.rename("./output/temp/output.mp3", f"{current_output_dir}/o_{count}.mp3")
        f = open(f"./{current_output_dir}/o_{count}.txt", "a")
        f.write(textOutput)
        f.close()

        count = count + 1
        




 
 
if __name__ == "__main__":
    main()