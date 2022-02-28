from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig
import azure.cognitiveservices.speech as speechsdk
from threading import Thread
from pygame import mixer
import pyjokes
import pywhatkit
import getpass
import os
from PIL import Image
import random
import wikipedia
import ssl
from bs4 import BeautifulSoup
import geocoder
from geopy.geocoders import Nominatim
import webbrowser
import pymongo
from getmac import get_mac_address as gma
import cv2
import face_recognition
import smtplib
import datetime
import re, requests, urllib.parse, urllib.request
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
import app
import wave
import contextlib
import playsound

#Variable Declaration
name="User"
task={}
filename1=[]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

#COSMOSDB Database
CONNECTION_STRING = "mongodb://edencosmosdb:DSCa5Ab2GwzzvufFtGPim9PiUcSs7Z2nETiF0mxEQJsSEDuQ5ame2CTamkQjYb0QoH8s5jnEu8EbHCYnzevWKA==@edencosmosdb.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@edencosmosdb@"
client = pymongo.MongoClient(CONNECTION_STRING)
client.server_info()
db=client['location']
collection=db['location']


# Text To Speech(Azure)
speech_config = SpeechConfig(subscription="40f2c24c83af474aa2a3bfd2a8913b97", region="centralindia") 
speech_config.speech_synthesis_language = "en-US" 
speech_config.speech_synthesis_voice_name ="en-US-SaraNeural"
speech_config.set_speech_synthesis_output_format(SpeechSynthesisOutputFormat["Riff24Khz16BitMonoPcm"])
synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=None)

# Speech To Text(Azure)
speech_config = speechsdk.SpeechConfig(subscription="40f2c24c83af474aa2a3bfd2a8913b97", region="centralindia")
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

#All Function Declaration
def reply(audio):
    app.ChatBot.addAppMsg(audio)
    return audio

def replyUser(audio):
    app.ChatBot.addUserMsg(audio)
    return audio

def strike(text):
    return ''.join([u'\u0336{}'.format(c) for c in text])

def location():
    chrome_options = Options()

    # SET CHROME OPTIONS
    chrome_options.add_experimental_option("prefs", { "profile.default_content_setting_values.geolocation": 1})

    # SET CAPABILITY
    desired_cap = chrome_options.to_capabilities()
    desired_cap.update({
      'browser_version': '75.0',
      'os': 'Windows',
      'os_version': '10'
    })
    driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=desired_cap)
    driver.maximize_window()
    driver.set_window_position(0,0)
    driver.get('https://www.google.com/maps/')
    time.sleep(4.5)
    driver.find_element_by_xpath('/html/body/div[3]/div[9]/div[22]/div[1]/div[2]/div[5]/div/button').click()
    time.sleep(2.5)
    driver.find_element_by_xpath('/html/body/div[3]/div[9]/div[1]/div[3]/canvas').click()
    time.sleep(1.5)
    Latitude,Longitude=driver.find_element_by_xpath('/html/body/div[3]/div[9]/div[22]/div[1]/div[1]/div[2]/div/div[2]/button[2]').get_attribute('aria-label').split(", ")
    driver.quit()
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse(Latitude+","+Longitude)
    try:
        document_id = collection.insert_one({'_id': ''.join(i for i in gma() if not i.isdigit()).replace(":",""),'location':str(location)}).inserted_id
    except:
        collection.update_one({"_id": ''.join(i for i in gma() if not i.isdigit()).replace(":","")}, {"$set":{'location': str(location)}})

