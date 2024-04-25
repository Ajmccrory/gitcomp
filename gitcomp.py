#!/usr/bin/env python3
from scrapers import git_scraper

if __name__ == '__main__':

    cnt = 1
    scraper = git_scraper.GithubScraper()
    while cnt != 3:
        username1 = input("Enter first GitHub username: ")
        scraper.scrape_user_data(username1)
        
        username2 = input("Enter second GitHub username: ")
        scraper.scrape_user_data(username2)

        scraper.compare_users_contributions(username1, username2)
        cnt = int(input('1- Compare again, 2- clear collection, 3- close\n'))
        if cnt == 3:
            scraper.close()
        if cnt == 2:
            scraper.mongo.clear_collection()

