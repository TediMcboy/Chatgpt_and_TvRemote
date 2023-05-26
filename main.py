import sys
import remoteControl
import openai
import time
import speech_recognition as sr
from colorama import Fore, Back, Style

print(sys.version)
#print(Fore.RED + 'some red text')

remoteControl.wakeonlan.send_magic_packet('54:bd:79:40:4d:7d')  #wake samsung tv cia MAC address

openai.api_key = "***********************"  #REPLACE WITH YOUR OPENAI API KEY 

messages = [ {"role": "system", "content": "You are a intelligent assistant"}]

# Initialize the recognizer
r = sr.Recognizer()

def lastWord(string):
    # split by space and converting
    # string to list and
    lis = list(string.split(" "))
    # length of list
    length = len(lis)
    # returning last element in list
    return lis[length - 1]

def loading_bar(): #simple loading bar to indicate user input has been recognized
    print("\n")
    for i in range(20):
        time.sleep(0.1)
        print(Fore.WHITE+'\rThinking [' + '#' * i + ' ' * (20-i) + ']', end='')
def listen():
    try:
        # use the microphone as source for input.
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)
            print(Fore.MAGENTA+"\nspeak now or forever hold your silence")
            # listens for the user's input
            audio2 = r.listen(source2)

            # Using google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
            print(Fore.GREEN +"\nYou: ", MyText)

            if "turn on the tv" in MyText or "turn off the tv" in MyText:
                print("Toggling tv power switch")
                remoteControl.tv.send_key("KEY_POWER")

            elif "turn up volume" in MyText:
                print("increasing volume by", MyText[-1])
                try:
                    remoteControl.vol_up(int(MyText[-1]))
                except:
                    print("try again")
            elif "turn down volume" in MyText:
                print("decreasing volume by", MyText[-1])
                try:
                    remoteControl.vol_down(int(MyText[-1]))
                except:
                    print("try again")
            elif "go back" in MyText:
                print("going back")
                remoteControl.back()
            elif "move right by" in MyText:
                if lastWord(MyText) == "one":
                    MyText = 1
                    print("moving right by", MyText)
                    remoteControl.right(int(MyText))
                else:
                    remoteControl.right(int(MyText[-1]))
            elif "move left by" in MyText:
                if lastWord(MyText) == "one":
                    MyText = 1
                    print("moving left by", MyText)
                    remoteControl.left(MyText)
                else:
                    remoteControl.left(int(MyText[-1]))
            elif MyText == "select" :
                print("pressing enter")
                remoteControl.enter()
            elif "pause show" in MyText or "play show" in MyText or "pause movie" in MyText or "play movie" in MyText:
                print("pressing enter")
                remoteControl.enter()
            elif "open hbo" in MyText:
                print("opening HBO")
                #remoteControl.open_hbo()
                #remoteControl.tv.run_app('3201601007230')
                app = remoteControl.tv.rest_app_run('3201601007230')  # hbo
                remoteControl.logging.info(app)
            elif "close hbo" in MyText:
                print("closing HBO")
                remoteControl.close_hbo()
            elif "open prime video" in MyText or "open amazon" in MyText:
                print("opening Amazon Video")
                #remoteControl.tv.run_app('3201512006785')  # prime video
                app = remoteControl.tv.rest_app_run('3201512006785')  # primevideo
                remoteControl.logging.info(app)
            elif "open hulu" in MyText:
                print("opening hulu")
                #remoteControl.tv.run_app('3201601007625') #hulu
                app = remoteControl.tv.rest_app_run('3201601007625')  # hulu
                remoteControl.logging.info(app)
            elif "open disney" in MyText:
                print("opening Disney")
                app = remoteControl.tv.rest_app_run('3201901017640') #Disney
                remoteControl.logging.info(app)
                #remoteControl.tv.run_app('3201901017640') #Disney

            else:
                message = MyText
                if message:
                    loading_bar()
                    messages.append(
                        {"role": "user", "content": message},

                    )
                    chat = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo", messages=messages
                    )

                reply = chat.choices[0].message.content  #Get response from OpenAI API 

                print(Fore.BLUE+"\nComputer: {}".format(reply)) 
                messages.append({"role": "assistant", "content": reply})
                #SpeakText(reply)

    except sr.RequestError as e:  #catch errors
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:# catch error if no comprehensible speech is inputted
        print("no speech detected")

while (True):
    listen()