def weather(city):
    city = city.replace(" ", "+")
    res = requests.get(f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    location = soup.select('#wob_loc')[0].getText().strip()
    info = soup.select('#wob_dc')[0].getText().strip()
    weather = soup.select('#wob_tm')[0].getText().strip()
    greetings=["Hello, I am Eden","Hey, I am Eden","Greetings, I am Eden","Namaste, I am Eden","Bonjour, I am Eden","Hola, I am Eden"]
    timewait=speak(reply(greetings[random.randint(0,5)]))
    time.sleep(timewait)
    timewait=speak("In "+location)
    time.sleep(timewait)
    timewait=speak("It is ")
    time.sleep(timewait-0.1)
    if(datetime.datetime.strptime(str(datetime.datetime.now().strftime("%H:%M")), "%H:%M").strftime("%I")[0]=='0'):
        speak(datetime.datetime.strptime(str(datetime.datetime.now().strftime("%H:%M")), "%H:%M").strftime("%I")[1])
    else:
        speak(datetime.datetime.strptime(str(datetime.datetime.now().strftime("%H:%M")), "%H:%M").strftime("%I"))
    time.sleep(0.8)
    if(datetime.datetime.strptime(str(datetime.datetime.now().strftime("%H:%M")), "%H:%M").strftime("%M")[0]=='0'):
        speak(datetime.datetime.strptime(str(datetime.datetime.now().strftime("%H:%M")), "%H:%M").strftime("%M")[1],"o")
    else:
        speak(datetime.datetime.strptime(str(datetime.datetime.now().strftime("%H:%M")), "%H:%M").strftime("%M"),"o")               
    time.sleep(0.8)
    if(datetime.datetime.now().hour>12):
        timewait=speak("P M","ui")
        time.sleep(timewait-0.1)
    else:
        timewait=speak("A M")
        time.sleep(timewait)
    timewait=speak("The Temperature is "+weather+"Degree Celcius","oi")
    time.sleep(timewait)
    
def weather_main():
    g = geocoder.ip('me')
    Latitude = str(g.latlng[0])  
    Longitude = str(g.latlng[1]) 
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse(Latitude+","+Longitude)
    address = location.raw['address']
    city_name=address['city']
    api_key = "da1f94efa4d6cefb2ed01470906d553f"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    city_name = city_name+" weather"
    weather(city_name)
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        timewait=speak("Humidity is " +str(current_humidity) + "percentage","op")
        time.sleep(timewait)
        
        if(("thunderstorm" in str(weather_description)) or ("rain" in str(weather_description)) or ("shower" in str(weather_description))):
            timewait=speak("You Might Need An Umbrella!")
            time.sleep(timewait)
        elif(("clear" in str(weather_description)) or ("sunny" in str(weather_description))):
            timewait=speak("We Have A Clear Sky!")
            time.sleep(timewait)
        elif("cloudy" in str(weather_description)):
            timewait=speak("The Sky Might Be Cloudy!")
            time.sleep(timewait)
        elif("haze" in str(weather_description)):
            timewait=speak("We Have A Hazy Weather Ahead!")
            time.sleep(timewait)
        else:
            timewait=speak("It's "+str(weather_description)+" Today","ooP")
            time.sleep(timewait)
        timewait=speak("Have a Nice Day!")
        time.sleep(timewait+1)

def speak(text,tp="1"):
    date_string = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
    result = synthesizer.speak_text_async(text).get() 
    stream = AudioDataStream(result)
    audiofilename='speech'+date_string+tp+'.wav'
    mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
    stream.save_to_wav_file(audiofilename)
    try:
        os.remove('pywhatkit_dbs.txt')
    except:
        pass
    filename1.append(audiofilename)
    if(len(filename1)>12):       
        for i in range(0,5):
            os.remove(filename1[i])
            filename1.pop(i)
    mixer.music.load(audiofilename)
    mixer.music.play()
    with contextlib.closing(wave.open(audiofilename,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)    
    return duration

try:
    foundPic=False
    for file in os.listdir("./"):
        filename = os.fsdecode(file)
        if filename.endswith(".jpg"):
            imgloaded=face_recognition.load_image_file(filename)
            imgloaded=cv2.cvtColor(imgloaded,cv2.COLOR_BGR2RGB)
            camera = cv2.VideoCapture(0)
            return_value, image = camera.read()
            cv2.imwrite(os.path.join('./' , 'testimage.jpg'), image)
            imgtest=face_recognition.load_image_file('./testimage.jpg')
            imgtest=cv2.cvtColor(imgtest,cv2.COLOR_BGR2RGB)
            faceloc=face_recognition.face_locations(imgloaded)[0]
            encodeloaded=face_recognition.face_encodings(imgloaded)[0]
            cv2.rectangle(imgloaded,(faceloc[3],faceloc[0]),(faceloc[1],faceloc[2]),(255,0,255),2)
            faceloctest=face_recognition.face_locations(imgtest)[0]
            encodetest=face_recognition.face_encodings(imgtest)[0]
            cv2.rectangle(imgtest,(faceloc[3],faceloc[0]),(faceloc[1],faceloc[2]),(255,0,255),2)
            results=face_recognition.compare_faces([encodeloaded],encodetest)
            foundPic=True
            if(results[0]):
                foundPic=True
                name=filename.replace(".jpg","")
                os.remove('testimage.jpg')
                camera.release()
                break
    if(not foundPic):
        timewait=speak("What's Your Name? ")
        time.sleep(timewait)
        print("Listening")
        MyText = speech_recognizer.recognize_once_async().get()
        name=MyText.text[:-1].lower()
        camera = cv2.VideoCapture(0)
        return_value, image = camera.read()
        date_string = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
        cv2.imwrite(os.path.join('./' , name+'.jpg'), image)
        camera.release()
        
except:
    timewait=speak("What's Your Name? ")
    time.sleep(timewait)
    print("Listening")
    MyText = speech_recognizer.recognize_once_async().get()
    name=MyText.text[:-1].lower()

    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    date_string = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
    cv2.imwrite(os.path.join('./' , name+'.jpg'), image)
    camera.release() 

#Threading The Program
t1 = Thread(target = app.ChatBot.start)
t1.start()

while(1):
    try:
        time.sleep(2)
        if(app.ChatBot.isUserInput()):
            MyText = app.ChatBot.popUserInput()
            MyText = MyText.lower()
        else:
            MyText = speech_recognizer.recognize_once_async().get()
            MyText=MyText.text[:-1].lower()
            if(MyText==""):
                continue
        replyUser(MyText.capitalize())

        if("joke" in MyText):
            My_joke = pyjokes.get_joke(language="en", category="all")
            reply(My_joke)
            time1 = speak(My_joke,"joke")
            time.sleep(int(time1))
            
        elif("music" in MyText or "song" in MyText):
            driver = webdriver.Chrome(ChromeDriverManager().install())
            driver.maximize_window()
            driver.set_window_position(-10000,0)
            driver.get('https://www.youtube.com/results?search_query=my+mixes')
            time.sleep(2)
            driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-playlist-renderer[1]/ytd-playlist-thumbnail/a/div[1]/ytd-playlist-video-thumbnail-renderer/yt-img-shadow/img').click()
            time.sleep(6.5)
            try:
                driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div/div/div/ytd-player/div/div/div[17]/div/div[3]/div/div[2]/span/button').click()
            except:
                pass
        elif(("messages" in MyText) and ("instagram" in MyText)):
            speak(reply("Please Hold On For A Moment, Let Me Check!"))
            driver = webdriver.Chrome(ChromeDriverManager().install())
            driver.maximize_window()
            driver.set_window_position(-10000,0)
            driver.get('https://www.instagram.com')
            time.sleep(2)
            driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input').send_keys('__kkarann__')
            driver.find_element_by_name('password').send_keys ('Kral_stark@12345') 
            time.sleep(3)
            driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]').click()
            time.sleep(3)
            driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/div/button').click()
            time.sleep (2)
            driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[2]').click()
            time.sleep (1)
            speak(reply("You Have "+str(driver.find_element_by_class_name("bqXJH").text)+" Messages On Instagram"))
            driver.quit()
        
        elif(("thanks" in MyText) or ("thank" in MyText)):
            welcomeReply=["You Got It!","Your Welcome","Mention Not"]
            timewait=speak(reply(welcomeReply[random.randint(0,3)]))
            time.sleep(timewait)
        
        elif((("who" in MyText) and ("you" in MyText)) or ("introduce" in MyText)):
            comment=["Hey! i am your personal assistant, Eden, What's up?","I am Eden, Your Assistant, i can do many things, all you have to do is ask.","I am Eden, I am here to help you, let me know if you need anything."]
            timewait=speak(reply(comment[random.randint(0,3)]))
            time.sleep(timewait)

        elif(("doing" in MyText) and ("what" in MyText)):
            botDoing=["Waiting For Your Command","Glancing Through Trillions Of Bytes Of Data","Hanging Around, What Do You Want Me To Do?"]
            timewait=speak(reply(botDoing[random.randint(0,3)]))
            time.sleep(timewait)

        elif(("check" in MyText) and ("up" in MyText)):
            split_sentence = MyText.split(' ')
            url=""
            for i in range(split_sentence.index('if')+1,split_sentence.index('is')):
                if("dot" == split_sentence[i]):
                    url+="."
                else:
                    url+=split_sentence[i]
            print(url)
            if('www' not in url):
                r = requests.head("https://www."+url)     
            else:
                r = requests.head("https://"+url)
            if(r.status_code == 200):
                speak(reply("The Website Is Up & Running"))
                
        elif(("open" in MyText)):
            split_sentence = MyText.split(' ')
            url=""
            for i in split_sentence:
                if(i=="open"):
                    continue
                if(i=="dot"):
                    url+="."
                else:
                    url+=i
            webbrowser.open_new(url)
            speak(reply("Right On It!"))
            
        elif(("hello" in MyText) or ("update" in MyText) or ("hi" in MyText) or ("hey" in MyText) or ("morning" in MyText) or ("afternoon" in MyText) or ("evening" in MyText)):
            speak(reply(name.title()),"iu")
            time.sleep(1)
            weather_main()
            if(task):
                reply(str(len(task))+" Item Remaining In Task List")
                timewait=speak("Also, "+name+" You Have Some Tasks Remaining To Complete")
                time.sleep(timewait)
                for key in task:
                        speak(reply("In "+key.title()+" You Have"),"o")
                        time.sleep(2)
                        for keys in task[key]:
                            reply(" • "+keys.title())
                            wait=speak(keys,"oo")
                            time.sleep(wait)
                timewait=speak("Be Sure To Complete Them","ui")
                time.sleep(timewait)

        elif("time" in MyText):
            speak(name,"iu")
            time.sleep(1)
            speak("The Time Is","O")
            time.sleep(0.9)
            if(datetime.datetime.strptime(str(datetime.datetime.now().strftime("%H:%M")), "%H:%M").strftime("%I")[0]=='0'):
                speak(datetime.datetime.strptime(str(datetime.datetime.now().strftime("%H:%M")), "%H:%M").strftime("%I")[1])
            else:
                speak(datetime.datetime.strptime(str(datetime.datetime.now().strftime("%H:%M")), "%H:%M").strftime("%I"))
            time.sleep(0.8)
            if(datetime.datetime.strptime(str(datetime.datetime.now().strftime("%H:%M")), "%H:%M").strftime("%M")[0]=='0'):
                speak(datetime.datetime.strptime(str(datetime.datetime.now().strftime("%H:%M")), "%H:%M").strftime("%M")[1],"o")
            else:
                speak(datetime.datetime.strptime(str(datetime.datetime.now().strftime("%H:%M")), "%H:%M").strftime("%M"),"o")               
            time.sleep(0.8)
            if(datetime.datetime.now().hour>12):
                timewait=speak("P M","ui")
                time.sleep(timewait-0.1)
            else:
                timewait=speak("A M")
                time.sleep(timewait)

        elif((("remove" in MyText) or ("delete" in MyText)) and ("all" in MyText) and (("list" in MyText) or ("task" in MyText))):
            task={}
            reply(strike("All Tasks Deleted"))
            mixer.init()
            mixer.music.load(r".//web//audio//chalk.mp3") 
            mixer.music.play()
            speak("All Tasks Deleted")
        
        elif((("remove" in MyText) or ("check" in MyText) or ("cross" in MyText)) and ("list" in MyText)):         
            split_sentence = MyText.split(' ')
            listtobeupdated=task[split_sentence[split_sentence.index("list")-1]]
            string=""
            for i in range(split_sentence.index("remove")+1,split_sentence.index("from")):
                if(i==split_sentence.index("from")-1):
                    string+=split_sentence[i]
                else:
                    string+=split_sentence[i]+" "
            if(string in listtobeupdated):
                listtobeupdated.remove(string)
            reply("Removed "+str(strike(string))+" from the list")
            mixer.init()
            mixer.music.load(r".//web//audio//chalk.mp3") 
            mixer.music.play()
            timewait=speak("Removed "+str(string)+" from the list")
            time.sleep(2)
            speak(reply("List Updated!"))

        elif(("siri" in MyText) or ("google assistant" in MyText) or ("alexa" in MyText)):
            comment=["She Seems Clever!","Full Respect, Being An Assistant Is Hardwork","I Know Her, She Is Amazing","You Know Her? That's Great!"]
            timewait=speak(reply(comment[random.randint(0,4)]))
            time.sleep(timewait)

        elif("date" in MyText):
            speak(name,"iu")
            time.sleep(1)
            x = datetime.datetime.now()
            speak("It's "+str(x.strftime("%A")))
            time.sleep(0.85)
            speak(str(x.strftime("%d")).replace("0",""),"i")
            time.sleep(0.8)
            speak(x.strftime("%B"),"P")
            time.sleep(0.8)
            speak(str(x.year),"OP")
            time.sleep(0.8)

        elif("id" in MyText):
            location()
            speak(name,"iu")
            time.sleep(1)
            timewait=speak(reply("Please Note Down Your ID "))
            time.sleep(timewait)
            time.sleep(0.5)
            timewait=speak(reply(''.join(i for i in gma() if not i.isdigit()).replace(":","")),"io")
            print(''.join(i for i in gma() if not i.isdigit()).replace(":",""))
            time.sleep(timewait)

        elif("location" in MyText):
            MyText=MyText.lower()
            split_sentence = MyText.split(' ')
            idd=''.join([str(elem) for elem in split_sentence[split_sentence.index("of")+1:]]).lower()
            timewait=speak(reply("Last Updated Location Is "+collection.find_one({"_id": idd})["location"]))
            time.sleep(timewait) 

        elif("mail" in MyText):
            port = 587  
            smtp_server = "smtp.gmail.com"
            sender_email = "techtrends288@gmail.com"
            speak("What's The Receiver's Mail I D")
            reply("What's The Receiver's Mail ID")
            recemail = app.ChatBot.popUserInput()
            replyUser(recemail)
            speak(reply("What's Your Password"))
            password = app.ChatBot.popUserInput()
            replyUser("•"*len(password))
            speak(reply("What's The Subject?"))
            time.sleep(2)
            reply("Speak Now")
            if(app.ChatBot.isUserInput()):
                SUBJECT = app.ChatBot.popUserInput()
            else:
                MyText = speech_recognizer.recognize_once_async().get()
                SUBJECT=MyText.text[:-1].lower()
            replyUser("Subject: "+SUBJECT)
            speak(reply("What Should The Message Say"))
            time.sleep(2)
            reply("Speak Now")
            if(app.ChatBot.isUserInput()):
                message = app.ChatBot.popUserInput()
            else:
                MyText = speech_recognizer.recognize_once_async().get()
                message=MyText.text[:-1].lower()
            replyUser("Message: "+message)
            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, port) as server:
                server.ehlo()  
                server.starttls(context=context)
                server.ehlo()  
                server.login(sender_email, password)
                message = 'Subject: {}\n\n{}'.format(SUBJECT, message)
                server.sendmail(sender_email, recemail, message)
            speak("Message On Its Way!")
            reply("Message Sent!")

        elif("play" in MyText):
            split_sentence = MyText.split(' ')
            url=""
            for i in split_sentence:
                if(i=="play"):
                    continue
                url+=i+" "
            music_name = url
            query_string = urllib.parse.urlencode({"search_query": music_name})
            formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
            search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
            clip = requests.get("https://www.youtube.com/watch?v=" + "{}".format(search_results[0]))
            clip2 = "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])
            webbrowser.open(clip2)
            
        elif("whatsapp" and "message" in MyText):
            if("to" in MyText):
                split_sentence = MyText.split(' ')
                name=split_sentence[-1]
                speak(reply("What's "+name+"'s Phone Number?"))
            else:
                speak(reply("What's Their Phone Number?"))
            time.sleep(2)
            reply("Speak Now")
            MyText = speech_recognizer.recognize_once_async().get()
            MyText=MyText.text[:-1].lower()
            number = MyText.lower().replace(" ", "")
            replyUser("+91 "+number)
            if(len(number)!=10):
                timesleep=speak(reply("The Number Is Invalid, Please Repeat The Correct Number."))
                time.sleep(timesleep)
                MyText = speech_recognizer.recognize_once_async().get()
                MyText=MyText.text[:-1].lower()
                number = MyText.lower().replace(" ", "")
                replyUser("+91 "+number)
            speak(reply("What's The Message? "))
            time.sleep(2)
            reply("Speak Now")
            MyText = speech_recognizer.recognize_once_async().get()
            MyText=MyText.text[:-1].lower()
            replyUser(MyText)
            msg = MyText.lower()
            speak(reply("Please Wait While i Send The Message"))
            try:
                pywhatkit.sendwhatmsg("+91"+number,msg,str(datetime.datetime.now().hour),str(datetime.datetime.now().minute+1))
            except:
                pywhatkit.sendwhatmsg("+91"+number,msg,datetime.datetime.now().hour,datetime.datetime.now().minute+2)
            speak(reply("Message On Its Way!"))
            
        elif("random" and "number" in MyText):
            speak(name,"iu")
            time.sleep(1)
            if("from" and "to" in MyText):
                split_sentence = MyText.split(' ')
                fromIndex=split_sentence.index('from')
                toIndex=split_sentence.index('to')
                speak(reply("Here's Your Random Number "+str(random.randint(int(split_sentence[int(fromIndex)+1]),int(split_sentence[int(toIndex)+1])))))
            else:
                speak(reply("Here's Your Random Number "+str(random.randint(0,100))))
            time.sleep(3)

        elif(("note"  in MyText) or( "write"  in MyText) or( "homework"  in MyText)):
            speak(reply("What's The Content? "))
            time.sleep(2)
            reply("Speak Now")
            MyText = speech_recognizer.recognize_once_async().get()
            MyText=MyText.text[:-1].lower()
            msg = MyText.lower()
            replyUser(msg)
            pywhatkit.text_to_handwriting(msg, save_to="pywhatkit.png")
            image1 = Image.open(r'pywhatkit.png')
            im1 = image1.convert('RGB')
            username=str(getpass.getuser())
            im1.save(r"C:\\Users\\"+username+"\\Documents\\HandWritten.pdf")
            speak("Your HomeWork Is Generated As Handwritten dot p d f")
            reply("Your HomeWork Is Generated As Handwritten.pdf in \n C:\\Users\\"+username+"\\Documents\\HandWritten.pdf")
            time.sleep(3)

        elif(("do"  in MyText) or( "what"  in MyText) or ("where" in MyText) or ("who" in MyText)):
            split_sentence = MyText.split(' ')
            if((split_sentence[-2]!="know") or (split_sentence[-2]!="is") or (split_sentence[-2]!="are") or (split_sentence[-2]!="an") or (split_sentence[-2]!="a") or (split_sentence[-2]!="the")):
                reply(wikipedia.summary(split_sentence[-2]+" "+split_sentence[-1],sentences=2))
                time1=speak(wikipedia.summary(split_sentence[-2]+" "+split_sentence[-1],sentences=2))
            else:
                reply(wikipedia.summary(split_sentence[-1],sentences=2))
                time1=speak(wikipedia.summary(split_sentence[-1],sentences=2))
            time.sleep(time1)
            
        elif(("create" in MyText) and  ("list" in MyText)):
            timesleep=speak(name,"iu")
            time.sleep(timesleep)
            split_sentence = MyText.split(' ')
            
            task[split_sentence[split_sentence.index("list")-1]]=[]
            nameoflist=split_sentence[split_sentence.index("list")-1]
            speak(reply("What Items Do You Want Me To Add?"))
            time.sleep(2)
            speak(reply("Please, Add One Item At a time!"),"p")
            time.sleep(4)
            
            while ("end" not in MyText):
                reply("Say Task")
                time.sleep(1)
                MyText = speech_recognizer.recognize_once_async().get()
                MyText=MyText.text[:-1].lower()
                replyUser(MyText)
                if("end" in MyText):
                    speak(reply("List Updated"))
                else:
                    task[nameoflist].append(MyText)
                    speak(reply("Next Item?"))
                    time.sleep(2)
        
        elif(("show" in MyText) and  ("list" in MyText)):
            speak(name,"iu")
            time.sleep(1)
            if(task=={}):
                speak(reply("You Currently Have No Items In The List"))
            else:
                found=False
                split_sentence = MyText.split(' ')
                for key in task.keys():
                    if(split_sentence[split_sentence.index("list")-1]==key):
                        found=True
                        speak(reply("In "+key.title()+" You Have"),"o")
                        time.sleep(2)
                        for keys in task[key]:
                            reply(" • "+keys.title())
                            wait=speak(keys,"oo")
                            time.sleep(wait)
                        break
                if(not found):
                    speak(reply("You Have "+str(len(task))+" Items In List"))
                    time.sleep(2)
                    for key in task:
                        speak(reply("In "+key.title()+" You Have"),"o")
                        time.sleep(2)
                        for keys in task[key]:
                            reply(" • "+keys.title())
                            wait=speak(keys,"oo")
                            time.sleep(wait)

        elif("weather" in MyText):
            speak(name,"iu")
            time.sleep(1)
            weather_main()

        elif("bye" in MyText):
            byeMessage = ["Bye, I'll Be Here If You Need Anything","GoodBye "+name,"Sayonara!"]
            speak(reply(byeMessage[random.randint(0,2)]))
        
        elif("search" in MyText):
            split_sentence = MyText.split(' ')
            url=""
            for i in split_sentence:
                if(i=="search"):
                    continue
                url+=i+"+"
            webbrowser.open("https://www.google.com/search?q={query}".format(query=url))
            reply("Right On It!")

        elif("night" in MyText or "nigh" in MyText):
            if(task):
                reply(str(len(task))+" Item Remaining In Task List")
                timewait=speak("But, "+name+" You Still Have Some Tasks Remaining To Complete")
                time.sleep(timewait)
                for key in task:
                        speak(reply("In "+key.title()+" You Have"),"o")
                        time.sleep(2)
                        for keys in task[key]:
                            reply(" • "+keys.title())
                            wait=speak(keys,"oo")
                            time.sleep(wait)
                timewait=speak("Be Sure To Complete Them","ui")
                time.sleep(timewait)
            nightWish=["Good Night!","Sleep Tight","Rest Now, "+name+" Bye!"]
            speak(reply(nightWish[random.randint(0,2)]))
            
        elif(("youtube" in MyText)):
            split_sentence = MyText.split(' ')
            url=""
            for i in split_sentence:
                if(i=="youtube"):
                    continue
                url+=i+"+"
            webbrowser.open("https://www.youtube.com/results?search_query={query}".format(query=url))
            reply("Right On It!")

        else:
            speak(reply("I Cannot Do That, Sorry!"))
            
    except BaseException as error:
        print(error)
        speak(reply("Can You Repeat That, Please?"))
        continue

