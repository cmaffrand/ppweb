import requests as req
from bs4 import BeautifulSoup
from datetime import datetime

# Change month to a number
def month_to_num(month):
    return{
        'November': '11',
        'December': '12',
    }[month]
    
# Get single data games with date and time
def get_games(link,stage):
    # Get date
    data = req.get(link)
    # Get all data from the page
    soup = BeautifulSoup(data.text, 'html.parser')
    # Get data table
    result_tables = soup.select('div.la')[0]
    # Get all games
    days_html = result_tables.select('span.sa')
    days = [d.text for d in days_html]
    # Split day from month
    days = [d.split(' ') for d in days]
    # change month to number
    days = [[month_to_num(d[0]), d[1]] for d in days]
    # Add year
    days = [['22', d[0], d[1]] for d in days]
    if stage == "Group A":
        days = [days[0], days[1], days[2], days[2], days[3], days[3]]
    elif stage == "Round Of 16":
        days = [days[0], days[0], days[1], days[1], days[2], days[2], days[3], days[3]]
    elif stage == "Quarter Finals":
        days = [days[0], days[0], days[1], days[1]]
    elif stage == "Semi Finals":
        days = [days[0], days[1]]
    elif stage[0] == "G": # Group Stage (No A)
        days = [days[0], days[0], days[1], days[1], days[2], days[2]]
    else: # Final and Third Place
        days = [days[0]]
    # Get all games
    games_html = result_tables.select('div.Ii')
    games = [g.text for g in games_html]
    # Split games in teams
    games = [g.split(' - ') for g in games]
    # Slit first five characters of teams
    games = [[g[0][5:], g[1], g[0][:5]] for g in games]
    games = [[g[0][:-1], g[0][-1], g[1][0], g[1][1:], g[2]] for g in games]
    # join day and time
    full_games = []
    for i in range(len(games)):
        full_games.append(games[i][:4] + days[i] + games[i][4:])    
    # Split time in hours and minutes
    full_games = [[g[0], g[1], g[2], g[3], g[4], g[5], g[6], g[7][:2], g[7][3:]] for g in full_games]    
    # Convert to datetime 
    time_format = "%y/%m/%d %H:%M:%S"
    full_games = [[g[0], g[1], g[2], g[3], datetime.strptime(f"{g[4]}/{g[5]}/{g[6]} {g[7]}:{g[8]}:00", time_format)] for g in full_games]
    # Change '-' by '/' in datetimes
    full_games = [[g[0], g[1], g[2], g[3], g[4].strftime(time_format).replace('-', '/')] for g in full_games]
    # Append stage
    full_games = [[stage, g[0], g[1], g[2], g[3], g[4]] for g in full_games]
    
    return full_games

# Get all urls of stages and stages names
def get_stages_links(link):
    data = req.get(link)
    # Get all data from the page
    soup = BeautifulSoup(data.text, 'html.parser')
    # Get data table
    links = soup.select('a.Ue')
    links = [l.get('href') for l in links]
    # Select all world cup links
    links = [l for l in links if '/world-cup/' in l]
    # Remove first link
    links = links[1:]
    game_urls = ['https://www.livescores.com' + l + '?tz=-3&page=1' for l in links]
    # Get Stage names from the links
    stages = [l.split('/')[3] for l in links]
    # Changer '-' by ' '
    stages = [s.replace('-', ' ') for s in stages]
    # Capital Letter in the first letter of each word
    stages = [s.title() for s in stages]
    # Append game_urls and stage name
    full_links = [[game_urls[i], stages[i]] for i in range(len(game_urls))]
    
    return full_links

# From Link get all games
def get_all_games(link):
    # Get all stages links
    stages_links = get_stages_links(link)
    # Get all games
    all_games = []
    for s in stages_links:
        all_games += get_games(s[0], s[1])
        
    # Sort by date
    all_games = sorted(all_games, key=lambda x: x[5])
    
    return all_games

# Save all games in a csv file
def get_fixture_csv():
    results_url = "https://www.livescores.com/football/world-cup/"
    all_games = get_all_games(results_url)
    i = 0
    with open('full_fixture.csv', 'w') as f:
        for g in all_games:
            i += 1
            f.write(f"{i},{g[0]},{g[1]},{g[4]},{g[5]}\n")

get_fixture_csv()







