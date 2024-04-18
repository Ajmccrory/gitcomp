import requests
from requests.exceptions import Timeout
from bs4 import BeautifulSoup
from datetime import datetime
from src import comparison
from data import mongo_ops


class GithubScraper:
    def __init__(self):
        self.cached_users = []
        self.mongo = mongo_ops.MongoOperations()
        
    def scrape_user_data(self, username):
        if username in self.cached_users:
            print(f"Data for user '{username}' already cached.")
            return

        url = f'https://github.com/users/{username}/contributions'
        retries = 3

        for attempt in range(retries):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    contributions = soup.find('h2', class_='f4 text-normal mb-2')
                    contributions_text = contributions.get_text(strip=True)
                    cont_num = contributions_text.split()[0]
                    cont = int(cont_num)
                    if cont_num:
                        data = {'username': username, 'contributions_last_year': cont}
                        self.mongo.insert_one(data)
                        self.cached_users.append(username)
                        print(f'data for user {username} stored.')
                        break
                    else:
                        print(f"No contributions data found for user '{username}'.")
                else:
                    print(f"Failed to fetch data for user '{username}'. Status code: {response.status_code}")
            except Timeout:
                print(f'Timeout has occured while fetching data for user {username}')
            except Exception as e:
                print(f"Error scraping data for user '{username}': {e}")



    def compare_users_contributions(self, username1, username2):
        user1_data = self.mongo.find_one({'username': username1})
        user2_data = self.mongo.find_one({'username': username2})
        return comparison.compare(username1, username2, user1_data, user2_data)
    
    def close(self):
        self.mongo.close()

