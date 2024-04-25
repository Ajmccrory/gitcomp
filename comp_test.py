from scrapers import git_scraper

def test_github_scraper():
    scraper = git_scraper.GithubScraper()

    usernames = ['Ajmccrory', 'bfu4', 'goxiaoy', 'oscartbeaumont']
    for user in usernames:
        scraper.scrape_user_data(user)

    scraper.compare_users_contributions(usernames[0], usernames[1])

    scraper.compare_users_contributions(usernames[2], usernames[3])

    scraper.compare_users_contributions(usernames[0], usernames[3])
    
    scraper.compare_users_contributions(usernames[1], usernames[2])

    scraper.close()

if __name__ == '__main__':
    test_github_scraper()

