#!/usr/bin/env python3
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
                # Optional: Add a simple verification that the session is still valid
                client.user_info_by_username(username)  # A simple API call to test
            except Exception as e:
                print(f"Session loading failed: {e}. Logging in again...")
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

        # Fetch followers and following
        print("Fetching followers…")
        followers_dict = self.client.user_followers(user_id, amount=0)
        followers = [self._extract_user(user) for user in followers_dict.values()]
        print(f"Got {len(followers)} followers.")

        return followers

    def get_following(self):
        user_id = str(self.client.user_id)

        print("Fetching following…")
        following_dict = self.client.user_following(user_id, amount=0)
        following = [self._extract_user(user) for user in following_dict.values()]
        print(f"Got {len(following)} following.")

        return following

    @staticmethod
    def save_connections(state: dict, filename: str = "state.json"):
        with open(filename, "w") as f:
            json.dump(state, f, indent=2)
        print("Saved state.json")

    @staticmethod
    def generate_report(followers: list[User], following: list[User]):
        report = Report(
            generated_at=get_morning_time(),
            num_followers=len(followers),
            num_following=len(following),
            users=[user.get_dict() for user in followers + following],
        )
        report.save()

    def run(self):
        current_dt = get_morning_time()
        if Report.find_one({"generated_at": current_dt}):
            print("Report already generated for today.")
            return

        followers: list[User] = self.get_followers()
        following: list[User] = self.get_following()
        User.update_many(followers + following)
        self.generate_report(followers, following)


if __name__ == "__main__":
    f = InstagramFollower()
    f.run()
