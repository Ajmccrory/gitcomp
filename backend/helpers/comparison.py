

class Comparison:
    """
    Class for comparing user contributions data.

    Attributes:
        usernames (list): List of usernames to compare.
        user_data (list): List of data dictionaries corresponding to each username.
    """

    def __init__(self, usernames, user_data):
        """
        Initialize Comparison class with usernames and corresponding data.

        Args:
            usernames (list): List of usernames to compare.
            user_data (list): List of data dictionaries corresponding to each username.
        """
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
            list*: A list containing contributions of all users.
        Raises:
            ValueError: If contributions data is not found for any user.
        """
        if not self.user_data:
            raise ValueError("No user data provided.")

        contributions = []
        for data in self.user_data:
            if not data or 'contributions_last_year' not in data:
                raise ValueError("Invalid user data format.")
            contributions.append(int(data['contributions_last_year']))

        return contributions


