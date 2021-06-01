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
import glob
import re



## Creating a list of integers from 1871 to 2019
years = np.linspace(1871,2019,149,dtype=int)

## Looping over all the years
for year in years:
    
    ## Initialising the chrome driver
    driver = webdriver.Chrome('chromedriver')
    
    ## Fetching the first url in the driver window
    url = "https://stathead.com/baseball/season_finder.cgi?request=1&sum=0&order_by_asc=0&order_by=WAR_bat&qualifiersSeason=nomin&minpasValS=502&mingamesValS=100&qualifiersCareer=nomin&minpasValC=3000&mingamesValC=1000&min_year_season="+str(year)+"&max_year_season="+str(year)+"&lg_ID=lgAny&lgAL_team=tmAny&lgNL_team=tmAny&lgFL_team=tmAny&lgAA_team=tmAny&lgPL_team=tmAny&lgUA_team=tmAny&lgNA_team=tmAny&exactness=anypos&pos_1=1&pos_2=1&pos_3=1&pos_4=1&pos_5=1&pos_6=1&pos_7=1&pos_8=1&pos_9=1&pos_10=1&pos_11=1&as=result_batter&offset=0&type=b&bats=any&throws=any&min_age=0&max_age=99&min_season=1&max_season=-1&location=pob&locationMatch=is&isHOF=either&isAllstar=either&isActive=either"
    driver.get(url)
    
    ## Giving a sleep time of 3 seconds so that the page loads completely
    time.sleep(3)
    
    ## Find the login link and click it
    driver.find_element_by_link_text('Already a subscriber? Log in for full results.').click()
    
    ## Find the username field, clearing it, and entering the username
    username = driver.find_element_by_id("username")
    username.clear()
    username.send_keys("<username>")
    
    ## Find the password field, clearing it, and entering the username
    password = driver.find_element_by_name("password")
    password.clear()
    password.send_keys("<password>")
    
    ## Pressing enter to login
    press('enter')
    
    ## After the login extracting the text at the bottom of the data table to find out the number of records for 
    ## this particular year
    num_records_raw_txt = driver.find_element_by_xpath("//div[@id='tfooter_ajax_result_table']//small").text
    
    ## Extracting the number of records text
    num_records = num_records_raw_txt[num_records_raw_txt.index(':')+2:]
    
    ## The text can contain values like 993 or 1,183
    ## The condition below checks for that condition and extracts the number of records
    if len(num_records) > 3:
        num_records_new = int(''.join(num_records.split(',')))
    else:
        num_records_new = int(num_records)
    
    ## Writing a condition on the number of records
    ## If the number of records is less than 300, then the number of pages containing data in each year in just one
    ## So we just have to save the first page of data
    
    if num_records_new <= 300:
        
        ## Sleep for 5 seconds
        time.sleep(5)
        
        ## Press ctrl+s
        keyboard.press_and_release('ctrl+s')
        
        ## Sleep for 5 seconds
        time.sleep(5)
        
        ## Enter the name of the file
        pyautogui.write(list(str(year)))
        time.sleep(5)
        
        ## Save the file
        pyautogui.press('enter')
        time.sleep(5)
        
        ## Move the file to the appropriate directory using shutil module
        shutil.move('C:/Users/anura/Downloads/'+str(year)+'.html', 
            'D:/UIUC/Era Adjustment/Sat Head Webpages/'+str(year)+'.html')

        shutil.move('C:/Users/anura/Downloads/'+str(year)+'_files', 
                'D:/UIUC/Era Adjustment/Sat Head Webpages/'+str(year)+'_files')

        print(year)
    
    ## If the number of records is more than 300 then we have change the offset parameter in the url
    else:
        ## Creating an index on which the inner loop will run
        for i in range(int(num_records_new/300)+1):
            
            ## Sleep for 5 seconds
            time.sleep(5)
            
            ## Press control + s to trigger the save window
            keyboard.press_and_release('ctrl+s')
            time.sleep(5)
            
            ## Indexing each page for the years for which we have multiple pages of data
            pyautogui.write(list(str(year))+['_']+[str((i+1))])
            time.sleep(5)
            pyautogui.press('enter')
            if i == (int(num_records_new/300)+1):
                break
            else:
                url = "https://stathead.com/baseball/season_finder.cgi?request=1&sum=0&order_by_asc=0&order_by=WAR_bat&qualifiersSeason=nomin&minpasValS=502&mingamesValS=100&qualifiersCareer=nomin&minpasValC=3000&mingamesValC=1000&min_year_season="+str(year)+"&max_year_season="+str(year)+"&lg_ID=lgAny&lgAL_team=tmAny&lgNL_team=tmAny&lgFL_team=tmAny&lgAA_team=tmAny&lgPL_team=tmAny&lgUA_team=tmAny&lgNA_team=tmAny&exactness=anypos&pos_1=1&pos_2=1&pos_3=1&pos_4=1&pos_5=1&pos_6=1&pos_7=1&pos_8=1&pos_9=1&pos_10=1&pos_11=1&as=result_batter&offset="+str(300*(i+1))+"&type=b&bats=any&throws=any&min_age=0&max_age=99&min_season=1&max_season=-1&location=pob&locationMatch=is&isHOF=either&isAllstar=either&isActive=either"
                driver.get(url)
                
                ## Printing the year and file number so that we can monitor the log, which will help us point 
                ## to the specific time till which the data has run
                print(str(year)+'_'+str(i+1))
            
            ## Move the extracted web pages
            shutil.move('C:/Users/anura/Downloads/'+str(year)+'_'+str((i+1))+'.html', 
            'D:/UIUC/Era Adjustment/Sat Head Webpages/'+str(year)+'_'+str((i+1))+'.html')

            shutil.move('C:/Users/anura/Downloads/'+str(year)+'_'+str((i+1))+'_files', 
            'D:/UIUC/Era Adjustment/Sat Head Webpages/'+str(year)+'_'+str((i+1))+'_files')

    driver.quit()
    
 
 
 def FileComb(player_cat,read_location, write_location):

    ## Storing the location of the file where the webpages have been stored
    location = read_location

    ## Declaring an empty list where we will store the names of the file
    file_lst = []

    ## Walking through the directory
    for r, d, f in os.walk(location):
        for item in f:

            ## If the file name begins with either 1/2 then store that file name in the list
            if '.html' in item and ((item[:1] == '1') or (item[:1] == '2')):
                file_lst.append(item)

    ## Creating an index variable and an empty dictionary where we would be storing all the data
    i = 0
    dict = {}
    PlayerLinkDict = {}

    ## Taking the first file to extract the header from it
    page_loc = location + '/' + file_lst[0]

    ## Extracting the soup from the target webpage
    soup = BeautifulSoup(open(page_loc,'rb'), "html.parser")

    ## Finding the table within the soup using the table id
    table = soup.find(id='ajax_result_table')

    ## Declaring an empty list where we would be storing the column name
    col_lst = []

    ## Extracting the header text and storing it into a list
    for header in table.find('thead').find('tr').find_all('th'):
        col_lst.append(header.text)


    ## Iterating over the list of files
    for file in file_lst:

        ## writing the main code within the try block, becuase I encountered an error during runtime owing to the 
        ## encoding of the data type 
        try:
            ## Reading the paage
            page_loc = location + '/' + file

            ## Extracting the soup
            soup = BeautifulSoup(open(page_loc, 'rb'), "html.parser")

            ## Extracting the table 
            table = soup.find(id='ajax_result_table')

            ## Printing the file name
            print(file)

            ## Iterating over all the table rows
            for data in table.find('tbody').find_all('tr'):
                i = i+1
                j = 0
                val_lst = []
                for rd in data.find_all('td'):
                    j= j+1
                    val_lst.append(rd.text)
                    if j == 1 and rd.find('a'):
                        PlayerLinkDict[rd.text] = str(rd.find("a").attrs['href'])
                dict[i] = val_lst
        except:
            pass


    ## Converting the dictionary to a data frame
    df = pd.DataFrame.from_dict(dict,orient='index',columns=col_lst[1:])

    ## Writing the file to a csv
    df.to_csv(write_location+str('/')+str(player_cat)+str('.csv'))
    print(df.shape)
    return df,PlayerLinkDict
 
 #combining data from webpages (Batters)
 read_location = 'D:/UIUC/Era Adjustment/Sat Head Webpages Batters'
