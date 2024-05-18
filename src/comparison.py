class Comparison:
    """
    class for comparing things.
    :param username1 (str)
    :param username2 (str)
    :param user1_data (dict)
    :param user2_data (dict)
    :return
    """

    def __init__(self, username1, username2, user1_data, user2_data):
        self.user1 = username1
        self.user2 = username2
        self.data1 = user1_data
        self.data2 = user2_data

    def compare_users(self):
        """
        function to compare the two users and the data given, these variables pull from the db not the cached data.
        :return:
        """
        if not self.data1:
            print(f"Data for user '{self.user1}' not found in the database.")
            return
        if not self.data2:
            print(f"Data for user '{self.user2}' not found in the database.")
            return

        contributions_user1 = int(self.data1['contributions_last_year'])
        contributions_user2 = int(self.data2['contributions_last_year'])
        scraped_data = [contributions_user1, contributions_user2]
        return scraped_data
        
