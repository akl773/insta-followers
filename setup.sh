#!/bin/bash

echo "🚀 Setting up Instagram Follower Analyzer Script..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

echo "✅ Python dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << 'EOF'
# Instagram Credentials
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password

# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=InstagramStat

# Optional Settings
EXCEPTION_NOT_FOLLOWING_BACK=username1,username2
DRY_RUN=false
FORCE_RUN=false
PRINT_QUERY_TIME=false
SAVE_DIR=.
EOF
    echo "✅ .env file created. Please update it with your Instagram credentials."
else
    echo "ℹ️ .env file already exists"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Update the .env file with your Instagram credentials"
echo "2. Make sure MongoDB is running"
echo "3. Run the script: python main.py"
echo ""
echo "💡 The script will analyze your Instagram followers and following,"
echo "   generate reports, and save results to MongoDB."
