from scrapers import git_scraper

def main():
    cnt = 1
    scraper = git_scraper.GithubScraper()
    while cnt == 1:
        username1 = input("Enter first GitHub username: ")
        scraper.scrape_user_data(username1)
        
        username2 = input("Enter second GitHub username: ")
        scraper.scrape_user_data(username2)

        scraper.compare_users_contributions(username1, username2)
        cnt = input('Would you like to compare more users? 1-yes 0-No')
        if cnt == 0:
            scraper.close()


if __name__ == "__main__":
    main()