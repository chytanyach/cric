import re
from bs4 import BeautifulSoup
from selenium import webdriver
from requests import get
from selenium.webdriver.common.keys import Keys
from contextlib import closing
from constants import *
import pandas as pd



def my_func():
    print("in utilities")

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                #print (resp.content)
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


def trim_func(player):
    return (re.sub(r"(.*?)\s?\(.*?\)", r"\1", player)).strip()


def find_players(html):
    players=[]
    for a in html.findAll('div', attrs={'class':'cb-col cb-col-100'}):
        if(a.find('a', attrs={'class':'text-hvr-underline'})):
            if("Playing XI" in a.text):
                players.append(a.text)
    return players


def find_final_squad(players):
    squad1=[]
    squad2=[]
    final_squad = []
    for x in players:
        a = x.split(":")[1]
        if (len(squad1) == 0):
            squad1=a.split(",")
        else:
            squad2=a.split(",")
    final_squad = squad1 + squad2
    return final_squad


def find_first_letters(name):
    temp=[]
    for x in name.split(" "):
        temp.append(x[0])
    return temp


def find_words(name):
    return name.split(" ")


def find_func1(words,html1):
    player_name=f'{words[1]}, {words[0][0]}'
    id=''
    for a in html1.findAll('a', attrs={'LinkNormal'}):
        if(player_name in a.text):
            id=a['href'].split("=")[1]
            break
        
    return id
            


def find_func2(words,html1):
    player_name=f'{words[1]},  {words[0][0]}'
    id=''
    for a in html1.findAll('a', attrs={'LinkNormal'}):
        words1=(a.text).split(" ")
        if( len(words1) == 3):
            name=(f'{words1[0]} {words1[1]}* {words1[2]}')
            regexPattern = re.compile(name)
            if(regexPattern.fullmatch(player_name)):
                id=a['href'].split("=")[1]
                break
    return id

def find_func3(words):
    raw_html1=simple_get(f'{player_stats_url}{words[0][0]}')
    html1 = BeautifulSoup(raw_html1, 'html.parser')
    id=''

    player_name=f'{words[0]} {words[1]}'
    for a in html1.findAll('a', attrs={'LinkNormal'}):
        if(player_name in a.text):
            id=a['href'].split("=")[1]
            break  
    return id


def find_player_from_file(name):
    pid=''
    data = pd.read_csv('E:/cricbuzz/files/players.txt', sep=",", header=None)
    data.columns = ["player_name","id"]
    pid=data[data.player_name == name].id
    if(len(pid) == 0):
            words=find_words(name)
            pid=find_player_id(words)
            file= open("E:/cricbuzz/files/players.txt","a+")
            line=f'{name},{pid}\n'
            file.write(f'{line}')
            file.close()
    return pid

#create a function to find the player id
def find_player_id(words):
    #for x in words:


    raw_html1=simple_get(f'{player_stats_url}{words[1]}')
    html1 = BeautifulSoup(raw_html1, 'html.parser')
    id=''

    id=find_func1(words,html1)
    if(len(id) ==  0):
        id=find_func2(words,html1)
        if(len(id) ==  0):
            id=find_func3(words)

    return id
    
