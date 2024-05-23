import requests
from requests.exceptions import Timeout
from bs4 import BeautifulSoup
import logging
from data import mongo_ops
from src import comparison


class GithubScraper:
    def __init__(self):
        self.cached_users = []
        self.mongo = mongo_ops.MongoOperations()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def scrape_user_data(self, username):
        """
        Scrapes contribution data for a given GitHub username and stores it in MongoDB.

        Args:
            username (str): GitHub username.

        Raises:
            ValueError: If contributions data is not found for the user.
        """
        if username in self.cached_users:
            self.logger.info(f"Data for user '{username}' already cached.")
            return

        url = f'https://github.com/users/{username}/contributions'
        retries = 3

        for attempt in range(retries):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    contributions = soup.find('h2', class_='f4 text-normal mb-2')
                    if contributions:
                        contributions_text = contributions.get_text(strip=True)
                        cont_num = contributions_text.split()[0]
                        cont = cont_num.replace(',', '') if len(cont_num) > 4 else cont_num
                        data = {'username': username, 'contributions_last_year': int(cont)}
                        self.mongo.insert_one(data)
                        self.cached_users.append(username)
                        self.logger.info(f'Data for user {username} stored.')
                        break
                    else:
                        self.logger.warning(f"No contributions data found for user '{username}'.")
                else:
                    self.logger.error(
                        f"Failed to fetch data for user '{username}'. Status code: {response.status_code}")
            except Timeout:
                self.logger.error(f'Timeout has occurred while fetching data for user {username}')
            except Exception as e:
                self.logger.exception(f"Error scraping data for user '{username}': {e}")
                if attempt == retries - 1:
                    raise

    def compare_users_contributions(self, usernames):
        """
        Compares contributions of multiple users.

        Args:
            usernames (list): List of GitHub usernames.

        Returns:
            list: Contributions of the users.

        Raises:
            ValueError: If an insufficient number of usernames is provided or data is missing.
        """
        if len(usernames) < 2 or len(usernames) > 4:
            raise ValueError("You must compare at least 2 and at most 4 users.")

        user_data = [self.mongo.find_one({'username': username}) for username in usernames]
        if any(data is None for data in user_data):
            missing_users = [usernames[i] for i, data in enumerate(user_data) if data is None]
            raise ValueError(f"No data found for users: {', '.join(missing_users)}")

        comp = comparison.Comparison(usernames, user_data)
        return comp.compare_users()

    def get_repos(self, username):
        """
        Fetches and stores repositories of a given GitHub user.

        Args:
            username (str): GitHub username.

        Returns:
            list: List of repository names.

        Raises:
            ValueError: If no repositories are found for the user.
        """
        url = f'https://github.com/{username}?tab=repositories'
        retries = 3

        for attempt in range(retries):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    repo_list = soup.find_all('h3', class_='wb-break-all')
                    if repo_list:
                        repositories = [repo.text.strip() for repo in repo_list]
                        for repo_name in repositories:
                            self.mongo.repo_collection.insert_one({'username': username, 'repository': repo_name})
                        return repositories
                    else:
                        self.logger.warning(f'No repositories found for {username}')
                        raise ValueError(f"No repositories found for user '{username}'.")
                else:
                    self.logger.error(
                        f"Failed to fetch data for user '{username}'. Status code: {response.status_code}")
            except Timeout:
                self.logger.error(f'Timeout has occurred while fetching data for user {username}')
            except Exception as e:
                self.logger.exception(f"Error scraping data for user '{username}': {e}")
                if attempt == retries - 1:
                    raise

    def close(self):
        """Closes the MongoDB connection."""
        self.mongo.close()
