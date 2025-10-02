# Instagram Follower Analyzer

A command-line tool that helps you analyze and track your Instagram followers and following relationships. Generate detailed reports of your Instagram network and monitor changes over time.

## 🌟 Features

### Core Analytics
- 🔍 Track followers and following relationships
- 📊 Generate daily reports of your Instagram network
- 📈 Monitor follower/following changes over time
- 🤝 Identify mutual connections
- 💾 Store historical data in MongoDB
- 🔐 Secure session management for Instagram authentication

### Command-Line Interface
- 🎨 Beautiful terminal-based UI with color-coded output
- 📋 Interactive prompts and user choices
- ⚡ Fast data processing and analysis
- 🔧 Configuration options for testing and debugging


## 🏗️ Architecture

This project is a command-line tool (`main.py`) that analyzes Instagram follower relationships using the Instagram API and stores data in MongoDB.

## 📋 Prerequisites

- Python 3.7+
- MongoDB (local or remote)
- Instagram account credentials

## 🚀 Quick Start

1. **Clone and setup:**
```bash
git clone https://github.com/akl773/instagramFollowers.git
cd instagramFollowers
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Create `.env` file:**
```env
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=InstagramStat
DRY_RUN=false
FORCE_RUN=false
PRINT_QUERY_TIME=false
```

3. **Run the analyzer:**
```bash
python main.py
```

## 📁 Project Structure

```
instagramFollowers/
├── main.py                 # Command-line application entry point
├── db_manager.py           # MongoDB connection and management
├── models/                 # Data models
│   ├── base.py            # Base model with MongoDB operations
│   ├── report.py          # Report model for daily statistics
│   └── user.py            # User model for Instagram users
├── utils/                  # Utility functions
│   ├── decorators.py      # Query timing decorators
│   └── time.py            # Time-related utilities
├── session/                # Instagram session storage
├── setup.sh               # Automated setup script
└── requirements.txt       # Python dependencies
```

## ⚙️ Configuration Options

### Environment Variables
- `INSTAGRAM_USERNAME` - Your Instagram username
- `INSTAGRAM_PASSWORD` - Your Instagram password
- `MONGO_URI` - MongoDB connection string
- `DATABASE_NAME` - Database name for storing data
- `EXCEPTION_NOT_FOLLOWING_BACK` - Comma-separated usernames to exclude
- `DRY_RUN` - Limit data fetching to 10 users for testing
- `FORCE_RUN` - Regenerate today's report even if it exists
- `PRINT_QUERY_TIME` - Show MongoDB query execution times

## 🎯 Usage Examples

### Command-Line Tool
```bash
# Generate a daily report
python main.py

# Run in dry-run mode (limited data)
DRY_RUN=true python main.py

# Force regenerate today's report
FORCE_RUN=true python main.py
```


## 🔒 Security Notes

- Instagram credentials are stored securely in environment variables
- Session data is stored locally in the `session` directory
- No sensitive data is exposed in error messages

## 🛠️ Development

To run the script in development mode:

```bash
python main.py
```

For testing with limited data (dry run):
```bash
DRY_RUN=true python main.py
```

## 📈 Data Analysis Features

### Report Generation
- Daily automated reports
- Follower and following counts
- Mutual connection identification
- Change tracking between reports
- User relationship mapping

### Analytics
- Growth trend analysis
- Relationship distribution
- Net follower changes
- Historical data comparison
- User engagement insights

## 🎨 User Interface

### Command-Line Interface
- **Color-coded Output** - Easy-to-read terminal interface
- **Progress Indicators** - Real-time status updates
- **Formatted Tables** - Clean data presentation
- **Interactive Prompts** - User-friendly choices

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test the command-line interface
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:
1. Check that MongoDB is running
2. Verify your Instagram credentials in the `.env` file
3. Ensure all dependencies are installed
4. Check the console for error messages

## 🚀 Deployment

### Local Development
- Run `python main.py` for local testing
- Use `DRY_RUN=true` for limited data testing

### Production Usage
- Set up MongoDB (local or cloud)
- Configure environment variables securely
- Schedule the script to run daily using cron

---

**Analyze your Instagram followers and following with this powerful command-line tool! 🎉📊**
