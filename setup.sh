#!/bin/bash

echo "🚀 Setting up Instagram Analytics Web Application..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
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

# Install frontend dependencies
echo "⚛️ Installing React frontend dependencies..."
cd frontend

# Install dependencies
npm install

if [ $? -ne 0 ]; then
    echo "❌ Failed to install frontend dependencies"
    exit 1
fi

cd ..

echo "✅ Frontend dependencies installed"

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
echo "3. Start the Flask backend: python app.py"
echo "4. Start the React frontend: cd frontend && npm run dev"
echo ""
echo "🌐 The application will be available at:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:5000"
echo ""
echo "🔧 To start both servers:"
echo "   # Terminal 1 - Start Flask backend"
echo "   python app.py"
echo ""
echo "   # Terminal 2 - Start React frontend"
echo "   cd frontend"
echo "   npm run dev"
