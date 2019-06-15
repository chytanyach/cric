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
#def my_func():
#    print("in utilities")

my_func()
driver = webdriver.Chrome(executable_path=web_drive_executable_path)


if __name__ == "__main__":

	raw_html = simple_get(playing_squad_url)
	html = BeautifulSoup(raw_html, 'html.parser')
	players=find_players(html)
	squad = find_final_squad(players)
	final_squad =list(map(trim_func,squad))

	#print("final squad is ",final_squad)

	final_squad_objects = map(Player,final_squad)

	print("players and ids are")
	for x in final_squad_objects:		
		print(f"name is {x.name} and his id is {x.id}")
