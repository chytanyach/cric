import re
from selenium import webdriver
from requests import get
from selenium.webdriver.common.keys import Keys
from contextlib import closing
from utilities import *
from bs4 import BeautifulSoup
from constants import *
from PlayerClass import *
import xlwt 
from xlwt import Workbook


#file = open(r"E:/cricbuzz/players.txt","w+")

players=[]
final_squad = []
squad=[]
venue=''
venue_name=''
average_first_innings_score=0
average_second_innings_score=0

# to-do:
# 	Multiple Players with same first name and last name has to be handled
# 	opposition needs to be handled

my_func()
driver = webdriver.Chrome(executable_path=web_drive_executable_path)

def venue_details_func(html):
	elements=html.findAll('div', attrs={'class':'cb-col cb-col-100 cb-col-rt'})
	details=elements[1].findAll('div', attrs={'class':'cb-col cb-col-73 cb-mat-fct-itm'})
	venue_details=elements[2].findAll('div', attrs={'class':'cb-col cb-col-73 cb-mat-fct-itm'})
	
	venue_name=details[0].text
	average_first_innings_score=int(venue_details[0].text)
	average_second_innings_score=int(venue_details[1].text)




if __name__ == "__main__":

	print("Started")
	raw_html = simple_get(playing_squad_url)
	html = BeautifulSoup(raw_html, 'html.parser')

	#opposition hardcoded for now
	opposition="England"

	players=find_players(html)
	squad = find_final_squad(players)
	final_squad =list(map(trim_func,squad))

	#print("final squad is ",final_squad)

	final_squad_objects = map(Player,final_squad)


	elements=html.findAll('div', attrs={'class':'cb-col cb-col-100 cb-col-rt'})
	details=elements[1].findAll('div', attrs={'class':'cb-col cb-col-73 cb-mat-fct-itm'})
	venue_details=elements[2].findAll('div', attrs={'class':'cb-col cb-col-73 cb-mat-fct-itm'})
	
	venue_name=details[0].text
	average_first_innings_score=int(venue_details[0].text)
	average_second_innings_score=int(venue_details[1].text)


	write_squad_stats(final_squad_objects)

	with open (output_venue_path,'w+') as r:
		temp=f'venue is {venue_name}\n'
		r.write(temp)
		temp=f'average first Innings score is {average_first_innings_score}\n'
		r.write(temp)
		temp=f'average second Innings score is {average_second_innings_score}'
		r.write(temp)

	print('completed')
