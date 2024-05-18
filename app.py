from flask import Flask, request, render_template
from git_scraper.git_scraper import GithubScraper
import matplotlib.pyplot as plt

app = Flask(__name__)
scraper = GithubScraper()

def compiled_data(scraped_data, user1, user2):
    if len(scraped_data) < 2:
        raise ValueError("There are no saved values being imported from comparrison.py")
    # Define the two integers
    int1 = scraped_data[0]
    int2 = scraped_data[1]

    # Create a new figure
    plt.figure()

    # Plot horizontal lines for the two integers
    plt.axhline(y=int1, color='blue', linestyle='--', linewidth=2, label=f'user:{user1}{int1}')
    plt.axhline(y=int2, color='green', linestyle='-', linewidth=2, label=f'user:{user2}{int2}')

    # Add titles and labels
    plt.title('Graph of user contributions')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')

    # Add a legend
    plt.legend()

    # Set limits for the axes for better visibility
    plt.ylim(0, 10)
    plt.xlim(-1, 1)

    # Save the plot as a file
    plt.savefig('static/graph.png')  # Save the plot as a file in the static folder
    # make this display in a redirect window

@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        user1 = request.form['user1']
        user2 = request.form['user2']
        scraped = scraper.compare_users_contributions(user1, user2)
        compiled_data(scraped, user1, user2)  # Call the compiled_data function
        return render_template('base.html')
    return render_template('base.html')

@app.route('/scrape', methods=['GET', 'POST'])
def scrape_user_data():
    if request.method == 'POST':
        repos = request.form['repos']
        repos = scraper.get_repos(repos)
        return render_template('scraping.html', repos=repos)

@app.route('/existing', methods=['GET', 'POST'])
def check_user_exists():
    return render_template('existing_user.html')

@app.route('/clear', methods=['GET', 'POST'])
def clear_mongo_collection():
    return render_template('clear_collection.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)