write_location = 'D:/UIUC/Era Adjustment/Scripts'
df_Batters, player_link_batters = FileComb("Batters",read_location,write_location)

#combining data from webpages (Pitchers)
read_location = 'D:/UIUC/Era Adjustment/Sat Head Webpages Pitchers'
write_location = 'D:/UIUC/Era Adjustment/Scripts'
df_Pitchers, player_link_pitchers = FileComb("Pitchers",read_location,write_location)

## Merging the player dictionaries
# Python code to merge dict using a single 
# expression
def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

merged_player_dict = Merge(player_link_batters, player_link_pitchers)

# Code chunk below is to deal with tranfer players (Players who changed leagues within a particular year)

## Function to extract the name and year of the player in which they played for multiple leagues

def MultiLeaguePlayers(df):
    
    ## Removing null entries in the data set
    df_clean = df.loc[-df['Player'].isnull(),]
    
    ## Seperating out multiple appearance from single appearance
    ml_league = df.loc[(df['Lg'] == 'ML'),]
    sl_league = df.loc[-(df['Lg'] == 'ML'),]
    
    ## Rolling up the multiple league data set to get single entries at a player year level
    player_year = ml_league.loc[:,["Player","Year"]].groupby(["Player","Year"]).size().reset_index(name = "Freq")
    
    ## We return two data sets one is the single appearance in a year and the other one is multiple appearance in a year
    return sl_league, player_year
    
 
 ## Extracting out the single league players and the player names that appeared in multiple leagues in a year
