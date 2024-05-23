import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
from flask import Flask, request, render_template, redirect, url_for
from git_scraper.git_scraper import GithubScraper
import matplotlib.pyplot as plt
import os
import logging
import uuid

app = Flask(__name__)
scraper = GithubScraper()
logging.basicConfig(level=logging.INFO)

def compile_data(scraped_data, users):
    if len(scraped_data) < 2:
        raise ValueError("Insufficient data for comparison.")

    # Extracting contribution values for each user
    contributions = {user: int(data) for user, data in zip(users, scraped_data)}

    # Creating the bar chart
    plt.figure()
    colors = ['blue', 'green', 'red', 'purple']  # Colors for each user's bar
    labels = list(contributions.keys())
    values = list(contributions.values())

    plt.bar(labels, values, color=colors[:len(labels)])
    plt.title('Comparison of User Contributions')
    plt.xlabel('Users')
    plt.ylabel('Contributions')
    plt.xticks(rotation=45)
    plt.tight_layout()

    filename = f'static/bar_chart_{uuid.uuid4().hex}.png'
    plt.savefig(filename)

    return filename

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/compare', methods=['GET','POST'])
def compare():
    if request.method == 'POST':
        usernames = [request.form.get(f'user{i}') for i in range(1, 5)]
        valid_usernames = [username for username in usernames if username]  # Remove empty usernames

        if len(valid_usernames) < 2:
            return render_template('error.html', error="Please provide 2 to 4 usernames.")

        try:
            for user in usernames:
                scraper.scrape_user_data(user)
            contributions = scraper.compare_users_contributions(valid_usernames)
            plot_path = compile_data(contributions, valid_usernames)
            return render_template('compare_users.html', plot_path=plot_path, usernames=valid_usernames, contributions=contributions)
        except ValueError as e:
            return render_template('error.html', error=str(e))
        except Exception as e:
            logging.error(f"Error occurred: {str(e)}")
            return render_template('error.html', error="An error occurred during comparison.")
    return render_template('compare_page.html')

@app.route('/display_comparison', methods=['GET'])
def display_comparison():
    plot_path = request.args.get('plot_path')
    return render_template('compare_users.html', plot_path=plot_path)

@app.route('/scrape', methods=['GET', 'POST'])
def scrape_user_data():
    if request.method == 'POST':
        username = request.form.get('username')
        if not username:
            return render_template('error.html', error="Please provide a username.")
        try:
            return redirect(url_for('show_scraped_data'))
        except Exception as e:
            logging.error(f"Error occurred: {str(e)}")
            return render_template('error.html', error=f"An error occurred: {str(e)}")

    return render_template('scraping.html')


@app.route('/scraped_user', methods=['GET', 'POST'])
def show_scraped_data():
    if request.method == 'POST':
        username = request.form.get('username')
        if not username:
            return render_template('error.html', error="Please provide a username.")
        repos = scraper.get_repos(username)
        return render_template('scraped.html', username=username, repos=repos)
    return render_template('scraped.html')  # Return the form if it's a GET request


@app.route('/existing', methods=['GET', 'POST'])
def check_user_exists():
    if request.method == 'POST':
        username = request.form.get('existing')
        if not username:
            return render_template('error.html', error="Please provide a username.")

        user_data = scraper.mongo.find_one({'username': username})
        if user_data:
            return render_template('existing_user.html', user_data=user_data)
        else:
            return render_template('error.html', error="User not found in the database.")

    return render_template('existing_user.html')

@app.route('/clear', methods=['GET', 'POST'])
def clear_mongo_collection():
    if request.method == 'POST':
        username = request.form.get('username')
        if not username:
            return render_template('error.html', error="Please provide a username.")

        try:
            scraper.mongo.clear_collection(username)
            return redirect(url_for('clear_collection_success'))
        except Exception as e:
            logging.error(f"Error occurred: {str(e)}")
            return render_template('error.html', error="An error occurred while clearing the collection.")

    return render_template('clear_collection.html')

@app.route('/clear_collection_success', methods=['GET'])
def clear_collection_success():
    username = request.args.get('username')  # Get the username from the query parameters
    return render_template('clear_collection_success.html', message=username)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
