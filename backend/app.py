import base64
from flask import Flask, request, render_template, redirect, url_for
from git_scraper.git_scraper import GithubScraper
import matplotlib
import matplotlib.pyplot as plt
import io
import logging
import uuid

matplotlib.use('Agg')  # Use a non-interactive backend

app = Flask(__name__)
scraper = GithubScraper()
logging.basicConfig(level=logging.INFO)

# Custom filter for base64 encoding
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

    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)

    file_id = scraper.mongo.save_image(img_bytes, f'bar_char_{uuid.uuid4().hex}.png')
    return file_id
# Custom filter for base64 encoding
def b64encode_filter(data):
    return base64.b64encode(data).decode('utf-8')

# Register the custom filter with Flask
app.jinja_env.filters['b64encode'] = b64encode_filter


@app.route('/')
def homepage():
    """
    Renders the homepage.
    """
    return render_template('index.html')

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    """
    Handles the comparison of user contributions.
    If the request method is POST, it scrapes data for the provided usernames and generates a comparison chart.
    """
    if request.method == 'POST':
        usernames = [request.form.get(f'user{i}') for i in range(1, 5)]
        valid_usernames = [username for username in usernames if username]

        if len(valid_usernames) < 2 or len(valid_usernames) > 4:
            return render_template('error.html', error="Please provide 2 to 4 usernames.")

        for user in valid_usernames:
            scraper.scrape_user_data(user)

        try:
            contributions = scraper.compare_users_contributions(valid_usernames)
            plot_id = compile_data(contributions, valid_usernames)
            return redirect(url_for('display_comparison', plot_id=plot_id))
        except ValueError as e:
            return render_template('error.html', error=str(e))
        except Exception as e:
            error_message = f"An error occurred during comparison. {str(e)}"
            return render_template('error.html', error=error_message)
    return render_template('compare_page.html')

@app.route('/display_comparison', methods=['GET'])
def display_comparison():
    plot_id = request.args.get('plot_id')
    if plot_id is None:
        return render_template('error.html', error="No plot ID provided.")
    try:
        image_data = scraper.mongo.get_image(plot_id)
        return render_template('compare_users.html', plot_data=image_data)
    except Exception as e:
        return render_template('error.html', error=f"An error occurred while retrieving the image: {str(e)}")
@app.route('/scrape', methods=['GET', 'POST'])
def scrape_user_data():
    """
    Scrapes user data from GitHub.
    If the request method is POST, it scrapes data for the provided username.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        if not username:
            return render_template('error.html', error="Please provide a username.")

        try:
            scraper.scrape_user_data(username)
            return redirect(url_for('show_scraped_data', username=username))
        except Exception as e:
            logging.error(f"Error occurred: {str(e)}")
            return render_template('error.html', error=f"An error occurred: {str(e)}")

    return render_template('scraping.html')

@app.route('/scraped_user', methods=['GET', 'POST'])
def show_scraped_data():
    """
    Displays the scraped data for the given username.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        if not username:
            return render_template('error.html', error="Please provide a username.")
        repos = scraper.get_repos(username)
        return render_template('scraped.html', username=username, repos=repos)
    return render_template('scraped.html')

@app.route('/existing', methods=['GET', 'POST'])
def check_user_exists():
    """
    Checks if the user exists in the database.
    If the request method is POST, it checks for the provided username.
    """
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
    """
    Clears the MongoDB collection for the given username.
    If the request method is POST, it clears data for the provided username.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        if not username:
            return render_template('error.html', error="Please provide a username.")

        try:
            scraper.mongo.clear_collection(username)
            return redirect(url_for('clear_collection_success', username=username))
        except Exception as e:
            logging.error(f"Error occurred: {str(e)}")
            return render_template('error.html', error="An error occurred while clearing the collection.")

    return render_template('clear_collection.html')

@app.route('/clear_collection_success', methods=['GET'])
def clear_collection_success():
    """
    Displays the success message after clearing the collection.
    """
    username = request.args.get('username')
    return render_template('clear_collection_success.html', message=username)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