single_league_batters, batters_player_year = MultiLeaguePlayers(df_Batters)
single_league_pitchers, pitchers_player_year = MultiLeaguePlayers(df_Pitchers)

## Merging the player names that came in multiple leagues in a year
player_year_merged = pd.concat([batters_player_year,pitchers_player_year])
transfer_players = list(set(player_year_merged.loc[:,["Player","Year"]].groupby(["Player","Year"]).size().reset_index(name = "Freq")['Player']))

# Function below saves the player info

def SavePlayerInfo(LocalDirectory,url,PlayerName):
    driver = webdriver.Chrome('chromedriver')
    driver.get(merged_player_dict[PlayerName])
    driver.maximize_window()
    driver.find_element_by_link_text('Login').click()
    username = driver.find_element_by_id("username")
    username.clear()
    username.send_keys("<User Name>")
    password = driver.find_element_by_name("password")
    password.clear()
    password.send_keys("<Password>")
    pyautogui.press('enter')
    time.sleep(5)
    keyboard.press_and_release('ctrl+s')
    time.sleep(2)
    pyautogui.write(list(PlayerName))
    time.sleep(2)
    pyautogui.press('enter')
    time.sleep(5)
    driver.quit()
    
    ## Moving the file to appropriate directory using the shutil mode
    shutil.move('C:/Users/anura/Downloads/'+PlayerName+'.html', 
                LocalDirectory+PlayerName+'.html')
    
    shutil.move('C:/Users/anura/Downloads/'+PlayerName+'_files', 
                LocalDirectory+PlayerName+'_files')
 
 
 ## Data to download the players appearing in multiple leagus in a year
pointer = 0
LocalDirectory = "D:/UIUC/Era Adjustment/Transfer Players/"
os.chdir("D:/UIUC/Era Adjustment/Scripts/")
for player in rem_player:
#     url = merged_player_dict[player]
#     SavePlayerInfo(LocalDirectory,url,player)
    pointer = pointer+1
    print(pointer)
    if pointer == len(rem_player):
        driver.quit()
    elif pointer  == 1:
        driver = webdriver.Chrome('chromedriver')
        driver.get(merged_player_dict[player])
        driver.maximize_window()
        driver.find_element_by_link_text('Login').click()
        username = driver.find_element_by_id("username")
        username.clear()
        username.send_keys("<Enter your Username>")
        password = driver.find_element_by_name("password")
        password.clear()
        password.send_keys("<Enter Your Password>")
        pyautogui.press('enter')
        time.sleep(10)
        keyboard.press_and_release('ctrl+s')
        time.sleep(2)
        pyautogui.write(list(player))
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(3)
        shutil.move('C:/Users/anura/Downloads/'+player+'.html', 
                LocalDirectory+player+'.html')
        shutil.move('C:/Users/anura/Downloads/'+player+'_files', 
                LocalDirectory+player+'_files')
    else:
        driver.get(merged_player_dict[player])
        time.sleep(3)
        keyboard.press_and_release('ctrl+s')
        time.sleep(2)
        pyautogui.write(list(player))
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(3)
        shutil.move('C:/Users/anura/Downloads/'+player+'.html', 
                LocalDirectory+player+'.html')
        shutil.move('C:/Users/anura/Downloads/'+player+'_files', 
                LocalDirectory+player+'_files')
                
 
 # Helper functions for data extractions
 
 def TableHeader(TableName):
    
    """
    This function returns the column of the tables depending upon which table is being call
    i.e. standard pitching, pitching value, standard batting, batting value
    
    """
    col_lst = ['Player']
    
    for header in TableName.find('thead').find('tr').find_all('th'):
        col_lst.append(header.text)
    
    return(col_lst)



