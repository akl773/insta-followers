#!/bin/bash

echo "🚀 Starting Instagram Analytics Web Application..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please run ./setup.sh first."
    exit 1
fi

# Function to cleanup background processes
cleanup() {
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start Flask backend
echo "🔧 Starting Flask backend..."
python app.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Check if backend started successfully
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "❌ Failed to start Flask backend"
    exit 1
fi

echo "✅ Flask backend started (PID: $BACKEND_PID)"

# Start React frontend
echo "⚛️ Starting React frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Wait a moment for frontend to start
sleep 5

# Check if frontend started successfully
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo "❌ Failed to start React frontend"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo "✅ React frontend started (PID: $FRONTEND_PID)"

echo ""
echo "🎉 Application is running!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔌 Backend API: http://localhost:5001"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user to stop
wait
