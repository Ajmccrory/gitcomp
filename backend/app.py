# RestfulAPI
from flask import Flask, request, jsonify, redirect, url_for, send_from_directory
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from git_scraper.git_scraper import GithubScraper
from config.config import Config
import base64
import matplotlib
import matplotlib.pyplot as plt
import io
import logging
import uuid


matplotlib.use('Agg')  # Use a non-interactive backend
app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
mongo_uri = app.config['MONGO_URI']
scraper = GithubScraper(mongo_uri)
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

    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)

    file_id = scraper.mongo.save_image(img_bytes, f'bar_char_{uuid.uuid4().hex}.png')
    return file_id

def create_graph(data, user_data):
    username = user_data['username']
    user_contributions = user_data['user_contributions']
    num_repos = len(user_data['repositories'])

    fig, ax = plt.subplots()

    bars = ax.bar(['Contributions', 'Repositories'], [user_contributions, num_repos], color=['blue', 'green'])

    ax.set_title(f'Github User Data for {username}')
    ax.set_ylabel('Count')

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom')

    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)

    img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')

    return img_base64


# Custom filter for base64 encoding
def b64encode_filter(data):
    return base64.b64encode(data).decode('utf-8')


# Register the custom filter with Flask
app.jinja_env.filters['b64encode'] = b64encode_filter


@app.route('/compare', methods=['POST'])
def compare():
    """
    Handles the comparison of user contributions.
    If the request method is POST, it scrapes data for the provided usernames and generates a comparison chart.
    """
    data = request.json
    usernames = data.get('usernames')
    if not usernames or len(usernames) < 2 or len(usernames) > 4:
        return jsonify({"error": "Please provide 2 to 4 usernames. "}), 400
    
    try:
        for user in usernames:
            scraper.scrape_user_data(user)

        contributions = scraper.get_users_contributions(usernames)
        plot_id = compile_data(contributions, usernames)
        return jsonify({"plot_id": plot_id}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        error_message = f'An error occurred during comparison. {str(e)}'
        return jsonify({"error": error_message}), 500

@app.route('/display_comparison', methods=['GET'])
def display_comparison():
    plot_id = request.args.get('plot_id')
    if not plot_id:
        return jsonify({"error": "No plot ID provided"}), 400
    try:
        image_data = scraper.mongo.get_image(plot_id)
        return jsonify({"plot_data": image_data}), 200
    except Exception as e:
        return jsonify({"error": f"An error occured while retrieving the image: {str(e)}"}), 500
    
@app.route('/scrape', methods=['POST'])
def scrape_user_data():
    """
    Scrapes user data from GitHub.
    If the request method is POST, it scrapes data for the provided username.
    """
    data = request.json
    username = data.get('username')
    if not username:
        return jsonify({"error": "Please provide a username."}), 400
    
    try:
        scraper.scrape_user_data(username)
        return redirect(url_for('show_scraped_data', data=data))
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}, 500)

@app.route('/scraped_user', methods=['POST'])
def show_scraped_data():
    """
    Displays the scraped data for the given username.
    """
    data = request.json
    username = data.get('username')
    if not username:
        return jsonify({"error": "username not provided"}), 400
    
    try:
        repos = scraper.get_repos(username)
        return jsonify({"username": username, "repos": repos}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/existing', methods=['POST'])
def check_user_exists():
    """
    Checks if the user exists in the database.
    If the request method is POST, it checks for the provided username.
    """
    data = request.json
    username = data.get('username')
    if not username:
        return jsonify({"error": "Please provide a username"}), 400
    
    user_data = scraper.mongo.find_one({'username': username})
    if user_data:
        return jsonify({"user_data": user_data}), 200
    else:
        return jsonify({"error": "User not found in the database."})

@app.route('/clear', methods=['POST'])
def clear_mongo_collection():
    """
    Clears the MongoDB collection for the given username.
    If the request method is POST, it clears data for the provided username.
    """
    data = request.json
    username = data.get('username')
    if not username:
        return jsonify({"error": "Please provide a username."}), 400
    
    try:
        scraper.mongo.clear_collection(username)
        return jsonify("Collection cleared successsfully."), 200
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify("An error occurred while clearing the collection"), 500

@app.route('/similarity', methods=['POST'])
def check_repo_similarity():
    """
    Runs a check to compare the similarity of multiple users
    accounts to show contributions in matching repositories.
    """
    data = request.json
    usernames = data.get('usernames')
    if not usernames or len(usernames) < 2 or len(usernames) > 4:
        return jsonify({"error": "Please provide anywhere from 2 to 4 usernames."}), 400
    
    try:
        similarities = scraper.get_similarity(usernames)
        return jsonify({"similarities": similarities}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred {str(e)}"}), 500

@app.route('/display_similarity', methods=['GET'])
def display_repo_similarity():
    """
    Displays the similarity between the repos of the compared users.
    """
    similarities = request.args.get('similarities')
    #  Similarities - A dictionary where keys are repo names and vals are lists of usernames that have that repo
    if not similarities:
        return jsonify({"error": "similarities info not provided."}), 400
    return jsonify({"similarities": similarities}), 200

@app.route('/graph', methods=['POST'])
def compile_graph():
    """
    Compiles user information into a graph that is saved with the user id's
    within a list in a MongoDB collection.
    """
    data = request.json
    usernames = data.get('usernames')
    if not usernames or len(usernames) < 2 or len(usernames) > 4:
        return jsonify({"error": "Please provide 2 to 4 usernames."}), 400
    
    try:
        user_data = [scraper.get_user_data(user) for user in usernames]
        graph = create_graph(user_data)
        graph_id = scraper.mongo.save_image(graph, f'user_graph_{uuid.uuid4().hex}.png')
        return jsonify({"graph_id": graph_id}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/display_graph', methods=['GET'])
def display_graph():
    """
    Display the graph of compiled user data for a single user.
    """
    graph_id = request.args.get('graph_id')
    if not graph_id:
        return jsonify({"error": 'graph id not provided.'}), 400
    try:
        image_data = scraper.mongo.get_image(graph_id)
        return jsonify({"graph_id": image_data}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred in displaying the graph: {str(e)}"}), 500

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Gitcomp"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
