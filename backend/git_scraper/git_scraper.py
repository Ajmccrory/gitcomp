import requests
from requests.exceptions import Timeout
from bs4 import BeautifulSoup
import logging
from data.mongo_ops import MongoOperations
from helpers.comparison import Comparison


class GithubScraper:
    """
    Class for scraping GitHub data and performing comparisons.

    Attributes:
        mongo (MongoOperations): Instance of MongoDB operations.
        logger (Logger): Logger instance for logging messages.
    """

    def __init__(self):
        """
        Initialize GithubScraper class with MongoDB operations and logger.
        """
        self.mongo = MongoOperations()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def scrape_user_data(self, username):
        """
        Scrape contribution data for a given GitHub username and store it in MongoDB.

        Args:
            username (str): GitHub username.

        Raises:
            ValueError: If username is empty or data retrieval fails.
        """
        if not username:
            raise ValueError("Username cannot be empty.")

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
                        break
                    else:
                        self.logger.warning(f"No contributions data found for user '{username}'.")
                else:
                    self.logger.error(f"Failed to fetch data for user '{username}'. Status code: {response.status_code}")
            except Timeout:
                self.logger.error(f'Timeout has occurred while fetching data for user {username}')
            except Exception as e:
                self.logger.exception(f"Error scraping data for user '{username}': {e}")
                if attempt == retries - 1:
                    raise

    def get_users_contributions(self, usernames):
        """
        Use compare helper to compare the contribution amount of two users.

        Args:
            usernames (list): List of GitHub usernames.

        Returns:
            list: Contributions of the users.

        Raises:
            ValueError: If insufficient usernames provided or data is missing.
        """
        if len(usernames) < 2 or len(usernames) > 4:
            raise ValueError("You must compare at least 2 and at most 4 users.")

        user_data = [self.mongo.find_one({'username': username}) for username in usernames]
        if any(data is None for data in user_data):
            missing_users = [usernames[i] for i, data in enumerate(user_data) if data is None]
            raise ValueError(f"No data found for users: {', '.join(missing_users)}")

        comp = Comparison(usernames, user_data)
        return comp.compare_users()

    def get_repos(self, username):
        """
        Fetch and store repositories of a given GitHub user.

        Args:
            username (str): GitHub username.

        Returns:
            list: List of repository names.

        Raises:
            ValueError: If username is empty or no repositories are found.
        """
        if not username:
            raise ValueError("Username cannot be empty.")

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
                    self.logger.error(f"Failed to fetch data for user '{username}'. Status code: {response.status_code}")
            except Timeout:
                self.logger.error(f'Timeout has occurred while fetching data for user {username}')
            except Exception as e:
                self.logger.exception(f"Error scraping data for user '{username}': {e}")
                if attempt == retries - 1:
                    raise

    def get_similarity(self, usernames):
        """
        Compares the repositories of multiple users from their stored data in their mongo collection.

        Args:
            usernames (list): list of usernames whos repsitory to compare.

        Returns:
            dict: A dictionary where keys are repo names and vals are lists of usernames that have that repo
        """
        if len(usernames) < 2 or len(usernames) > 4:
            raise ValueError("You must compare at least 2 and at most 4 users.")
        
        user_repos = {}
        for user in usernames:
            user_data = self.mongo.repo_collection.find({'username': user})
            if user_data is None:
                raise ValueError(f"No data found for user '{user}'.")
            user_repos[user] = [repo['repository'] for repo in user_data]

        # Create a dict to store the comparison results
        repo_comparison = {}
        for username, repos in user_repos.items():
            for repo in repos:
                if repo not in repo_comparison:
                    repo_comparison[repo] = []
                repo_comparison[repo].append(username)

        # Filter to only include repos that have contributions from more than one user.
        repo_comparison = {repo: users for repo, users in repo_comparison.items() if len(users) > 1}

        return repo_comparison
    
    def get_user_data(self, username):
        """
        Compile user data into a dict with one key that is user and one value that is 
        that users important information.
        Args:
            username (str): name for the user 
        """
        if not username:
            raise ValueError("Username cannot be empty.")
        user_data = self.mongo.find_one({'username': username})
        if user_data:
            self.logger.info(f'User data for {username} found.')
        else:
            self.logger.info(f'data for {username} not found')
            try:
                self.scrape_user_data(username)
                self.get_repos(username)
                user_data = [self.mongo.find_one({'username': username})]
            except Exception as e:
                self.logger.error(f'Error occured while scraping {username} data: {e}')
                raise

        if not user_data:
            raise ValueError(f'Failed to retrieve data for user {username}')
        
        repos_data = list(self.mongo.repo_collection.find({'username': username}))
        repositories = [repo['repository'] for repo in repos_data]

        return {
            'username': username,
            'contributions_last_year': user_data.get('user_contributions', 0),
            'repositories': repositories
        }
        
    def close(self):
        """
        Close MongoDB connection.
        """
        self.mongo.close()
