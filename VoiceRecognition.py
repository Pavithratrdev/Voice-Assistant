import requests 
from bs4 import BeautifulSoup 
import re
import speech_recognition as sr 
from datetime import date
import webbrowser
import pyttsx3

def scrape_weather(city):
    url = 'https://www.google.com/search?q=accuweather+' + city
    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'lxml')

    links = [a['href']for a in soup.findAll('a')]
    link = str(links[16])
    link = link.split('=')
    link = str(link[1]).split('&')
    link = link[0]
    
    page = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})

    soup = BeautifulSoup(page.content, 'lxml') 
    
    time = soup.find('p', attrs = {'class': 'cur-con-weather-card__subtitle'})
    time = re.sub('\n', '', time.text)
    time = re.sub('\t', '', time)
    time = 'Time: ' + time

    temperature = soup.find('div', attrs = {'class':'temp'})
    temperature = 'Temperature: ' + temperature.text
    
    realfeel = soup.find('div', attrs = {'class': 'real-feel'})
    realfeel = re.sub('\n', '',realfeel.text)
    realfeel = re.sub('\t', '',realfeel)
    realfeel = 'RealFeel: ' + realfeel[-3:] + 'C'

    climate = soup.find('span', attrs = {'class':'phrase'})
    climate = "Climate: " + climate.text
    
    info = 'For more information visit: ' + link 
    
    print('The weather for today is: ')
    print(time)
    print(temperature)
    print(realfeel)
    print(climate)
    print(info)
    engine.say('The weather for today is: ')
    engine.say(time)
    engine.say(temperature)
    engine.say(realfeel)
    engine.say(climate)
    engine.say('For more information visit accuweather.com' )
    engine.runAndWait()
    
def scrape_meaning(audio):
    word = audio
    url = 'https://www.dictionary.com/browse/' + word
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    soup
    meanings = soup.findAll('div', attrs =  {'class': 'css-1o58fj8 e1hk9ate4'})
    meaning = [x.text for x in meanings]
    first_meaning = meaning[0]
    for x in meaning:
        print(x)
        print('\n')
    engine.say(first_meaning)
    engine.runAndWait()
    
def take_notes():
     r5 = sr.Recognizer()  
     with sr.Microphone() as source:
        print('What is your "TO DO LIST" for today')
        engine.say('What is your "TO DO LIST" for today')
        engine.runAndWait()
        audio = r5.listen(source)
        audio = r5.recognize_google(audio)
        print(audio)
        today = date.today()
        today = str(today)
        with open('MyNotes.txt','a') as f:
            f.write('\n')
            f.write(today)
            f.write('\n')
            f.write(audio)
            f.write('\n')
            f.write('......')
            f.write('\n')
            f.close() 
        engine.say('Notes Taken')
        engine.runAndWait()


def scrape_news():
    url = 'https://news.google.com/topstories?hl=en-IN&gl=IN&ceid=IN:en '
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    news = soup.findAll('h3', attrs = {'class':'ipQwMb ekueJc RD0gLb'})
    for n in news:
        print(n.text)
        print('\n')
        engine.say(n.text)
    print('For more information visit: ', url)
    engine.say('For more information visit google news')
    engine.runAndWait()

def play_youtube(audio):

    url = 'https://www.google.com/search?q=youtube+' + audio
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    engine.say('Playing')
    engine.say(audio)
    engine.runAndWait()
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    link = soup.findAll('div', attrs = {'class':'r'})
    link = link[0]
    link = link.find('a')
    link = str(link)
    link = link.split('"')
    link = link[1]

    webbrowser.open(link)

    
engine = pyttsx3.init('sapi5')

r1 = sr.Recognizer()
with sr.Microphone() as source:
    print('Listening..')
    engine.say('Listening')
    engine.runAndWait()
    audio = r1.listen(source)
    audio = r1.recognize_google(audio)

    if 'weather' in audio:
        print('..')
        words = audio.split(' ')
        print(words[-1])
        scrape_weather(words[-1])

    elif 'meaning' in audio:
        print('..')
        words = audio.split(' ')
        print(words[-1])
        scrape_meaning(words[-1])
        
    elif 'take notes' in audio:
        print('..')
        take_notes()
        print('Noted!!')
              
    elif 'news' in audio:
        print('..')
        scrape_news()
        
    elif 'play' in audio:
        print('..')
        words = audio.split(' ')
        print(words[-1])
        play_youtube(audio)
        
    elif 'open' in audio:
        print('..')
        words = audio.split('open')
        print(words[-1])
        link = str(words[-1])
        link = re.sub(' ', '', link)
        engine.say('Opening')
        engine.say(link)
        engine.runAndWait()
        link = f'https://{link}.com'
        print(link)
        webbrowser.open(link)
        
    elif 'where is' in audio:
        print('..')
        words = audio.split('where is')
        print(words[-1])
        link = str(words[-1])
        link = re.sub(' ', '', link)
        engine.say('Locating')
        engine.say(link)
        engine.runAndWait()
        link = f'https://www.google.co.in/maps/place/{link}'
        print(link)
        webbrowser.open(link)
        
            
    else:
        print(audio)
        print('Sorry, I do not understand that!')
        engine.say('Sorry, I do not understand that!')
        engine.runAndWait()