from flask import Flask, request, render_template # redirect, url_for, session
from git_scraper.git_scraper import GithubScraper
"""
Flask interface for github comparison app.

Author: AJ McCrory
Version: 2.0.1 5/16/2024
"""

app = Flask(__name__)
scraper = GithubScraper()

def compiled_data(scraped_data):
    


@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        user1 = request.form['user1']
        user2 = request.form['user2']
        scraped = scraper.compare_users_contributions(user1, user2)
        return compiled_data(scraped)
    return render_template('index.html')

@app.route('/scrape', methods=['GET', 'POST'])
def scrape_user_data():
    return render_template('scraping.html')

@app.route('/exisiting', methods=['GET', 'POST'])
def check_user_exists():
    return render_template('existing_user.html')

@app.route('/clear', methods=['GET', 'POST'])
def clear_mongo_collection():
    return render_template('clear_collection.html')



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000) 