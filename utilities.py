import re
from bs4 import BeautifulSoup
from selenium import webdriver
from requests import get
from selenium.webdriver.common.keys import Keys
from contextlib import closing
from constants import *
from datetime import datetime
#from MainModule import *
import pandas as pd
import unicodedata
import os



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



def get_cricbuzz_dob(name):
    raw_html5=simple_get(playing_squad_url)
    html5 = BeautifulSoup(raw_html5, 'html.parser')
    profile_id_url=''

    line=html5.findAll('a', attrs={'class':'text-hvr-underline'})
    for x in line:
        if (name in x.text):
            profile_id_url=x['href']
            break

    profile_cricbuzz_url=f'{cricbuzz_url}{profile_id_url}'

    raw_html6=simple_get(profile_cricbuzz_url)
    html6 = BeautifulSoup(raw_html6, 'html.parser')

    line=html6.findAll('div', attrs={'class':'cb-col cb-col-60 cb-lst-itm-sm'})
    dob_cricbuzz=line[0].text.strip()
    dob_cricbuzz=dob_cricbuzz[:12]
    return dob_cricbuzz



def compare_dob_func(html,name):
    line=html.findAll('table', attrs={'border':'0', 'width':'100%', 'cellpadding':'2', 'cellspacing':'0'})

    rows=line[0].findAll('td')
    dob_howstat=rows[6].text.strip()
    dob_cricbuzz=get_cricbuzz_dob(name)

    date_cricbuzz = datetime.strptime(dob_cricbuzz, '%b %d, %Y')
    date_howstat = datetime.strptime(dob_howstat, '%d/%m/%Y')

    
    if(date_cricbuzz == date_howstat):
        return True
    else:
        return False



def find_correct_id(ids,words,name):
    for x in ids:
        temp_url=f'{player_overview_url}{x}'
        raw_html4=simple_get(temp_url)
        html4 = BeautifulSoup(raw_html4, 'html.parser')
        line=html4.findAll('td', attrs={'TextGreenBold12'})
        unicode_str = unicodedata.normalize("NFKD",line[0].text.strip())
        temp=unicode_str.replace('\t', ' ')
        temp=unicode_str.replace('\n', ' ')

        dob_match=compare_dob_func(html4,name)

        

        plyr_name=temp.split(" ")
        if(words[0] == plyr_name[0] or dob_match):
            return x
            break


def find_func1(words,html1,name):
    player_name=f'{words[1]}, {words[0][0]}'
    ids=[]
    for a in html1.findAll('a', attrs={'LinkNormal'}):
        if(player_name in a.text):
            ids.append(a['href'].split("=")[1])
    
    if(len(ids)==1):
        return str(ids[0])
    elif(len(ids) > 1):
        id=find_correct_id(ids,words,name)
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
    for a in html1.findAll('a', attrs={'LinkNormal'}):
        if(player_name in a.text):
            id=a['href'].split("=")[1]
            return str(id)
            break


def find_player_from_file(name):

    exists = os.path.isfile(players_id_file)
    data={}
    if exists:
        # Store configuration file values
        data = pd.read_csv(players_id_file, sep=",", header='infer')
        data.columns = ["player_name","id"]
    else:
        # Keep presets
        line=f'Player,Id\n'
        with open (players_id_file,'w+') as r:
            r.write(line)


    pid=''
    pidDF=data.loc[data.player_name == name]
        
    if(len(pidDF) > 0):
        pid=pidDF["id"].values[0]

    if(len(str(pid)) == 0):
            words=find_words(name)
            pid=find_player_id(words,name)
            file= open(players_id_file,"a+")
            file.write('\n')
            line=f'{name},{pid}\n'
            file.write(f'{line}')
            file.close()
    return pid

#create a function to find the player id
def find_player_id(words,name):
    #for x in words:
    raw_html1=simple_get(f'{player_name_url}{words[1]}')
    html1 = BeautifulSoup(raw_html1, 'html.parser')
    id=''

    id=find_func1(words,html1,name)
    if(id is None):
        id=find_func2(words,html1)
        if(id is None):
            id=find_func3(words)

    return str(id)
    
def get_player_batting_stats(name,id):
    player_url=f'{player_stats_url}{id}'
    print(player_url)
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

def avg_versus_opp_func(player_data,id,team1,team2):
    opposition=''
    team_name=get_team_name(id)
    if(team_name.lower() == team1.lower()):
        opposition=team2
    else:
        opposition=team1
    print("opposition is ",opposition)
    player_ver_opp_df=player_data.loc[player_data['Versus'] == opposition]
    player_ver_opp=player_ver_opp_df['Runs'].tail(n=5).mean()
    if (player_ver_opp != 0):
        return player_ver_opp
    else:
        return 0

def avg_in_ground_func(player_data,venue):
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
            row=f'{x.name};{x.id};{x.id_name};{x.total_average};{x.latest_average};{x.avg_versus_opp};{x.avg_in_ground};{x.final_batting_score}\n'
            r.write(row)

def get_teams():
    raw_html5=simple_get(playing_squad_url)
    html5 = BeautifulSoup(raw_html5, 'html.parser')
    name=html5.findAll('h1', attrs={'cb-nav-hdr cb-font-18 line-ht24'})
    words=name[0].text.split(" ")
    return words

def player_team(id):
    temp_url=f'{player_overview_url}{id}'
    raw_html4=simple_get(temp_url)
    html4 = BeautifulSoup(raw_html4, 'html.parser')
    line=html4.findAll('td', attrs={'TextGreenBold12'})


def get_team_name(id):
    # teams=get_teams()
    # team1=teams[0]
    # team2=teams[2].split(",")[0]
    team_url=f'{team_name_url}{id}'
    raw_html4=simple_get(team_url)
    html4 = BeautifulSoup(raw_html4, 'html.parser')
    line=html4.findAll('td', attrs={'TextGreenBold12'})
    name=line[0].text.strip()
    new_str = unicodedata.normalize("NFKD", name)
    temp=new_str.replace('\t', ' ')
    temp=new_str.replace('\n', ' ')
    line=temp.split(" ")
    team_name=line[len(line)-1]
    team_name=team_name[1:-1]
    return team_name
    # if(team_name.lower() == team1.lower()):
    #     return team2
    # else:
    #     return team1    

def get_final_batting_score(total_average,latest_average,avg_versus_opp,avg_in_ground):
    final_average=0
    if(total_average !=0 and latest_average != 0 and avg_versus_opp!= 0 and avg_in_ground!= 0):
        final_average =  ((total_average*2)+(latest_average*3)+(avg_versus_opp*2)+(avg_in_ground))/4    
    elif(total_average !=0 and latest_average != 0 and avg_versus_opp!= 0 and avg_in_ground == 0):
        final_average =  ((total_average*2)+(latest_average*3)+(avg_versus_opp))/3
    elif(total_average !=0 and latest_average != 0 and avg_versus_opp == 0 and avg_in_ground != 0):
        final_average =  ((total_average*2)+(latest_average*3)+(avg_in_ground))/3
    elif(total_average !=0 and latest_average != 0 and avg_versus_opp == 0 and avg_in_ground == 0):
        final_average =  ((total_average)+(latest_average*2))/2

    return final_average
    

# def get_batting_xi(final_squad_objects):
#     player_name=[]
#     batting_score=[]
#     for x in final_squad_objects:
#         batting_score.append[x.final_batting_score]
#         player_name.append[x.name]
#     return





