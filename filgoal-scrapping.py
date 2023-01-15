import requests
from bs4 import BeautifulSoup
import csv


# Get All Cups
def get_cups(soup):
    container_of_cups = soup.find('div',{'id':'match-list-viewer'})
    cups = container_of_cups.find_all('div',{'class':'mc-block'})
    return cups


def count_of_matches(cup):
    matches = cup.find_all('div',{'class':'cin_cntnr'})
    return len(matches)
    
# CUP MATCHES
def get_cup_details(cup):
    
    cup_name = get_cup_title(cup)
    cup_matches = get_cup_matches(cup)
    
    matches_info = []
    
    for i in range(len(cup_matches)):
        
        teams_div = cup_matches[i].find('div',{'class':'c-i-next'})
        details_div = cup_matches[i].find('div',{'class':'match-aux'})
        
        teamA = teams_div.find('div',{'class':'f'}).find('strong').text.strip()
        teamB = teams_div.find('div',{'class':'s'}).find('strong').text.strip()
        
        spans_count = len(details_div.find_all('span'))
        time = details_div.find_all('span')[spans_count-1].text.strip()
        
        score = [] # first index for the first team -> 2nd for 2nd
        score.append(teams_div.find('div',{'class':'f'}).find('b').text.strip()) # first team score
        score.append(teams_div.find('div',{'class':'s'}).find('b').text.strip()) # second team score
        
        matches_info.append({'Cup Type':cup_name, 'Team A':teamA, 'team B': teamB, 'time':time, 'score':f"{score[0]} - {score[1]}" })        
        
    return matches_info
###### end of get_cup_details

# Cup matches divs
def get_cup_matches(cup):
    return cup.find_all('div',{'class':'cin_cntnr'})

 
# Get Cup title
def get_cup_title(cup):
    return cup.contents[1].find('span').text.strip()


#####################
# Main : Entry point
#####################
def main(page):
    src = page.content
    soup = BeautifulSoup(src,'lxml')
    
    all_cups = get_cups(soup)
    
    for cup in all_cups:
        # append each cup details as a dictionary
        all_matches_details.append(get_cup_details(cup))
    
    # print(all_matches_details)
    
    keys = all_matches_details[0][0].keys()
    print(all_matches_details[0])
    
    with open('./matches-details.csv','w') as output_file:
        dict_writer = csv.DictWriter(output_file,keys)
        dict_writer.writeheader()
        for cup in all_matches_details:
            dict_writer.writerows(cup)
        
        
    
####################


# Execution (Calling)
date = input('Please Enter the date : ')
all_matches_details = []
filgoalPage = requests.get(f"https://www.filgoal.com/matches/?date={date}")
main(filgoalPage)

