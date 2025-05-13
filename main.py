"""
Instagram Follower Tracker
"""

import os
import json
import logging
from typing import Set, Dict, List, Optional, Union
from pathlib import Path
from datetime import datetime
import time

from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ClientError
from dotenv import load_dotenv


class InstagramFollowerTracker:
    """
    A class to track changes in Instagram followers and following lists.

    This class provides functionality to:
    - Authenticate with Instagram
    - Retrieve current followers and following
    - Compare with previous data
    - Generate reports on changes
    - Persist state between runs
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the tracker with configuration.

        Args:
            config_path: Path to configuration file (optional)
        """
        # Setup logging
        self._setup_logging()

        # Load configuration
        self.config = self._load_config(config_path)

        # Initialize client
        self.client = Client()
        self.client.delay_range = [1, 3]  # Add delay between API calls to avoid rate limiting

        # Initialize state variables
        self.user_id = None
        self.curr_followers = set()
        self.curr_following = set()
        self.old_followers = set()
        self.old_following = set()

        # State file path
        self.state_file = Path(self.config.get("state_file", "state.json"))

        self.logger.info("Instagram Follower Tracker initialized")

    def _setup_logging(self) -> None:
        """Configure logging for the application."""
        log_level = os.environ.get("LOG_LEVEL", "INFO")
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

        # Create logs directory if it doesn't exist
        Path("logs").mkdir(exist_ok=True)

        # Configure logging
        logging.basicConfig(
            level=getattr(logging, log_level),
            format=log_format,
            handlers=[
                logging.FileHandler(f"logs/tracker_{datetime.now().strftime('%Y%m%d')}.log"),
                logging.StreamHandler()
            ]
        )

        self.logger = logging.getLogger("instagram_tracker")

        # Reduce noise from third-party libraries
        logging.getLogger("instagrapi").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)

    def _load_config(self, config_path: Optional[str] = None) -> Dict:
        """
        Load configuration from environment variables or config file.

        Args:
            config_path: Path to configuration file (optional)

        Returns:
            Dict containing configuration
        """
        # Load environment variables from .env file if it exists
        load_dotenv()

        config = {}

        # Try to load from config file if provided
        if config_path:
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                self.logger.info(f"Loaded configuration from {config_path}")
            except Exception as e:
                self.logger.error(f"Failed to load config from {config_path}: {e}")

        # Override with or set from environment variables
        config["username"] = os.environ.get("INSTAGRAM_USERNAME", config.get("username"))
        config["password"] = os.environ.get("INSTAGRAM_PASSWORD", config.get("password"))
        config["state_file"] = os.environ.get("STATE_FILE", config.get("state_file", "state.json"))

        # Validate required config
        if not config.get("username") or not config.get("password"):
            self.logger.error("Missing required configuration: username and password")
            raise ValueError("Missing required configuration: username and password")

        return config

    def authenticate(self) -> bool:
        """
        Authenticate with Instagram.

        Returns:
            bool: True if authentication was successful, False otherwise
        """
        try:
            username = self.config["username"]
            password = self.config["password"]

            self.logger.info(f"Attempting to login as {username}")

            # Try to load session from file if it exists
            session_file = Path(f"{username}_session.json")
            if session_file.exists():
                self.logger.info("Found existing session, attempting to reuse")
                try:
                    self.client.load_settings(session_file)
                    self.client.get_timeline_feed()  # Test if session is valid
                    self.logger.info("Successfully reused existing session")
                except Exception as e:
                    self.logger.warning(f"Failed to reuse session: {e}")
                    # Fall back to regular login
                    self.client.login(username, password)
                    self.client.dump_settings(session_file)
            else:
                # Regular login
                self.client.login(username, password)
                self.client.dump_settings(session_file)

            # Get user ID
            self.user_id = self.client.user_id_from_username(username)
            self.logger.info(f"Authenticated successfully as {username} (ID: {self.user_id})")
            return True

        except Exception as e:
            self.logger.error(f"Authentication failed: {e}")
            return False

    def fetch_current_data(self) -> bool:
        """
        Fetch current followers and following data.

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.logger.info("Fetching current followers and following data")

            retry_attempts = 3
            for attempt in range(retry_attempts):
                try:
                    # Get followers with pagination to handle large accounts
                    followers = {}
                    followers_per_page = self.client.user_followers(self.user_id, amount=0)
                    followers.update(followers_per_page)
                    self.curr_followers = set(followers.keys())

                    # Get following with pagination
                    following = {}
                    following_per_page = self.client.user_following(self.user_id, amount=0)
                    following.update(following_per_page)
                    self.curr_following = set(following.keys())

                    break
                except (LoginRequired, ClientError) as e:
                    if attempt < retry_attempts - 1:
                        self.logger.warning(f"API error on attempt {attempt + 1}, retrying: {e}")
                        self.authenticate()
                        time.sleep(5)  # Wait before retry
                    else:
                        raise

            self.logger.info(f"Fetched {len(self.curr_followers)} followers and {len(self.curr_following)} following")
            return True

        except Exception as e:
            self.logger.error(f"Failed to fetch current data: {e}")
            return False

    def load_previous_state(self) -> bool:
        """
        Load previous state from file.

        Returns:
            bool: True if successful, False if no previous state
        """
        try:
            if self.state_file.exists():
                with open(self.state_file, 'r') as f:
                    prev = json.load(f)

                self.old_followers = set(prev.get("followers", []))
                self.old_following = set(prev.get("following", []))

                self.logger.info(f"Loaded previous state with {len(self.old_followers)} followers and {len(self.old_following)} following")
                return True
            else:
                self.logger.info("No previous state found, this appears to be the first run")
                return False

        except Exception as e:
            self.logger.error(f"Failed to load previous state: {e}")
            # Initialize with empty sets in case of error
            self.old_followers = set()
            self.old_following = set()
            return False

    def analyze_changes(self) -> Dict:
        """
        Analyze changes between current and previous state.

        Returns:
            Dict containing analysis results
        """
        lost_followers = self.old_followers - self.curr_followers
        new_followers = self.curr_followers - self.old_followers
        unfollowed_by_you = self.old_following - self.curr_following
        newly_followed = self.curr_following - self.old_following

        # Convert user IDs to usernames where possible
        lost_followers_info = self._get_usernames_for_ids(lost_followers)
        new_followers_info = self._get_usernames_for_ids(new_followers)
        unfollowed_by_you_info = self._get_usernames_for_ids(unfollowed_by_you)
        newly_followed_info = self._get_usernames_for_ids(newly_followed)

        self.logger.info(f"Analysis complete: {len(lost_followers)} lost, {len(new_followers)} new, "
                         f"{len(unfollowed_by_you)} unfollowed by you, {len(newly_followed)} newly followed")

        return {
            "lost_followers": lost_followers_info,
            "new_followers": new_followers_info,
            "unfollowed_by_you": unfollowed_by_you_info,
            "newly_followed": newly_followed_info,
            "total_followers": len(self.curr_followers),
            "total_following": len(self.curr_following)
        }

    def _get_usernames_for_ids(self, user_ids: Set[str]) -> List[Dict[str, str]]:
        """
        Convert user IDs to usernames.

        Args:
            user_ids: Set of user IDs

        Returns:
            List of dicts with user information
        """
        result = []
        for user_id in user_ids:
            try:
                user_info = self.client.user_info(user_id)
                result.append({
                    "id": user_id,
                    "username": user_info.username,
                    "full_name": user_info.full_name
                })
            except Exception as e:
                self.logger.warning(f"Couldn't get username for ID {user_id}: {e}")
                result.append({"id": user_id, "username": "unknown", "full_name": ""})

        return result

    def save_state(self) -> bool:
        """
        Save current state to file.

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            state = {
                "followers": list(self.curr_followers),
                "following": list(self.curr_following),
                "timestamp": datetime.now().isoformat()
            }

            # Create directory if it doesn't exist
            self.state_file.parent.mkdir(exist_ok=True)

            with open(self.state_file, 'w') as f:
                json.dump(state, f, indent=4)

            self.logger.info(f"State saved to {self.state_file}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to save state: {e}")
            return False

    def generate_report(self, changes: Dict) -> str:
        """
        Generate a human-readable report of changes.

        Args:
            changes: Dict containing change information

        Returns:
            str: Formatted report
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        report_lines = [f"Instagram Follower Report - {now}"]
        report_lines.append("-" * 50)

        if changes["lost_followers"]:
            report_lines.append("\nLost Followers:")
            for user in changes["lost_followers"]:
                report_lines.append(f"  - {user['username']} ({user['full_name']})")

        if changes["new_followers"]:
            report_lines.append("\nNew Followers:")
            for user in changes["new_followers"]:
                report_lines.append(f"  - {user['username']} ({user['full_name']})")

        if changes["unfollowed_by_you"]:
            report_lines.append("\nYou Unfollowed:")
            for user in changes["unfollowed_by_you"]:
                report_lines.append(f"  - {user['username']} ({user['full_name']})")

        if changes["newly_followed"]:
            report_lines.append("\nYou Started Following:")
            for user in changes["newly_followed"]:
                report_lines.append(f"  - {user['username']} ({user['full_name']})")

        report_lines.append("\nSummary:")
        report_lines.append(f"  Total Followers: {changes['total_followers']}")
        report_lines.append(f"  Total Following: {changes['total_following']}")

        return "\n".join(report_lines)

    def run(self) -> Union[str, None]:
        """
        Execute the full tracking workflow.

        Returns:
            str: Report if successful, None otherwise
        """
        try:
            # Step 1: Authenticate
            if not self.authenticate():
                return None

            # Step 2: Load previous state
            self.load_previous_state()

            # Step 3: Fetch current data
            if not self.fetch_current_data():
                return None

            # Step 4: Analyze changes
            changes = self.analyze_changes()

            # Step 5: Save current state
            self.save_state()

            # Step 6: Generate report
            report = self.generate_report(changes)
            print(report)

            # Optionally save report to file
            report_file = Path(f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt")
            report_file.parent.mkdir(exist_ok=True)
            with open(report_file, 'w') as f:
                f.write(report)

            return report

        except Exception as e:
            self.logger.error(f"Error during execution: {e}", exc_info=True)
            return None


if __name__ == "__main__":
    # Create and run the tracker
    try:
        # You can specify a config file path or rely on environment variables
        # tracker = InstagramFollowerTracker("config.json")
        tracker = InstagramFollowerTracker()
        tracker.run()
    except Exception as e:
        logging.error(f"Unhandled exception: {e}", exc_info=True)