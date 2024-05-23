class Comparison:
    """
    Class for comparing user contributions data.

    Args:
        usernames (list): List of usernames to compare.
        user_data (list): List of data dictionaries corresponding to each username.
    """

    def __init__(self, usernames, user_data):
        if not isinstance(usernames, list) or not isinstance(user_data, list):
            raise TypeError("Both usernames and user_data should be lists.")
        if len(usernames) != len(user_data):
            raise ValueError("Usernames and user_data lists must be of the same length.")

        self.usernames = usernames
        self.user_data = user_data

    def compare_users(self):
        """
        Compare contributions of multiple users.

        Returns:
            list: A list containing contributions of all users.
        Raises:
            ValueError: If contributions data is not found for any user.
        """
        contributions = []

        for username, data in zip(self.usernames, self.user_data):
            if not data:
                raise ValueError(f"Data for user '{username}' not found in the database.")
            if 'contributions_last_year' not in data:
                raise ValueError(f"Contributions data for user '{username}' is missing 'contributions_last_year'.")

            contributions.append(int(data.get('contributions_last_year', 0)))

        return contributions
