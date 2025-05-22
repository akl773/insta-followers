import os
import json
from pathlib import Path

from instagrapi import Client
from dotenv import load_dotenv
from instagrapi.types import UserShort

from Models.report import Report
from Models.user import User
from utils.time import get_morning_time

load_dotenv()


class InstagramFollower:

    def __init__(self):
        self.client = self.initialise()
        self.dry_run = True
        self.amount = 0 if not self.dry_run else 10

    @staticmethod
    def initialise():
        username = os.getenv("INSTAGRAM_USERNAME")
        password = os.getenv("INSTAGRAM_PASSWORD")
        if not username or not password:
            print("Error: set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD in .env")
            exit(1)

        client = Client()
        session_file = Path(f"session/{username}_session.json")
        session_file.parent.mkdir(exist_ok=True)

        # Reuse session if available, else login
        if session_file.exists():
            print("Loading existing session…")
            try:
                client.load_settings(session_file)
                client.user_following(str(client.user_id), amount=1)
            except Exception as se:
                print(f"Session loading failed: {se}. Logging in again...")
                client.login(username, password)
                client.dump_settings(session_file)
        else:
            print("Logging in…")
            client.login(username, password)
            client.dump_settings(session_file)
            print("Session saved.")

        return client

    @staticmethod
    def _extract_user(user_short: UserShort) -> User:
        return User(
            _id=user_short.pk,
            username=user_short.username,
            full_name=user_short.full_name,
            profile_pic_url=str(user_short.profile_pic_url),
        )

    def get_followers(self):
        user_id = str(self.client.user_id)

        # Fetch followers
        print("Fetching followers…")
        followers_dict = self.client.user_followers(user_id, amount=self.amount)
        followers = [self._extract_user(user) for user in followers_dict.values()]
        print(f"Got {len(followers)} followers.")

        return followers

    def get_following(self):
        user_id = str(self.client.user_id)

        # Fetch following
        print("Fetching following…")
        following_dict = self.client.user_following(user_id, amount=self.amount)
        following = [self._extract_user(user) for user in following_dict.values()]
        print(f"Got {len(following)} following.")

        return following

    @staticmethod
    def save_connections(state: dict, filename: str = "state.json"):
        with open(filename, "w") as f:
            json.dump(state, f, indent=2)
        print("Saved state.json")

    @staticmethod
    def extract_ids_by_type(report_obj, user_type):
        """Extract user IDs of a specific type from a report."""
        return {user.get('id') for user in report_obj.users
                if user.get('id') and user_type in user.get('type', [])}

    @staticmethod
    def get_user_details(report_list, user_ids):
        """Get user details for a list of user IDs from reports."""
        for report in report_list:
            if not report:
                continue
            users_found = [user for user in report.users if user.get('id') in user_ids]
            if users_found:
                return users_found
        return []

    @staticmethod
    def print_diff_section(title, emoji, users):
        """Print a section of the difference report."""
        print(f"\n{emoji} {title} ({len(users)}):")
        for user in users:
            print(f"  - @{user.get('username', 'unknown')} ({user.get('full_name', '')})")

    @staticmethod
    def generate_report(followers: list[User], following: list[User]):
        """
        Generate a report containing follower and following information.
        Categorizes each user as follower, following, or both.
        """
        # Get sets of IDs for efficient operations
        follower_ids = {user.id for user in followers}
        following_ids = {user.id for user in following}

        # Create a dictionary to deduplicate users
        unique_users = {}

        # Process all users
        for user in followers + following:
            user_id = user.id
            if user_id not in unique_users:
                user_dict = user.get_dict()
                user_dict['type'] = []
                unique_users[user_id] = user_dict

            # Add type information
            if user_id in follower_ids and 'follower' not in unique_users[user_id]['type']:
                unique_users[user_id]['type'].append('follower')
            if user_id in following_ids and 'following' not in unique_users[user_id]['type']:
                unique_users[user_id]['type'].append('following')

        # Create the report
        report = Report(
            generated_at=get_morning_time(),
            num_followers=len(followers),
            num_following=len(following),
            users=list(unique_users.values()),
        )
        report.save()
        return report

    @staticmethod
    def previous_generated_report():
        return Report.find_one({}, sort=[("generated_at", -1)])

    @staticmethod
    def analyse_reports(report: Report, last_report: Report):
        """Analyze the differences between the current report and the previous report."""
        if not last_report:
            print("This is the first report - no comparison available.")
            return

        # Calculate differences using the helper methods
        current_followers = report.get_user_ids_by_type('follower')
        current_following = report.get_user_ids_by_type('following')
        previous_followers = last_report.get_user_ids_by_type('follower')
        previous_following = last_report.get_user_ids_by_type('following')

        # Calculate differences
        new_followers = current_followers - previous_followers
        lost_followers = previous_followers - current_followers
        new_following = current_following - previous_following
        unfollowed = previous_following - current_following

        # Update report with results
        report.new_followers = list(new_followers)
        report.lost_followers = list(lost_followers)
        report.new_following = list(new_following)
        report.unfollowed = list(unfollowed)

    def run(self):
        current_dt = get_morning_time()
        existing_report = Report.find_one({"generated_at": current_dt})

        if existing_report:
            print(f"Report already generated for {current_dt}.")
            return

        # Get followers and following
        followers: list[User] = self.get_followers()
        following: list[User] = self.get_following()

        # Update user collection
        User().update_many(followers + following)

        # Get a previous report for comparison
        last_report = self.previous_generated_report()

        # Generate a new report
        report = self.generate_report(followers, following)

        # Analyze and update a report with comparison data
        if last_report:
            self.analyse_reports(report, last_report)
        else:
            print("This is the first report - no comparison data available.")


if __name__ == "__main__":
    try:
        f = InstagramFollower()
        f.run()
        print("\nDone! Instagram follower analysis complete.")
    except Exception as e:
        print(f"\nError: {e}")
