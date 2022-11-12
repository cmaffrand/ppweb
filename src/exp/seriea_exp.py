import requests as req
from bs4 import BeautifulSoup

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
    games = []
    for l in links:
        games.append(get_game_from_link(l))
    return games

# Get games links from a stage
def get_games_links(link):    
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

# Save all games in a csv file
def get_fixture_csv(link1, link2):
    links1 = get_games_links(link1)
    links2 = get_games_links(link2)
    print(links1)
    print(links2)
    games1 = get_all_games_from_links(links1)
    games2 = get_all_games_from_links(links2)
    print(games1)
    print(games2)
    i = 0
    with open('seriea_fixture.csv', 'w') as f:
        for g in games1:
            i += 1
            f.write(f"{i},Serie A,{g[0]},{g[3]},{g[4]}\n")
        for g in games2:
            i += 1
            f.write(f"{i},Serie A,{g[0]},{g[3]},{g[4]}\n")

link1 = 'https://www.livescores.com/football/italy/serie-a/?tz=-3&date=20221112'
link2 = 'https://www.livescores.com/football/italy/serie-a/?tz=-3&date=20221113'

get_fixture_csv(link1,link2)