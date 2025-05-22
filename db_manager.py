import os

from dotenv import load_dotenv
from pymongo import MongoClient


class DBManager:
    """Handles MongoDB operations."""

    _instance = None

    def __init__(
            self,
            mongo_uri: str | None = None,
            db_name: str | None = None
    ):
        """Initializes the main application class."""
        self.db = None
        self.client = None

        print(f"🚀 DB Manager started")
        self.setup_mongodb(mongo_uri, db_name)

    def get_instance(self):
        if DBManager._instance is not None:
            return self.db

        self.setup_mongodb()
        return self.get_instance()

    def setup_mongodb(
            self,
            mongo_uri: str | None = None,
            db_name: str | None = None
    ):
        """Connect to MongoDB."""
        load_dotenv()
        # Use defaults if env vars are missing
        mongo_uri = mongo_uri or os.getenv("MONGO_URI", "mongodb://localhost:27017")
        db_name = db_name or os.getenv("DATABASE_NAME", "InstagramStat")
        try:
            self.client = MongoClient(mongo_uri)
            self.db = self.client[db_name]
            DBManager._instance = self
            print(f"Connected to database: {db_name} @ {mongo_uri[:5]}...")
        except Exception as e:
            print(f"Failed to connect to MongoDB at {mongo_uri}: {e}")
            raise
