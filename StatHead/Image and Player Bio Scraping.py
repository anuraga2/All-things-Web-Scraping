# Code for Player Image Scraping
# Importing the modules
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import shutil,os


## Reading the url file and cleaning the data
player_url = pd.read_csv("PlayerDict.csv")
del player_url['Unnamed: 0']
player_url.set_index('Name',inplace = True)
player_dict = player_url.to_dict()['Link']

## Defining the two core functions for scraping the image

# Function to fetch the url of a particular player and return the html of the web page
def getdata(url):  
    r = requests.get(url)  
    return r.text

# Function to download the image of the player
def DownloadImage(soup, player):
    
    """
    Takes in two parameters
    soup: The soup object of the player being called
    player: The player name in String format
    """
    filename = player + '.jpg'
    loop_var = True
    for item in soup.find_all('img'):
        if re.search('headshots', item['src']):
            while loop_var:
                r = requests.get(item['src'], stream = True)
                print(item['src'])
                if r.status_code == 200:
                    r.raw.decode_content = True
                    with open(filename,'wb') as f:
                        shutil.copyfileobj(r.raw, f)
                    print('Image sucessfully Downloaded: ',filename, ':',player)
                else:
                    print('Image Couldn\'t be retreived', player)
                loop_var = False


# Iterating over all the player Names and downloading the images in the working directory
for player in player_dict:
    htmldata = getdata(player_dict[player])
    soup = BeautifulSoup(htmldata, 'html.parser')
    DownloadImage(soup, player)



## Reading the url file and cleaning the data
player_url = pd.read_csv("PlayerDict.csv")
del player_url['Unnamed: 0']
player_url.set_index('Name',inplace = True)
player_dict = player_url.to_dict()['Link']

def getdata(url):  
    r = requests.get(url)  
    return r.text


def player_bio(player_name,soup):
    bio_header = [item.getText() for item in soup.find("div", {"id": "info"}).find("div").find_all("strong")]
    bio_details = [item.next_sibling.strip() for item in soup.find("div", {"id": "info"}).find("div").find_all("strong")]
    player_det = pd.DataFrame({
        'player_name': [player_name]*len(bio_header),
        'bio_header': bio_header,
        'bio_details':bio_details
    })
    
    return player_det


def career_summary(player,soup):
    i = 1
    loop_var = True
    header = []
    value = []
    player_career_summary = soup.find("div",{"class":"stats_pullout"})
    while loop_var:
        class_name = "p"+str(i)
        if player_career_summary.find("div",{"class":class_name}):
            header_list = [item.getText() for item in player_career_summary.find("div",{"class":class_name}).find_all('h4')]
            header += header_list
            value_list = [item.getText() for item in player_career_summary.find("div",{"class":class_name}).find_all('p')]
            value += value_list
            i = i + 1
        else:
            loop_var = False

        df = pd.DataFrame({
            'player_name': [player]*len(header),
            'player_stats': header,
            'player_stats_value':value
        })
        
        return df

bio_df = pd.DataFrame()
summary_df = pd.DataFrame()
i = 1
player_skipped = []
for keys in player_dict:
    
    htmldata = getdata(player_dict[keys])
    soup = BeautifulSoup(htmldata, 'html.parser')
    
    try:
        print(i)
        i = i+1
        # Getting individual bio data frames
        indi_bio_data = player_bio(keys,soup)
        bio_df = pd.concat([bio_df, indi_bio_data])
    
        #Getting individual career summary
        indi_career_summary = career_summary(keys,soup)
        summary_df = pd.concat([summary_df, indi_career_summary])
    
    except:
        player_skipped.append(keys)
        continue

# Putting the list of players in a files for which data could not be pulled. will be looking into the pages of these player
# s later
with open('det_missing.txt', 'w') as f:
    for item in player_skipped:
        f.write("%s\n" % item)

# saving the player bio data
bio_df.to_csv("bio_data.csv",index=False)
summary_df.to_csv("summary_data.csv",index=False)