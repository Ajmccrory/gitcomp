#!/usr/bin/env python3
from scrapers import git_scraper

if __name__ == '__main__':

    cnt = 1
    scraper = git_scraper.GithubScraper()
    while cnt == 1:
        username1 = input("Enter first GitHub username: ")
        scraper.scrape_user_data(username1)
        
        username2 = input("Enter second GitHub username: ")
        scraper.scrape_user_data(username2)

        scraper.compare_users_contributions(username1, username2)
        cnt = int(input('Would you like to compare more users? 1-yes 0-No\n'))
        if cnt == 0:
            scraper.close()
