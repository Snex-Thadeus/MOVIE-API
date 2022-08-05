from bs4 import BeautifulSoup
from importlib_metadata import re
import requests, openpyxl
from datetime import datetime
import config


# excel = openpyxl.Workbook()
# sheet = excel.active
# sheet.title = 'Top Rated Movies'
# sheet.append(['Movie_Rank', 'Movie_Name', 'Year_of_Release', 'Movie_Rating', 'Movie_Duration', 'Movie_Description', 'Date_Time'])

data = []

import psycopg2

#establishing the connection
conn = psycopg2.connect(
   database=config.database, user=config.user, password=config.password, host=config.host, port=config.port
)


#Creating a cursor object using the cursor() method
cursor = conn.cursor()

try:
    source = requests.get('https://www.imdb.com/search/title/?count=250&groups=top_250&sort=user_rating')
    source.raise_for_status() #If url has some issues
    
    soup = BeautifulSoup(source.text, 'html.parser')
    
    #movies = soup.find('tbody', class_="lister-list").find_all('tr')
    movies = soup.findAll('div', attrs={'class': 'lister-item mode-advanced'})
    
    for movie in movies:
        
        name = movie.h3.a.text
        
        rating = movie.find('div', class_="inline-block ratings-imdb-rating").text.strip()
        
        year = movie.h3.find('span', class_="lister-item-year text-muted unbold").text.strip('()').strip('I) (').lstrip('(')
        
        duration = movie.p.find('span', class_='runtime').text.strip('min')
        
        rank = movie.h3.find('span', class_="lister-item-index unbold text-primary").text.split('.')[0]
        
        description = movie.select('.text-muted')[2].get_text().strip().replace( '"', '')
        
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
 
        #print(name)
        result = (rank, name, year, rating, duration, description, dt_string)
        
        data.append(result)
        
        # sheet.append([rank, name, year, rating, duration, description, dt_string])       
    
    
except Exception as e:
    print(e)


for d in data:
    cursor.execute('INSERT into public."MovieAPI_movies"  VALUES (%s, %s, %s, %s, %s, %s, %s)', d)
    #print("Insert Done")
    
conn.commit()


# excel.save('IMDB Top Movies.csv')