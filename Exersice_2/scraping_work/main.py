import requests
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient

url = 'https://quotes.toscrape.com/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

#Collecting data for quotes.json:
quotes = soup.find_all('span', class_='text')
authors = soup.find_all('small', class_='author')
tags = soup.find_all('div', class_='tags')
quotes_list = []
author_links = set()

for i in range(len(quotes)):
    author = authors[i].text
    tagsforquote = tags[i].find_all('a', class_='tag')
    tags_list = [tag.text for tag in tagsforquote]
    quotes_dict = {"tags": tags_list, 
                   "author": author, 
                   "quote": quotes[i].text}
    quotes_list.append(quotes_dict)
    #Collecting links for authors:
    author_link = soup.find_all('small', class_='author')[i].find_next_sibling('a')['href']
    author_links.add(url + author_link)

#Creating quotes.json:
with open("quotes.json", "w", encoding="utf-8") as f:
    json.dump(quotes_list, f)

#Collecting data for authors.json:
authors_about_list = []

for link in author_links:
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'lxml')

    fullname = soup.find('h3', class_='author-title').text.strip()
    born_date = soup.find('span', class_='author-born-date').text.strip()
    born_location = soup.find('span', class_='author-born-location').text.strip()
    description = soup.find('div', class_='author-description').text.strip()

    author_about = {
        "fullname": fullname,
        "borndate": born_date,
        "born-location": born_location,
        "description": description
    }
    authors_about_list.append(author_about)

#Creating authors.json:
with open("authors.json", "w", encoding="utf-8") as f:
    json.dump(authors_about_list, f)

#Insert data to BD:
# Connect to MongoDB
client = MongoClient("mongodb+srv://marina27043:I2gR3SalxamYUzYG@cluster0.vcftq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['Authors_and_quotes']

# Load JSON data and insert into MongoDB
with open('authors.json', 'r', encoding='utf-8') as f:
    authors_data = json.load(f)
    db.authors.insert_many(authors_data)

with open('quotes.json', 'r', encoding='utf-8') as f:
    quotes_data = json.load(f)
    db.quotes.insert_many(quotes_data)

print("Data imported successfully!")