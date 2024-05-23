import unittest
from unittest.mock import MagicMock
from git_scraper.git_scraper import GithubScraper
from data.mongo_ops import MongoOperations
from src.comparison import Comparison


class TestGithubScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = GithubScraper()

    def tearDown(self):
        self.scraper.close()

    def test_scrape_user_data(self):
        # Mocking the MongoDB insert_one method
        self.scraper.mongo.insert_one = MagicMock()

        # Testing the scrape_user_data function
        self.scraper.scrape_user_data('test_user')

        # Asserting that insert_one was called with the correct arguments
        self.scraper.mongo.insert_one.assert_called_once_with(
            {'username': 'test_user', 'contributions_last_year': '100'})

    def test_compare_users_contributions(self):
        # Mocking the MongoDB find_one method
        self.scraper.mongo.find_one = MagicMock(side_effect=[
            {'username': 'user1', 'contributions_last_year': '100'},
            {'username': 'user2', 'contributions_last_year': '150'}
        ])

        # Testing the compare_users_contributions function
        result = self.scraper.compare_users_contributions(['user1', 'user2'])

        # Asserting the result of the comparison
        self.assertEqual(result, ['user1', 'user2', 'user2'])

    def test_get_repos(self):
        # Mocking the requests.get method
        requests_mock = MagicMock()
        requests_mock.status_code = 200
        requests_mock.text = '<h3 class="wb-break-all">repo1</h3><h3 class="wb-break-all">repo2</h3>'
        self.scraper.requests.get = MagicMock(return_value=requests_mock)

        # Testing the get_repos function
        repos = self.scraper.get_repos('test_user')

        # Asserting the returned repositories
        self.assertEqual(repos, ['repo1', 'repo2'])


if __name__ == '__main__':
    unittest.main()
