# Gitcomp
## A GitHub User Data Scraper, Analyzer, and Compiler

## Overview

This web application scrapes GitHub user data and provides various analysis tools. It allows users to scrape data from GitHub profiles, check for existing data, clear user data, compare contributions, repositories, and create user activity graphs.

### Background

This was originally an open ended class project. After completing the class I decided to expand on the CLI tool I had originally created to run these functions. In building the app my goal was demonstrate my understanding of backend and frontend development methodlogies and production cycles.

## Table of Contents

1. [How to Use](#how-to-use)
2. [Setup for Devs](#setup-instructions-for-developers)
3. [Development Information](#development-information)
4. [Contribute to Gitcomp](#contribute)


## How to Use

### 1. Scrape User Data
- Enter the GitHub username(s) you want to scrape.
- Click the "Scrape Data" button to initiate the process.

### 2. Check If Data Was Already Scraped
- Enter the GitHub username to check if their data is already in the system.
- Click the "Check Data" button for a quick verification.

### 3. Clear User Data
- Enter the GitHub username whose data you want to clear.
- Confirm the action by clicking "Clear Data."

### 4. Compare Contributions of Multiple Users
- Enter the GitHub usernames you want to compare.
- Click "Compare Contributions" to see a side-by-side analysis.

### 5. Compare Repository Similarity
- Select repositories for comparison from the available list.
- Click "Compare Repositories" to visualize their similarities.

### 6. Create a Graph of a Specific User
- Enter the GitHub username to generate a user activity graph.
- View the graph to understand the user's activity over time.

## Setup Instructions (For Developers)

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/repo-name.git
   cd repo-name
    ```

2. **Install Dependencies**
* Backend(Flask):
    ```bash
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
* Frontend(React):
    ```bash
    cd frontend
    npm install
    ```

3. **Configure Enviornment Variablse**
* Create a `.env` file in the backend directory with the following:
```bash
# note this project is omptimized from MONGO Atlas usage for cloud services to work in production
MONGOURI=YOUR_MONGO_ATLAS_URI
```

4. **Run the Application**
* Backend(Flask):
```bash
flask run
```

*Frontend(React):
```bash
npm start
```

5. **Access the Application**
* Open your browser and navigate to 'http://localhost:5000' to access the application locally

## Development Information
### Technologies Used
* Containerization: Docker, Docker Compose
* CI/CD: Github Actions
* Deployment: AWS(EC2, S3, CloudFront)
* Frontend: More info on FrontEnd at [FE README](/frontend/READNE.md)
* Backend: More info on BackEnd at [BE README](/backend/README.md)

### Development Enviornment
* Ensure Python 3.x and Node.js are installed.
* Use Docker and Docker Compose for local development and testing.
* Set up GitHub Actions for continous integration and deployment

## Created By
* AJ McCrory
### Past verisons
* [gitcomp-code-v1.0.0](../../tree/app-version-1.0.0) from: 5.2.2024
* [gitcomp-code-v1.0.1](../../tree/app-version-1.0.1) from: 5.10.2024
* [gitcomp-code-v1.0.2](../../tree/app-version-1.0.2) from 5.23.2024

## License
This Project is licensed under the [MIT License](LICENSE).

## Contribute {#contribute}
Contributions to Gitcomp are more than welcome, as this was literally something I did in my free time. If you'd like to contribute, please follow these steps:
1. Fork the repo
2. Create a new branch for your feature or bug fix(`git checkout -b feature-name`)
3. Follow steps under [Setup for Devs](#setup-instructions-for-developers)
4. Commit your changes(`git commit -am 'Add new feature <brief feature description>`)
5. Push to the branch(`git push origin feature-name`)
6. Create a new Pull Request on GitHub
I appreciate any and all contributions and look forward to collaboration!
