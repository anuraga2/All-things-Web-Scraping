## Importing all the relevant packages
import numpy as np
import pandas as pd
from selenium import webdriver
import time
import shutil,os
from bs4 import BeautifulSoup
from keyboard import press
import requests
import keyboard
import pyautogui

# Columns that are required from the Fangraphs Website
PitchersCol = ['IP', 'K/9', 'BB/9', 'HR/9', 'BABIP', 'ERA', 'FIP', 'WAR', 'WHIP']
BattersCol = ['PA', 'AB', 'HR', 'H', '2B', '3B', 'RBI', 'SB', 'ISO', 'BABIP', 'AVG', 'OBP', 'SLG', 'wOBA', 'wRC+', 'WAR', 'CS', 'BB%', 'K%']


## Reading the list of ids from the text file
pitchers_file = open("D:/UIUC/Era Adjustment/Fan Graph Individual Files/Metrics HTML Code.txt","r")

# storing the list of
PitchersDict = dict([(items[items.find(">")+1:items.find("</li")],idx-1) for idx, items in enumerate(pitchers_file.readlines()) if "li" in items])
pitchers_file.close()

## Reading the list of ids from the text file
batters_file = open("D:/UIUC/Era Adjustment/Fan Graph Individual Files/Batters Metrics HTML code.txt","r")

# storing the list of
BattersDict = dict([(items[items.find(">")+1:items.find("</li")],idx-1) for idx, items in enumerate(batters_file.readlines()) if "li" in items])
batters_file.close()


def ColumnListSelector(PlayerCategory):
    ColList =  PitchersCol if PlayerCategory == "Pitchers" else BattersCol
    return(ColList)

def ColString(ColList,PlayerCategory):
    ColStr = "c"
    for Cols in ColList:
        if PlayerCategory == "Batters":
            ColStr+=','+str(BattersDict[Cols]+2)
        elif PlayerCategory == "Pitchers":
            ColStr+=','+str(PitchersDict[Cols]+2)
        else:
            ColStr = "invalid player category"
    
    return(ColStr)

def FangraphScraper(Year, Var, PlayerCat, League,DownloadDirecotry,DumpDirectory):
    driver = webdriver.Chrome('chromedriver')
    url = "https://blogs.fangraphs.com/wp-login.php?redirect_to=https%3a%2f%2fwww.fangraphs.com%2findex.aspx"
    driver.get(url)
    time.sleep(3)
    username = driver.find_element_by_id("user_login")
    username.clear()
    username.send_keys("anurag2492")
    password = driver.find_element_by_id("user_pass")
    password.clear()
    password.send_keys("pSJ1zMH7xiHX")
    press('enter')
    time.sleep(2)
    ColList =  ColumnListSelector(PlayerCat)
    url2 = "https://www.fangraphs.com/leaders.aspx?pos=all&stats="+str(Var)+"&lg="+League+"&qual=y&type="+ColString(ColList,PlayerCat)+"&season="+str(Year)+"&month=0&season1="+str(Year)+"&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate=&enddate="
    driver.get(url2)
    driver.maximize_window()
    try:
        banner_ad = driver.find_element_by_class('membership-push-wide-app')
        if banner_ad:
            url2 = "https://www.fangraphs.com/leaders.aspx?pos=all&stats="+str(Var)+"&lg="+League+"&qual=y&type="+ColString(ColList,PlayerCat)+"&season="+str(Year)+"&month=0&season1="+str(Year)+"&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate=&enddate="
            driver.get(url2)
            driver.maximize_window()
            time.sleep(5)
            pyautogui.click(1878,960)
            driver.find_element_by_link_text('Export Data').click()
            time.sleep(5)
    except:
        time.sleep(5)
        pyautogui.click(1878,960)
        driver.find_element_by_link_text('Export Data').click()
        time.sleep(5)

    driver.quit()
    shutil.move(DownloadDirecotry+'FanGraphs Leaderboard.csv', 
                DumpDirectory+'FanGraphs_Leaderboard_'+str(Year)+'_'+Var+'_'+League+'.csv')
    print(str(Year)+'_'+Var+'_'+League)



DownloadDirecotry = 'C:/Users/anura/Downloads/'
DumpDirectory = 'D:/UIUC/Era Adjustment/Fan Graph Individual Files/'
Leagues = ['al','nl']
PlayerCat = [("Pitchers","pit"),("Batters","bat")]
Years = np.linspace(1880, 2019, 140, dtype=int)

for league in Leagues:
    for playercat in PlayerCat:
        for year in Years:
            FangraphScraper(year, playercat[1], playercat[0],league,DownloadDirecotry,DumpDirectory)


## Code to combine all the data files in one file
DownloadDirecotry = 'C:/Users/anura/Downloads/'
DumpDirectory = 'D:/UIUC/Era Adjustment/Fan Graph Individual Files/'
Leagues = ['al','nl']
PlayerCat = [("Pitchers","pit"),("Batters","bat")]
Years = np.linspace(1880, 2019, 140, dtype=int)
Leagues = ['al','nl']
PlayerCat = [("Pitchers","pit"),("Batters","bat")]
Years = np.linspace(1880, 2019, 140, dtype=int)

i = 0
for league in Leagues:
    for year in Years:
        if i == 0:
            df = pd.read_csv(DumpDirectory+'FanGraphs_Leaderboard_'+str(year)+'_'+PlayerCat[1][1]+'_'+league+'.csv')
            df['year'] = year
            df['playercategory'] = PlayerCat[1][1]
            df['league'] = league
            i = i+1
            print(DumpDirectory+'FanGraphs_Leaderboard_'+str(year)+'_'+PlayerCat[1][1]+'_'+league+'.csv')
            continue
        else:
            df1 = pd.read_csv(DumpDirectory+'FanGraphs_Leaderboard_'+str(year)+'_'+PlayerCat[1][1]+'_'+league+'.csv')
            df1['year'] = year
            df1['playercategory'] =PlayerCat[1][1]
            df1['league'] = league
            df = pd.concat([df,df1])
            print(DumpDirectory+'FanGraphs_Leaderboard_'+str(year)+'_'+PlayerCat[1][1]+'_'+league+'.csv')