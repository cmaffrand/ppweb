import requests as req
from bs4 import BeautifulSoup
from datetime import datetime

# Change month to a number
def month_to_num(month):
    return{
        'November': '11',
        'December': '12',
    }[month]
    
# Get all the games links in a stage
def get_games_links_from_stage(link):    
    # Get data
    data = req.get(link)
    soup = BeautifulSoup(data.text, 'html.parser')
    # Get data table
    links = soup.select('a')
    links = [l.get('href') for l in links]
    links = [l for l in links if l != None]
    links = [l for l in links if '-vs-' in l]
    links = ['https://www.livescores.com' + l for l in links]
    
    return links
    
# Get all urls of stages and stages names
def get_stages_links(link):
    data = req.get(link)
    # Get all data from the page
    soup = BeautifulSoup(data.text, 'html.parser')
    # Get data table
    links = soup.select('a')
    links = [l.get('href') for l in links]
    # Select all world cup links
    links = [l for l in links if '/world-cup/' in l]
    links = [l for l in links if not '-vs-' in l]
    links = [l for l in links if not '/world-cup/?' in l]
    # Remove duplicates
    links = list(dict.fromkeys(links))
    # Complete url
    stage_urls = ['https://www.livescores.com' + l + '&page=1' for l in links]
    
    return stage_urls
      
def get_links_from_all_stages(links):
    all_links = []
    for l in links:
        all_links += get_games_links_from_stage(l)
        
    return all_links

def order_links_with_csv(links):
    ordered_links = []
    # Open csv file
    with open('full_fixture.csv', 'r') as f:
        # Order links according to csv file
        for l in f:
            # Replace " " with "-"
            l = l.replace(" ", "-")
            l = l.split(',')
            if int(l[0]) <= 48:
                for link in links:                
                    if l[2].lower() in link:
                        if l[3].lower() in link:
                            ordered_links.append(link)
    # Append last 16 links
    ordered_links += links[48:]
                
    return ordered_links

def get_game_from_link(link):
    # Get data
    data = req.get(link)
    soup = BeautifulSoup(data.text, 'html.parser')
    # Get game data
    game = soup.select('span')
    # Get Text
    game = [g.text for g in game]
    # if is ' in first position game is not finished
    if "'" in game[0]:
        game = [game[1], game[2], game[4], game[5], game[0]]
    elif "HT" in game[0]:
        game = [game[1], game[2], game[4], game[5], game[0]]
    elif "FT" in game[0]:
        game = [game[1], game[2], game[4], game[5], game[0]]
    else:
        game = [game[1], "?", "?", game[3], game[0]]
    
    return game

def get_all_games_from_links(links):
    game = []
    games = []
    i = 0
    for l in links:
        i += 1
        game.append(i)
        game.append(get_game_from_link(l))
        games.append(game)
        game = []
        
    return games

link = "https://www.livescores.com/football/world-cup/?tz=-3"

links = get_stages_links(link)
links = get_links_from_all_stages(links)
ordered_links = order_links_with_csv(links)

games = get_all_games_from_links(ordered_links)

for g in games:
    print(g)
    



