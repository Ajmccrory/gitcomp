from scrapers import git_scraper

USERNAMES = ['Ajmccrory', 'bfu4', 'goxiaoy', 'oscartbeaumont']

def test_github_scraper():
    scraper = git_scraper.GithubScraper()

    for user in USERNAMES:
        scraper.scrape_user_data(user)
    scraper.close()

def test_compare_users():
    scraper = git_scraper.GithubScraper()
    scraper.compare_users_contributions(USERNAMES[0], USERNAMES[1])

    scraper.compare_users_contributions(USERNAMES[2], USERNAMES[3])

    scraper.compare_users_contributions(USERNAMES[0], USERNAMES[3])
    
    scraper.compare_users_contributions(USERNAMES[1], USERNAMES[2])

    scraper.close()

def test_repo_collection():
    scraper = git_scraper.GithubScraper()
    for user in USERNAMES:
        repos = scraper.get_repos(user)
        print(repos)
        print(len(repos))

if __name__ == '__main__':
    test_github_scraper()
    test_compare_users()
    test_repo_collection()

