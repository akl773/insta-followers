#!/usr/bin/env python3
import os
import json
from pathlib import Path

from instagrapi import Client
from dotenv import load_dotenv
from instagrapi.types import UserShort

from Models.user import User

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
    def _extract_user(user_short: UserShort) -> dict:
        return {
            "id": user_short.pk,
            "username": user_short.username,
            "full_name": user_short.full_name,
            "profile_pic_url": str(user_short.profile_pic_url),
        }

    def retrieve_user_connections(self):
        user_id = str(self.client.user_id)

        # Fetch followers and following
        print("Fetching followers…")
        followers_dict = self.client.user_followers(user_id, amount=10)
        followers = [self._extract_user(user) for user in followers_dict.values()]
        print(f"Got {len(followers)} followers.")

        print("Fetching following…")
        following_dict = self.client.user_following(user_id, amount=10)
        following = [self._extract_user(user) for user in following_dict.values()]
        print(f"Got {len(following)} following.")

        return {"followers": followers, "following": following}

    @staticmethod
    def save_connections(state: dict, filename: str = "state.json"):
        with open(filename, "w") as f:
            json.dump(state, f, indent=2)
        print("Saved state.json")

    def run(self):
        state = self.retrieve_user_connections()
        self.save_connections(state)


if __name__ == "__main__":
    User
    # f = InstagramFollower()
    # f.run()
