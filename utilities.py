import re
from bs4 import BeautifulSoup
from selenium import webdriver
from requests import get
from selenium.webdriver.common.keys import Keys
from contextlib import closing
from constants import *
#from MainModule import *
import pandas as pd
import unicodedata



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


def find_correct_id(ids,words):
    for x in ids:
        temp_url=f'{player_overview_url}{x}'
        raw_html4=simple_get(temp_url)
        html4 = BeautifulSoup(raw_html4, 'html.parser')
        name=html4.findAll('td', attrs={'TextGreenBold12'})
        unicode_str = unicodedata.normalize("NFKD",name[0].text.strip())
        temp=unicode_str.replace('\t', ' ')
        temp=unicode_str.replace('\n', ' ')
        plyr_name=temp.split(" ")
        if(words[0] == plyr_name[0]):
            return x
            break


def find_func1(words,html1):
    player_name=f'{words[1]}, {words[0][0]}'
    ids=[]
    for a in html1.findAll('a', attrs={'LinkNormal'}):
        if(player_name in a.text):
            ids.append(a['href'].split("=")[1])
    
    if(len(ids)==1):
        return str(ids[0])
    elif(len(ids) > 1):
        id=find_correct_id(ids,words)
        return str(id)
            


def find_func2(words,html1):
    player_name=f'{words[1]},  {words[0][0]}'
    #id=''
    for a in html1.findAll('a', attrs={'LinkNormal'}):
        words1=(a.text).split(" ")
        if( len(words1) == 3):
            name=(f'{words1[0]} {words1[1]}* {words1[2]}')
            regexPattern = re.compile(name)
            if(regexPattern.fullmatch(player_name)):
                id=a['href'].split("=")[1]
                return str(id)
                break
    

def find_func3(words):
    url=f'{player_name_url}{words[0][0]}'
    raw_html1=simple_get(url)
    html1=BeautifulSoup(raw_html1,'html.parser')
    id=''

    player_name=f'{words[0]} {words[1]}'
    print('player name in func3 is',player_name)
    for a in html1.findAll('a', attrs={'LinkNormal'}):
        if(player_name in a.text):
            id=a['href'].split("=")[1]
            print('id is',id)
            return str(id)
            break


def find_player_from_file(name):
    pid=''
    data = pd.read_csv('E:/cricbuzz/files/players.txt', sep=",", header=None)
    data.columns = ["player_name","id"]
    pidDF=data.loc[data.player_name == name]
        
    if(len(pidDF) > 0):
        pid=pidDF["id"].values[0]

    if(len(str(pid)) == 0):
            words=find_words(name)
            pid=find_player_id(words)
            file= open("E:/cricbuzz/files/players.txt","a+")
            file.write('\n')
            line=f'{name},{pid}\n'
            file.write(f'{line}')
            file.close()
    return pid

#create a function to find the player id
def find_player_id(words):
    #for x in words:
    raw_html1=simple_get(f'{player_name_url}{words[1]}')
    html1 = BeautifulSoup(raw_html1, 'html.parser')
    id=''

    id=find_func1(words,html1)
    if(id is None):
        id=find_func2(words,html1)
        if(id is None):
            id=find_func3(words)

    return str(id)
    
def get_player_stats(name,id):
    player_url=f'{player_stats_url}{id}'
    player_stats_path=f'{stats_path}{name}.txt'
    raw_html2=simple_get(player_url)
    html2 = BeautifulSoup(raw_html2, 'html.parser')
    table = html2.find_all('table',attrs={'class':'TableLined'})
    tab=table[0]
    with open (player_stats_path,'w+') as r:
        for row in tab.find_all('tr'):
            for y in row.find_all('td'):
                if not (("Progressive" in y.text) or ("Innings" in y.text) or ("nbsp" in y.text)):
                    line=f'{y.text.strip()};'
                    r.write(line)
            r.write('\n')

def remove_ast(runs):
    num = re.sub(r'\D', " ", str(runs))
    return int(num)

def read_player_stats(name):
    # words=name.split(" ")
    player_data=''
    player_stats_path=f'{stats_path}{name}.txt'
    player_data = pd.read_csv(player_stats_path, sep=";", header='infer',skiprows=2, skipfooter=1,engine='python',dtype=str)
    player_data.columns = ["Match_Number","Date","Versus","Ground","Dismissed","Runs","Balls_Faced","Strike_Rate","Extra1","Runs_Cumulative","Average","Strike_Rate","Extra2"]
    player_data.Runs=player_data.Runs.replace(to_replace="-", value=0, inplace=False, limit=None, regex=False, method='pad')
    player_data['Runs'] = player_data['Runs'].apply(lambda x: remove_ast(x))

    return player_data

def total_average_func(player_data):
    averageDF=player_data.tail(n=1)
    average=averageDF['Average'].values[0]
    return average
    # if (average != 0):
    #     return average
    # else:
    #     return 0

def latest_average_func(player_data):
    latest_average=player_data["Runs"].tail(n=5).mean()
    return latest_average
    # if (latest_average != 0):
    #     return latest_average
    # else:
    #     return 0

def avg_versus_opp_func(player_data):
    opposition="England"
    player_ver_opp_df=player_data.loc[player_data['Versus'] == opposition]
    player_ver_opp=player_ver_opp_df['Runs'].tail(n=5).mean()
    if (player_ver_opp != 0):
        return player_ver_opp
    else:
        return 0

def avg_in_ground_func(player_data):
    venue="Kennington Oval"
    player_in_ground_df=player_data.loc[player_data['Ground']== venue]
    player_in_ground=player_in_ground_df['Runs'].mean()
    if (player_in_ground != 0):
        return player_in_ground
    else:
        return 0
 

def find_id_name(id):
    temp_url=f'{player_overview_url}{id}'
    raw_html4=simple_get(temp_url)
    html4 = BeautifulSoup(raw_html4, 'html.parser')
    name=html4.findAll('td', attrs={'TextGreenBold12'})

    unicode_str = unicodedata.normalize("NFKD",name[0].text.strip())
    temp=unicode_str.replace('\t', ' ')
    temp=unicode_str.replace('\n', ' ')
    temp=temp.strip()
    return temp



def write_squad_stats(final_squad_objects):
    with open (output_stats_path,'w+') as r:
        for x in final_squad_objects:
            row=f'{x.name};{x.id};{x.id_name};{x.total_average};{x.latest_average};{x.avg_versus_opp};{x.avg_in_ground}\n'
            r.write(row)
    