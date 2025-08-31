# Instagram Follower Analyzer

A comprehensive Instagram analytics tool that helps you analyze and track your Instagram followers and following relationships. This project provides both a command-line interface and a modern web application for detailed insights into your Instagram network.

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

### Web Application
- 🌐 Modern React frontend with Material-UI
- 📱 Responsive design for desktop, tablet, and mobile
- 📊 Interactive charts and data visualizations
- 🔄 Real-time data updates
- 🎯 User-friendly dashboard and analytics pages

## 🏗️ Architecture

This project consists of two main components:

1. **Command-Line Tool** (`main.py`) - Original terminal-based analyzer
2. **Web Application** - Full-stack application with Flask backend and React frontend

## 📋 Prerequisites

- Python 3.7+
- Node.js 16+ (for web application)
- MongoDB (local or remote)
- Instagram account credentials

## 🚀 Quick Start

### Option 1: Web Application (Recommended)

1. **Clone the repository:**
```bash
git clone https://github.com/akl773/instagramFollowers.git
cd instagramFollowers
```

2. **Run the setup script:**
```bash
chmod +x setup.sh start.sh
./setup.sh
```

3. **Update the `.env` file with your Instagram credentials:**
```env
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=InstagramStat
```

4. **Start the application:**
```bash
./start.sh
```

5. **Access the web application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5001

### Option 2: Command-Line Tool

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

## 📊 Web Application Features

### Dashboard
- Real-time follower and following statistics
- Quick report generation
- Recent changes analysis
- User overview with profile pictures
- Relationship breakdown visualization

### Reports
- Historical data viewing
- Detailed analysis with expandable sections
- Change tracking between reports
- Sortable and filterable user lists

### Not Following Back
- Grid layout with user cards
- Direct Instagram profile links
- Exception handling for specific users
- Empty state handling

### Analytics
- Growth trend charts
- Relationship distribution pie charts
- Net changes bar charts
- Summary statistics
- Interactive data visualizations

## 🔌 API Endpoints

The web application provides a REST API:

- `GET /api/health` - Health check
- `GET /api/followers` - Get followers list
- `GET /api/following` - Get following list
- `GET /api/reports` - Get historical reports
- `GET /api/reports/latest` - Get latest report
- `POST /api/reports/generate` - Generate new report
- `GET /api/not-following-back` - Get users not following back
- `GET /api/user/<user_id>` - Get detailed user information

## 📁 Project Structure

```
instagramFollowers/
├── main.py                 # Command-line application entry point
├── app.py                  # Flask web application
├── db_manager.py           # MongoDB connection and management
├── models/                 # Data models
│   ├── base.py            # Base model with MongoDB operations
│   ├── report.py          # Report model for daily statistics
│   └── user.py            # User model for Instagram users
├── utils/                  # Utility functions
│   ├── decorators.py      # Query timing decorators
│   └── time.py            # Time-related utilities
├── frontend/              # React web application
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/         # Application pages
│   │   ├── services/      # API service functions
│   │   └── types/         # TypeScript type definitions
│   ├── package.json       # Frontend dependencies
│   └── vite.config.ts     # Vite configuration
├── session/               # Instagram session storage
├── setup.sh              # Automated setup script
├── start.sh              # Application startup script
└── requirements.txt      # Python dependencies
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

### Web Application
1. Open http://localhost:3000 in your browser
2. Navigate through the dashboard, reports, and analytics pages
3. Generate new reports using the dashboard
4. View detailed user information and relationship analysis

## 🔒 Security Notes

- Instagram credentials are stored securely in environment variables
- Session data is stored locally in the `session` directory
- The web application uses CORS protection
- No sensitive data is exposed in error messages

## 🛠️ Development

### Backend Development
```bash
# Start Flask backend in debug mode
python app.py
```

### Frontend Development
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
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

### Web Application
- **Modern Design** - Material-UI components with dark theme
- **Responsive Layout** - Works on all device sizes
- **Interactive Charts** - Recharts and Material-UI X Charts
- **Real-time Updates** - Live data fetching and display
- **Loading States** - Smooth user experience

### Command-Line Interface
- **Color-coded Output** - Easy-to-read terminal interface
- **Progress Indicators** - Real-time status updates
- **Formatted Tables** - Clean data presentation
- **Interactive Prompts** - User-friendly choices

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both command-line and web interfaces
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
- Use `./start.sh` for local development
- Both servers run on localhost with hot reload

### Production Deployment
- Build the frontend: `cd frontend && npm run build`
- Configure production environment variables
- Use a production WSGI server for Flask
- Set up proper MongoDB security

---

**Transform your Instagram analytics from command-line to a beautiful web experience! 🎉📊**
