"""
Comparison algorithm that compares user data and returns who has more contributions.
"""

def compare(username1, username2, user1_data, user2_data):
    if not user1_data:
        print(f"Data for user '{username1}' not found in the database.")
        return
    if not user2_data:
        print(f"Data for user '{username2}' not found in the database.")
        return

    contributions_user1 = user1_data['contributions_last_year']
    contributions_user2 = user2_data['contributions_last_year']

    if contributions_user1 > contributions_user2:
        print(f"{username1} has more contributions in the last year.")
    elif contributions_user2 > contributions_user1:
        print(f"{username2} has more contributions in the last year.")
    else:
        print(f"{username1} and {username2} have an equal number of contributions in the last year.")

