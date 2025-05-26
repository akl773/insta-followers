# Instagram Follower Analyzer

A Python-based tool that helps you analyze and track your Instagram followers and following relationships. This tool provides detailed insights into your Instagram network, including follower changes, mutual connections, and relationship statistics.

## Features

- 🔍 Track followers and following relationships
- 📊 Generate daily reports of your Instagram network
- 📈 Monitor follower/following changes over time
- 🤝 Identify mutual connections
- 💾 Store historical data in MongoDB
- 🎨 Beautiful terminal-based UI with color-coded output
- 🔐 Secure session management for Instagram authentication

## Prerequisites

- Python 3.7+
- MongoDB (local or remote)
- Instagram account credentials

## Installation

1. Clone the repository:
```bash
git clone https://github.com/akl773/instagramFollowers.git
cd instagramFollowers
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with the following variables:
```env
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password
MONGO_URI=mongodb://localhost:27017  # Or your MongoDB connection string
DATABASE_NAME=InstagramStat
DRY_RUN=false  # Set to true for testing with limited data
FORCE_RUN=false  # Set to true to regenerate today's report
PRINT_QUERY_TIME=false  # Set to true to see query execution times
```

## Usage

Run the analyzer:
```bash
python main.py
```

The tool will:
1. Authenticate with Instagram
2. Fetch your current followers and following
3. Generate a daily report
4. Compare with previous reports to show changes
5. Display a summary of your Instagram network

### Report Features

- Total followers and following counts
- Mutual connections
- New followers and lost followers
- New following and unfollowed accounts
- Net changes in followers and following
- Detailed user information including usernames and profile pictures

## Project Structure

```
instagramFollowers/
├── main.py              # Main application entry point
├── db_manager.py        # MongoDB connection and management
├── models/             # Data models
│   ├── base.py         # Base model with MongoDB operations
│   ├── report.py       # Report model for daily statistics
│   └── user.py         # User model for Instagram users
├── utils/              # Utility functions
│   ├── decorators.py   # Query timing decorators
│   └── time.py         # Time-related utilities
└── requirements.txt    # Project dependencies
```

## Configuration Options

- `DRY_RUN`: When enabled, limits data fetching to 10 users for testing
- `FORCE_RUN`: When enabled, regenerates today's report even if it exists
- `PRINT_QUERY_TIME`: When enabled, shows MongoDB query execution times

## Security Notes

- The tool uses secure session management to store Instagram authentication
- Session data is stored locally in the `session` directory
