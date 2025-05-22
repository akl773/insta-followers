import json
import os
import time
from pathlib import Path
from typing import List

from colorama import init, Fore, Style
from dotenv import load_dotenv
from instagrapi import Client
from instagrapi.types import UserShort

from Models.report import Report
from Models.user import User
from utils.time import get_morning_time

init()

load_dotenv()


class InstagramFollower:

    def __init__(self):
        print(f"{Fore.CYAN}╔══════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║     Instagram Follower Analyzer      ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚══════════════════════════════════════╝{Style.RESET_ALL}")

        self.start_time = time.time()
        self.client = self.initialise()
        self.dry_run = os.getenv("DRY_RUN", "false").lower() in ('true', 'yes', '1', 'y')
        self.force_run = os.getenv("FORCE_RUN", "false").lower() in ('true', 'yes', '1', 'y')

        if self.dry_run:
            print(f"{Fore.YELLOW}⚠️  DRY RUN MODE ENABLED - Limited to 10 users{Style.RESET_ALL}")
        if self.force_run:
            print(f"{Fore.YELLOW}⚠️  FORCE RUN MODE ENABLED - Will regenerate today's report{Style.RESET_ALL}")

        self.amount = 0 if not self.dry_run else 10

    @staticmethod
    def initialise():
        username = os.getenv("INSTAGRAM_USERNAME")
        password = os.getenv("INSTAGRAM_PASSWORD")
        if not username or not password:
            print(
                f"{Fore.RED}Error: INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD must be set in .env file{Style.RESET_ALL}")
            exit(1)

        client = Client()
        session_file = Path(f"session/{username}_session.json")
        session_file.parent.mkdir(exist_ok=True)

        # Reuse session if available, else login
        if session_file.exists():
            print(f"{Fore.BLUE}🔑 Loading existing session for @{username}...{Style.RESET_ALL}")
            try:
                client.load_settings(session_file)
                client.user_following(str(client.user_id), amount=1)
                print(f"{Fore.GREEN}✅ Session loaded successfully{Style.RESET_ALL}")
            except Exception as se:
                print(f"{Fore.RED}❌ Session loading failed: {se}{Style.RESET_ALL}")
                print(f"{Fore.BLUE}🔑 Logging in to Instagram...{Style.RESET_ALL}")
                client.login(username, password)
                client.dump_settings(session_file)
                print(f"{Fore.GREEN}✅ New session saved{Style.RESET_ALL}")
        else:
            print(f"{Fore.BLUE}🔑 First-time login to Instagram...{Style.RESET_ALL}")
            client.login(username, password)
            client.dump_settings(session_file)
            print(f"{Fore.GREEN}✅ Session saved successfully{Style.RESET_ALL}")

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
        print(f"\n{Fore.BLUE}📥 Fetching followers...{Style.RESET_ALL}")
        start_time = time.time()
        followers_dict = self.client.user_followers(user_id, amount=self.amount)
        followers = [self._extract_user(user) for user in followers_dict.values()]
        duration = time.time() - start_time

        print(
            f"{Fore.GREEN}✅ Retrieved {Fore.YELLOW}{len(followers)}{Fore.GREEN} followers in {Fore.YELLOW}{duration:.2f}{Fore.GREEN} seconds{Style.RESET_ALL}")

        return followers

    def get_following(self):
        user_id = str(self.client.user_id)

        # Fetch following
        print(f"\n{Fore.BLUE}📤 Fetching following...{Style.RESET_ALL}")
        start_time = time.time()
        following_dict = self.client.user_following(user_id, amount=self.amount)
        following = [self._extract_user(user) for user in following_dict.values()]
        duration = time.time() - start_time

        print(
            f"{Fore.GREEN}✅ Retrieved {Fore.YELLOW}{len(following)}{Fore.GREEN} following in {Fore.YELLOW}{duration:.2f}{Fore.GREEN} seconds{Style.RESET_ALL}")

        return following

    @staticmethod
    def save_connections(state: dict, filename: str = "state.json"):
        with open(filename, "w") as f:
            json.dump(state, f, indent=2)
        print(f"{Fore.GREEN}✅ Saved state to {filename}{Style.RESET_ALL}")

    @staticmethod
    def generate_report(followers: List[User], following: List[User]):
        """
        Generate a report containing follower and following information.
        Categorizes each user as a follower, following, or both.
        """
        print(f"\n{Fore.BLUE}📊 Generating report...{Style.RESET_ALL}")
        start_time = time.time()

        # Get sets of IDs for efficient operations
        follower_ids = {user.id for user in followers}
        following_ids = {user.id for user in following}

        # Get counts of different relationship types
        mutual_count = len(follower_ids.intersection(following_ids))
        followers_only = len(follower_ids - following_ids)
        following_only = len(following_ids - follower_ids)

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

        duration = time.time() - start_time

        # Print report summary
        print(f"{Fore.GREEN}✅ Report generated in {Fore.YELLOW}{duration:.2f}{Fore.GREEN} seconds{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}┌─────────────── Report Summary ───────────────┐{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Style.RESET_ALL} Date: {report.generated_at.strftime('%Y-%m-%d')}")
        print(f"{Fore.CYAN}│{Style.RESET_ALL} Total Followers: {Fore.YELLOW}{len(followers)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Style.RESET_ALL} Total Following: {Fore.YELLOW}{len(following)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Style.RESET_ALL} Mutual Connections: {Fore.GREEN}{mutual_count}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Style.RESET_ALL} Followers Only: {Fore.BLUE}{followers_only}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Style.RESET_ALL} Following Only: {Fore.MAGENTA}{following_only}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}└──────────────────────────────────────────────┘{Style.RESET_ALL}")

        return report

    @staticmethod
    def previous_generated_report():
        return Report.find_one({}, sort=[("generated_at", -1)])

    @staticmethod
    def analyse_reports(report: Report, last_report: Report):
        """Analyze the differences between the current report and the previous report."""
        if not last_report:
            print(f"{Fore.YELLOW}ℹ️ This is the first report - no comparison available.{Style.RESET_ALL}")
            return

        print(
            f"\n{Fore.BLUE}🔍 Analyzing changes since last report ({last_report.generated_at.strftime('%Y-%m-%d')})...{Style.RESET_ALL}")

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

        # Create stats dictionary
        report.stats = {
            "new_followers_count": len(new_followers),
            "lost_followers_count": len(lost_followers),
            "new_following_count": len(new_following),
            "unfollowed_count": len(unfollowed),
            "net_follower_change": len(new_followers) - len(lost_followers),
            "net_following_change": len(new_following) - len(unfollowed),
            "previous_report_date": last_report.generated_at.strftime('%Y-%m-%d')
        }

        # Save updated report
        report.save()

        # Print analysis
        print(f"\n{Fore.CYAN}┌─────────────── Changes Analysis ───────────────┐{Style.RESET_ALL}")

        # New followers
        if new_followers:
            print(f"{Fore.CYAN}│{Style.RESET_ALL} {Fore.GREEN}📈 New Followers: {len(new_followers)}{Style.RESET_ALL}")
            for i, user_id in enumerate(new_followers, 1):
                user = report.get_user_by_id(user_id)
                if user:
                    print(
                        f"{Fore.CYAN}│{Style.RESET_ALL}   {i}. @{user.get('username', 'unknown')} ({user.get('full_name', '')})")
                if i >= 5 and len(new_followers) > 5:
                    print(f"{Fore.CYAN}│{Style.RESET_ALL}   ... and {len(new_followers) - 5} more")
                    break
        else:
            print(f"{Fore.CYAN}│{Style.RESET_ALL} {Fore.YELLOW}📈 No new followers{Style.RESET_ALL}")

        # Lost followers
        if lost_followers:
            print(f"{Fore.CYAN}│{Style.RESET_ALL} {Fore.RED}📉 Lost Followers: {len(lost_followers)}{Style.RESET_ALL}")
            for i, user_id in enumerate(lost_followers, 1):
                user = last_report.get_user_by_id(user_id)
                if user:
                    print(
                        f"{Fore.CYAN}│{Style.RESET_ALL}   {i}. @{user.get('username', 'unknown')} ({user.get('full_name', '')})")
                if i >= 5 and len(lost_followers) > 5:
                    print(f"{Fore.CYAN}│{Style.RESET_ALL}   ... and {len(lost_followers) - 5} more")
                    break
        else:
            print(f"{Fore.CYAN}│{Style.RESET_ALL} {Fore.YELLOW}📉 No lost followers{Style.RESET_ALL}")

        # New following
        if new_following:
            print(f"{Fore.CYAN}│{Style.RESET_ALL} {Fore.GREEN}➕ New Following: {len(new_following)}{Style.RESET_ALL}")
            for i, user_id in enumerate(new_following, 1):
                user = report.get_user_by_id(user_id)
                if user:
                    print(
                        f"{Fore.CYAN}│{Style.RESET_ALL}   {i}. @{user.get('username', 'unknown')} ({user.get('full_name', '')})")
                if i >= 5 and len(new_following) > 5:
                    print(f"{Fore.CYAN}│{Style.RESET_ALL}   ... and {len(new_following) - 5} more")
                    break
        else:
            print(f"{Fore.CYAN}│{Style.RESET_ALL} {Fore.YELLOW}➕ No new following{Style.RESET_ALL}")

        # Unfollowed
        if unfollowed:
            print(f"{Fore.CYAN}│{Style.RESET_ALL} {Fore.RED}➖ Unfollowed: {len(unfollowed)}{Style.RESET_ALL}")
            for i, user_id in enumerate(unfollowed, 1):
                user = last_report.get_user_by_id(user_id)
                if user:
                    print(
                        f"{Fore.CYAN}│{Style.RESET_ALL}   {i}. @{user.get('username', 'unknown')} ({user.get('full_name', '')})")
                if i >= 5 and len(unfollowed) > 5:
                    print(f"{Fore.CYAN}│{Style.RESET_ALL}   ... and {len(unfollowed) - 5} more")
                    break
        else:
            print(f"{Fore.CYAN}│{Style.RESET_ALL} {Fore.YELLOW}➖ No unfollowed users{Style.RESET_ALL}")

        # Net changes
        net_follower_change = len(new_followers) - len(lost_followers)
        net_following_change = len(new_following) - len(unfollowed)

        if net_follower_change > 0:
            print(
                f"{Fore.CYAN}│{Style.RESET_ALL} {Fore.GREEN}📊 Net follower change: +{net_follower_change}{Style.RESET_ALL}")
        elif net_follower_change < 0:
            print(
                f"{Fore.CYAN}│{Style.RESET_ALL} {Fore.RED}📊 Net follower change: {net_follower_change}{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}│{Style.RESET_ALL} {Fore.YELLOW}📊 Net follower change: 0{Style.RESET_ALL}")

        if net_following_change > 0:
            print(
                f"{Fore.CYAN}│{Style.RESET_ALL} {Fore.GREEN}📊 Net following change: +{net_following_change}{Style.RESET_ALL}")
        elif net_following_change < 0:
            print(
                f"{Fore.CYAN}│{Style.RESET_ALL} {Fore.RED}📊 Net following change: {net_following_change}{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}│{Style.RESET_ALL} {Fore.YELLOW}📊 Net following change: 0{Style.RESET_ALL}")

        print(f"{Fore.CYAN}└───────────────────────────────────────────────┘{Style.RESET_ALL}")

    def run(self):
        current_dt = get_morning_time()
        existing_report = Report.find_one({"generated_at": current_dt})

        if existing_report and not self.force_run and not self.dry_run:
            print(f"\n{Fore.YELLOW}ℹ️ Report already exists for {current_dt.strftime('%Y-%m-%d')}.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}ℹ️ Use FORCE_RUN=true to regenerate the report.{Style.RESET_ALL}")
            return

        # Get followers and following
        followers: List[User] = self.get_followers()
        following: List[User] = self.get_following()

        # Update user collection
        print(f"\n{Fore.BLUE}💾 Updating user database...{Style.RESET_ALL}")
        User.update_many(followers + following)
        print(f"{Fore.GREEN}✅ User database updated with {len(followers) + len(following)} entries{Style.RESET_ALL}")

        # Get a previous report for comparison
        last_report = self.previous_generated_report()

        # Generate a new report
        report = self.generate_report(followers, following)

        # Analyze and update a report with comparison data
        if last_report:
            self.analyse_reports(report, last_report)
        else:
            print(f"\n{Fore.YELLOW}ℹ️ This is the first report - no comparison data available.{Style.RESET_ALL}")

        # Calculate total runtime
        total_time = time.time() - self.start_time
        print(
            f"\n{Fore.GREEN}✅ Done! Analysis completed in {Fore.YELLOW}{total_time:.2f}{Fore.GREEN} seconds{Style.RESET_ALL}")


if __name__ == "__main__":
    try:
        f = InstagramFollower()
        f.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️ Process interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
        raise  # Remove this in production if you don't want stack traces
