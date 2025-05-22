#!/usr/bin/env python3
import os
import json
from pathlib import Path

from instagrapi import Client
from dotenv import load_dotenv

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
            client.load_settings(session_file)
        else:
            print("Logging in…")
            client.login(username, password)
            client.dump_settings(session_file)
            print("Session saved.")

        return client

    def retrieve_user_connections(self):
        client = self.client
        user_id = str(client.user_id)

        # Fetch followers and following
        print("Fetching followers…")
        followers = list(client.user_followers(user_id, amount=0).keys())
        print(f"Got {len(followers)} followers.")
        print("Fetching following…")
        following = list(client.user_following(user_id, amount=0).keys())
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
    f = InstagramFollower()
    f.run()
