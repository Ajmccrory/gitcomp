from scrapers import git_scraper

def main():
    scraper = git_scraper.GithubScraper('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')
    username1 = input("Enter first GitHub username: ")
    scraper.get_user_data(username1)
    
    username2 = input("Enter second GitHub username: ")
    scraper.get_user_data(username2)

    scraper.compare_users_contributions(username1, username2)
    
    scraper.close()

if __name__ == "__main__":
    main()