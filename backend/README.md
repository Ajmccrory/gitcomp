# Gitcomp Backend

## Overview

The Gitcomp Backend is a Flask-based application designed to handle data scraping, storage, and comparison functionalities for GitHub user data. It serves as the backbone of the Gitcomp tool, providing APIs for scraping user data, comparing contributions, repositories, and generating user activity graphs.

## Functionality

### 1. Data Scraping
- **Route:** `/scrape`
- **Method:** GET, POST
- **Description:** Initiates the scraping process for GitHub user data.
- **Parameters:** GitHub usernames as input.

### 2. Data Checking
- **Route:** `/existing`
- **Method:** GET, POST
- **Description:** Checks if a user's data exists in the database.
- **Parameters:** GitHub username as input.

### 3. Data Clearing
- **Route:** `/clear`
- **Method:** DELETE
- **Description:** Clears a user's data from the database.
- **Parameters:** GitHub username as input.

### 4. Data Comparison
- **Route:** `/compare`
- **Method:** GET, POST
- **Description:** Compares contributions and repositories of multiple users.
- **Parameters:** List of GitHub usernames as input.

### 5. Similarity Comparison
- **Route** `/similarity`
- **Method:**GET, POST
- **Description:** Compares the similarity of multiple users repos to check for contributions.
- **Parameters:** List of GitHub usernames as input.

### 6. Graph Generation
- **Route:** `/graph`
- **Method:** GET, POST
- **Description:** Generates a user activity graph based on GitHub username.
- **Parameters:** GitHub username as input.

## Contributions

Contributions to the backend of Gitcomp are more than welcome, for more information on how to contribute navigate to [the contribution guidelines](../README.md#contribute)

## Return to main

For setup, and more information, return to [main folder README](../README.md)


