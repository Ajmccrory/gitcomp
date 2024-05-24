## Gitcomp Frontend

The Gitcomp Frontend is built using React and Context API, providing a user-friendly interface for interacting with the Gitcomp Backend APIs. It allows users to perform various actions such as scraping GitHub user data, checking data, clearing user data, comparing contributions, and repositories, and generating user activity graphs.

## Functionality

### 1. User Interface
- **Scrape Data:** Input GitHub username(s) and initiate data scraping.
- **Check Data:** Verify if a user's data exists in the system.
- **Clear Data:** Remove a user's data from the database.
- **Compare Contributions:** Compare contributions of multiple users.
- **Compare Repositories:** Visualize similarities between repositories.
- **Generate Graph:** Create user activity graphs for analysis.

### 2. Context API Integration
- **Global State Management:** Manage application state using React Context API.
- **Shared Data:** Share data and functions across components efficiently.
- **Dynamic Updates:** Update UI components dynamically based on state changes.

## Setup Instructions

1. Clone the Gitcomp Frontend repository:
   ```bash
   git clone https://github.com/Ajmccrory/gitcomp-frontend.git
   cd gitcomp-frontend
   ```
2. Install dependencies using npm:
    ```bash
    npm install
    ```
3. Configure Environment Variables
* Ensure the backend API endpoint is correctly set in `src/config.js`
* For more on setup navigate to [setup for developers](../README.md#setup-instructions-for-developers-setup-instructions)
4. Run the Application Locally
    ```bash
    npm start
    ```
5. Access the application
* Open your browser and navigate to `http://localhost:5000` to access the frontend of gitcomp.

## Development Information
### Technologies Used
* React: JavaScript library for building UI's.
* Context API: React's state management system for global state.
* Axios: HTTP client for making API requests to the backend.
* Chart.js: Library used for creating interactive charts and graphs.

### Folder Structure
* src/components: React components for different functionalities.
* src/context: Context providers and consumers for state management.
* src/services: Service files for API calls and data handling.
* src/config.js: Configuration file for API endpoints and other constants.

## Contribute
Contributions to the frontend are more than welcome, If you'd like to commit follow the steps in the [contribute](../README.md#contribute-contribute)

## Return to main

For setup, and more information, return to [main folder README](../README.md)
