#!/usr/bin/env python3
from scrapers import git_scraper

if __name__ == '__main__':

    cnt = int(input('1- Compare\n2- scrape user repos\n3- check for user info]\n4- clear collection\n5- close\n '))
    scraper = git_scraper.GithubScraper()
    while cnt != 5:

        if cnt == 1:
            username1 = input("Enter first GitHub username: ")
            scraper.scrape_user_data(username1)
            
            username2 = input("Enter second GitHub username: ")
            scraper.scrape_user_data(username2)

            scraper.compare_users_contributions(username1, username2)
            cnt = int(input('1- Compare\n2- scrape user repos\n3- check for user info]\n4- clear collection\n5- close\n '))

        elif cnt == 2:
            username = input("Enter the users repos you'd like to scrape: ")
            repos = scraper.get_repos(username)
            print(repos)
            cnt = int(input('1- Compare\n2- scrape user repos\n3- check for user info]\n4- clear collection\n5- close\n '))

        elif cnt == 3:
            username = input("what user do you wish to search db for?: ")
            user_info = scraper.mongo.find_one({'username': username})
            print(user_info)
            cnt = int(input('1- Compare\n2- scrape user repos\n3- check for user info]\n4- clear collection\n5- close\n '))

        elif cnt == 4:
            si_or_no = input('Are you sure you want to clear the collections? 1 - yes : 0 - no: ')
            if si_or_no == 1:
                cleared = scraper.mongo.clear_collection()
                print(cleared)
            cnt = int(input('1- Compare\n2- scrape user repos\n3- check for user info]\n4- clear collection\n5- close\n '))

    scraper.close()
    