def PlayerInfo(PlayerName, TableName):
    
    """
    This function extracts the batting and the pitching info of 
    players from their individual web pages
    """
    col_lst = TableHeader(TableName)
    i = 0
    PlayerInfo = {}
    for data in TableName.find('tbody').find_all('tr'):
        val_lst = []
        
        if data.get('id') or 'partial_table' in data.get('class'):
            for rd in data.find_all('th'):
                val_lst.append(PlayerName)
                val_lst.append(rd.text)
            for rd in data.find_all('td'):
                val_lst.append(rd.text)
        
        if val_lst:
            i = i+1
            PlayerInfo[i] = val_lst
    
    df = pd.DataFrame.from_dict(PlayerInfo,orient='index',columns=col_lst)
    return(df)


def RemMultipleLeague(df):
    """
    This function removes the aggregate entries for players from their individual web pages
    """
    return(df.loc[(df['Lg'] != 'MLB') & (df['Lg'] != ''),])


def ExtractMultipleEntries(PageLocation, PlayerName, PlayCategory, SinglePlayerDf, PlayerYearDf):
    
    
    """
    PageLocation: Contains the page location
    PlayerName: Contains the player name for which the data is being extracted
    PlayCategory: pitching / batting
    SinglePlayerDf: single_league_pitchers / single_league_batters
    PlayerYearDf: pitchers_player_year / batters_player_year
    """
    soup = BeautifulSoup(open(PageLocation,'rb'), "html.parser")
    
    ## Extracting standard activity table
    standard_role = soup.find(id=str(PlayCategory)+'_standard')
    standard_role_df = PlayerInfo(PlayerName, standard_role)
    standard_role_df = RemMultipleLeague(standard_role_df)
    standard_role_df.reset_index(inplace = True, drop = True)
    
    ## Extracting the value activity table
    value_role = soup.find(id=str(PlayCategory)+"_value")
    value_role_df = PlayerInfo(PlayerName,value_role)
    value_role_df = RemMultipleLeague(value_role_df)
    value_role_df.reset_index(inplace = True, drop = True)
    
    ## Merging the standard pitching and pitching value table
    merged = standard_role_df.merge(value_role_df, 
                                             how = 'inner', 
                                             left_on = ['Player','Year','Tm','Lg'],
                                            right_on = ['Player','Year','Tm','Lg'],
                                            suffixes = (None, "_y"))
    
    ## Finding out the list of columns 
    merged_cols = set(list(merged.columns))
    
    ## Adding the WAR Column in case of Batting player category
    if PlayCategory == "batting":
        single_league_cols = set(list(SinglePlayerDf.columns)+['WAR'])
    else:
        single_league_cols = set(list(SinglePlayerDf.columns))

    col_diff = single_league_cols.difference(merged_cols)


    for col in col_diff:
        merged[col] = ""
        
    
    merged_df_final = merged[single_league_cols].merge(PlayerYearDf,
                                                                   how = 'inner',
                                                                   left_on = ['Player','Year'],
                                                                   right_on = ['Player','Year'])
    
    return merged_df_final
    
    
    
 
 # Code to separate out players that were added into the final data frame againt those who were not added 
 
 extension = 'html'
page_location = 'D:/UIUC/Era Adjustment/Transfer Players/'
os.chdir("D:/UIUC/Era Adjustment/Transfer Players/")
result = glob.glob('*.{}'.format(extension))

emp_df_pitching = pd.DataFrame()
emp_df_batting = pd.DataFrame()
file_not_added = []
for file in result:
    try:
        player_name = str(file).split('.html')[0]
        file_loc = page_location + file
        if player_name in list(batters_player_year['Player'].unique()):
            bt_df = ExtractMultipleEntries(file_loc,player_name,'batting',single_league_batters,batters_player_year)
        else:
            bt_df = pd.DataFrame()
        
        if player_name in list(pitchers_player_year['Player'].unique()):
            pt_df = ExtractMultipleEntries(file_loc,player_name,'pitching',single_league_pitchers,pitchers_player_year)
        else:
            pt_df = pd.DataFrame()
            
        emp_df_pitching = pd.concat([emp_df_pitching,pt_df])
        emp_df_batting = pd.concat([emp_df_batting,bt_df])
        print("This particular file: "+file+" was successfully added")
    
    except:
        print("This particular file: "+file+" was not added")
        file_not_added.append(file)
        pass
        

# Writing the data frame as csv's into the directory

os.chdir("D:/UIUC/Era Adjustment/Scripts/")
emp_df_batting.to_csv('Transfer_Players_Batting.csv')
emp_df_pitching.to_csv('Transfer_Players_pitching.csv')