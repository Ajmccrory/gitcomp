from flask import Flask, request, render_template, redirect, url_for, session
from uuid import uuid4
import json
from git_scraper import GithubScraper
"""
Flask interface for github comparison app.

Author: AJ McCrory
Version: 2.0.1 5/16/2024
"""

app = Flask(__name__)
scraper = GithubScraper()

@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        user1 = request.form['user1']
        user2 = request.form['user2']
        scraper.compare_user_contributions(user1, user2)
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000) 